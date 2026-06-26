import io
import json
import os
import re
import tempfile
import unittest
import zipfile
from contextlib import redirect_stdout
from pathlib import Path
from urllib.parse import quote
from unittest.mock import patch

import language_detection

from language_detection import (
    MAXIMUM_TEXT_CHARACTERS,
    MIN_STOPWORD_MARGIN,
    MIN_STOPWORD_MATCHES,
    UNKNOWN_LANGUAGE,
    _calculate_languages_ratios,
    detect_language,
    load_checked_in_stop_words,
    load_stopword_sets,
)


class FakeStopwords:
    DATA = {
        "english": ["the", "and", "you", "will", "there"],
        "french": ["une", "le", "la", "et", "des"],
        "spanish": ["el", "la", "y", "que"],
    }

    def fileids(self):
        return list(self.DATA)

    def words(self, language):
        return self.DATA[language]


class CorpusOverlapStopwords:
    FIXTURE_PATH = Path(__file__).with_name("fixtures") / "nltk_stopword_overlap.json"

    def __init__(self):
        fixture = json.loads(self.FIXTURE_PATH.read_text(encoding="utf-8"))
        self.provenance = fixture["provenance"]
        self.data = fixture["stopwords_by_language"]

    def fileids(self):
        return list(self.data)

    def words(self, language):
        return self.data[language]


class NoisyStopwords:
    DATA = {
        "english": [" The ", "AND", "", "  ", "\tyou\n", None, 123],
        "french": ["une"],
    }

    def fileids(self):
        return list(self.DATA)

    def words(self, language):
        return self.DATA[language]


class NoisyLanguageStopwords:
    DATA = {
        " English ": [" The ", "AND"],
        "ENGLISH": ["you"],
        " French ": ["une"],
        "  ": ["ignored"],
    }

    def fileids(self):
        return list(self.DATA)

    def words(self, language):
        return self.DATA[language]


class MalformedEntryStopwords:
    DATA = {
        "english": [" The ", None, 123, b"and", object(), "AND", "you"],
        "french": ["une"],
    }

    def fileids(self):
        return list(self.DATA)

    def words(self, language):
        return self.DATA[language]


class ScalarCollectionStopwords:
    def __init__(self, words):
        self.words_value = words

    def fileids(self):
        return ["english"]

    def words(self, language):
        return self.words_value


class ScalarLanguageCollectionStopwords:
    def __init__(self, languages):
        self.languages = languages
        self.words_calls = []

    def fileids(self):
        return self.languages

    def words(self, language):
        self.words_calls.append(language)
        return ["the", "and", "you"]


class MappingLanguageCollectionStopwords(ScalarLanguageCollectionStopwords):
    def __init__(self):
        super().__init__({"english": object(), "french": object()})


def simple_tokenizer(text):
    return text.replace(".", " ").replace(",", " ").split()


def nltk_wordpunct_equivalent_tokenizer(text):
    return re.findall(r"\w+|[^\w\s]+", text, flags=re.UNICODE)


def padded_tokenizer(text):
    return [" The ", "\tAND\n", "signal"]


def malformed_entry_tokenizer(text):
    return [" The ", None, 123, b"and", object(), "AND", "you", "", "!!!"]


class FailingStopwordIterable:
    def __iter__(self):
        yield "the"
        yield "and"
        raise RuntimeError("private stopword iteration failure")


class FailingStopwordMapping:
    def items(self):
        yield "english", ["the", "and"]
        raise RuntimeError("private stopword mapping iteration failure")


class FailingProviderFileids:
    def fileids(self):
        raise RuntimeError("private provider fileids failure")


class FailingProviderWords:
    def fileids(self):
        return ["english", "french"]

    def words(self, language):
        if language == "english":
            return ["the", "and", "you"]
        raise RuntimeError("private provider words failure")


class MissingCorpusStopwords:
    def fileids(self):
        raise LookupError("missing private corpus path")


class BrokenDefaultStopwords:
    def fileids(self):
        raise RuntimeError("private default provider failure")


class LanguageDetectionTests(unittest.TestCase):
    def setUp(self):
        self.stopword_sets = load_stopword_sets(FakeStopwords())

    def test_calculate_language_ratios(self):
        ratios = _calculate_languages_ratios(
            "une adoption et des chiffres",
            stopword_sets=self.stopword_sets,
            tokenizer=simple_tokenizer,
        )

        self.assertEqual(ratios["french"], 3)
        self.assertEqual(ratios["english"], 0)

    def test_detect_language(self):
        language = detect_language(
            "the quick example and you will see",
            stopword_sets=self.stopword_sets,
            tokenizer=simple_tokenizer,
        )

        self.assertEqual(language, "english")

    def test_unknown(self):
        self.assertEqual(
            detect_language(
                "",
                stopword_sets=self.stopword_sets,
                tokenizer=simple_tokenizer,
            ),
            UNKNOWN_LANGUAGE,
        )
        self.assertEqual(
            detect_language(
                "the",
                stopword_sets=self.stopword_sets,
                tokenizer=simple_tokenizer,
            ),
            UNKNOWN_LANGUAGE,
        )
        self.assertEqual(
            detect_language(
                "xyzzy plugh",
                stopword_sets=self.stopword_sets,
                tokenizer=simple_tokenizer,
            ),
            UNKNOWN_LANGUAGE,
        )

    def test_empty_stopword_mapping_is_no_evidence(self):
        self.assertEqual(
            _calculate_languages_ratios(
                "the and you",
                stopword_sets={},
                tokenizer=simple_tokenizer,
            ),
            {},
        )
        self.assertEqual(
            detect_language(
                "the and you",
                stopword_sets={},
                tokenizer=simple_tokenizer,
            ),
            UNKNOWN_LANGUAGE,
        )

    def test_stopword_mapping_iteration_failure_discards_partial_evidence(self):
        self.assertEqual(
            _calculate_languages_ratios(
                "the example and signal",
                stopword_sets=FailingStopwordMapping(),
                tokenizer=simple_tokenizer,
            ),
            {},
        )
        self.assertEqual(
            detect_language(
                "the example and signal",
                stopword_sets=FailingStopwordMapping(),
                tokenizer=simple_tokenizer,
            ),
            UNKNOWN_LANGUAGE,
        )

    def test_explicit_stopword_provider_invocation_failures_discard_all_evidence(self):
        for provider in (FailingProviderFileids(), FailingProviderWords()):
            with self.subTest(provider=type(provider).__name__):
                self.assertEqual(load_stopword_sets(provider), {})
                self.assertEqual(
                    _calculate_languages_ratios(
                        "the and you",
                        stopwords_provider=provider,
                        tokenizer=simple_tokenizer,
                    ),
                    {},
                )
                self.assertEqual(
                    detect_language(
                        "the and you",
                        stopwords_provider=provider,
                        tokenizer=simple_tokenizer,
                    ),
                    UNKNOWN_LANGUAGE,
                )

    def test_scalar_provider_language_collections_are_empty_evidence(self):
        for malformed_collection in ("english", b"english"):
            with self.subTest(collection_type=type(malformed_collection).__name__):
                provider = ScalarLanguageCollectionStopwords(malformed_collection)

                self.assertEqual(load_stopword_sets(provider), {})
                self.assertEqual(provider.words_calls, [])
                self.assertEqual(
                    _calculate_languages_ratios(
                        "the and you",
                        stopwords_provider=provider,
                        tokenizer=simple_tokenizer,
                    ),
                    {},
                )
                self.assertEqual(provider.words_calls, [])
                self.assertEqual(
                    detect_language(
                        "the and you",
                        stopwords_provider=provider,
                        tokenizer=simple_tokenizer,
                    ),
                    UNKNOWN_LANGUAGE,
                )
                self.assertEqual(provider.words_calls, [])

    def test_mapping_provider_language_collections_are_empty_evidence(self):
        provider = MappingLanguageCollectionStopwords()

        self.assertEqual(load_stopword_sets(provider), {})
        self.assertEqual(provider.words_calls, [])
        self.assertEqual(
            _calculate_languages_ratios(
                "the and you",
                stopwords_provider=provider,
                tokenizer=simple_tokenizer,
            ),
            {},
        )
        self.assertEqual(provider.words_calls, [])
        self.assertEqual(
            detect_language(
                "the and you",
                stopwords_provider=provider,
                tokenizer=simple_tokenizer,
            ),
            UNKNOWN_LANGUAGE,
        )
        self.assertEqual(provider.words_calls, [])

    def test_missing_default_stopword_corpus_uses_checked_in_fallback(self):
        with patch.object(language_detection, "_nltk_stopwords", MissingCorpusStopwords()), \
                patch.object(language_detection, "load_checked_in_stop_words", return_value={"the", "and"}):
            self.assertEqual(load_stopword_sets(), {"english": {"the", "and"}})

    def test_no_argument_main_uses_english_when_nltk_is_unavailable(self):
        output = io.StringIO()

        with patch.object(language_detection, "_nltk_stopwords", None), \
                patch.object(language_detection, "_nltk_wordpunct_tokenize", None), \
                redirect_stdout(output):
            exit_code = language_detection.main([])

        self.assertEqual(exit_code, 0)
        self.assertEqual(output.getvalue(), "english\n")

    def test_no_argument_main_uses_english_when_corpus_is_unavailable(self):
        output = io.StringIO()

        with patch.object(language_detection, "_nltk_stopwords", MissingCorpusStopwords()), \
                patch.object(language_detection, "_nltk_wordpunct_tokenize", None), \
                redirect_stdout(output):
            exit_code = language_detection.main([])

        self.assertEqual(exit_code, 0)
        self.assertEqual(output.getvalue(), "english\n")

    def test_default_sample_leads_all_corpus_languages_by_required_margin(self):
        provider = CorpusOverlapStopwords()
        ratios = _calculate_languages_ratios(
            language_detection.DEFAULT_SAMPLE,
            stopwords_provider=provider,
            tokenizer=nltk_wordpunct_equivalent_tokenizer,
        )
        english_score = ratios["english"]
        runner_up_score = max(
            score for language, score in ratios.items() if language != "english"
        )

        self.assertEqual(provider.provenance["language_count"], 33)
        self.assertEqual(len(ratios), provider.provenance["language_count"])
        self.assertGreaterEqual(english_score, MIN_STOPWORD_MATCHES)
        self.assertEqual(ratios["hinglish"], runner_up_score)
        self.assertGreaterEqual(
            english_score - runner_up_score,
            MIN_STOPWORD_MARGIN,
        )
        self.assertEqual(max(ratios, key=ratios.get), "english")

    def test_no_argument_main_uses_english_complete_corpus_overlap_fixture(self):
        output = io.StringIO()

        with patch.object(language_detection, "_nltk_stopwords", CorpusOverlapStopwords()), \
                patch.object(language_detection, "_nltk_wordpunct_tokenize", nltk_wordpunct_equivalent_tokenizer), \
                redirect_stdout(output):
            exit_code = language_detection.main([])

        self.assertEqual(exit_code, 0)
        self.assertEqual(output.getvalue(), "english\n")

    def test_no_argument_main_prints_detector_result_for_default_sample(self):
        output = io.StringIO()
        patched_sample = "patched default sample"

        with patch.object(language_detection, "DEFAULT_SAMPLE", patched_sample), \
                patch.object(language_detection, "detect_language", return_value="detected") as detector, \
                redirect_stdout(output):
            exit_code = language_detection.main([])

        detector.assert_called_once_with(patched_sample)
        self.assertEqual(exit_code, 0)
        self.assertEqual(output.getvalue(), "detected\n")

    def test_unexpected_default_stopword_provider_failure_returns_empty_evidence(self):
        with patch.object(language_detection, "_nltk_stopwords", BrokenDefaultStopwords()), \
                patch.object(language_detection, "load_checked_in_stop_words") as fallback:
            self.assertEqual(load_stopword_sets(), {})
            fallback.assert_not_called()

    def test_punctuation_only_tokens_do_not_create_stopword_evidence(self):
        stopword_sets = {"english": {"-", "&"}}

        self.assertEqual(
            _calculate_languages_ratios(
                "- &",
                stopword_sets=stopword_sets,
                tokenizer=simple_tokenizer,
            ),
            {"english": 0},
        )
        self.assertEqual(
            detect_language(
                "- &",
                stopword_sets=stopword_sets,
                tokenizer=simple_tokenizer,
            ),
            UNKNOWN_LANGUAGE,
        )

    def test_ambiguous_top_score_returns_unknown(self):
        self.assertEqual(
            detect_language(
                "the and une et",
                stopword_sets=self.stopword_sets,
                tokenizer=simple_tokenizer,
            ),
            UNKNOWN_LANGUAGE,
        )

    def test_near_tie_stopword_scores_return_unknown(self):
        self.assertEqual(
            detect_language(
                "the and you une et",
                stopword_sets=self.stopword_sets,
                tokenizer=simple_tokenizer,
            ),
            UNKNOWN_LANGUAGE,
        )

    def test_long_balanced_mixed_language_passage_returns_unknown(self):
        text = (
            "the designer and you will review there before sunrise while the "
            "team prepares une maquette et le client compare la palette des couleurs"
        )

        self.assertEqual(
            detect_language(
                text,
                stopword_sets=self.stopword_sets,
                tokenizer=simple_tokenizer,
            ),
            UNKNOWN_LANGUAGE,
        )

    def test_long_mixed_language_passage_with_clear_margin_returns_winner(self):
        text = (
            "the designer and you will review there before sunrise while the "
            "team prepares une maquette et compares every color carefully"
        )

        self.assertEqual(
            detect_language(
                text,
                stopword_sets=self.stopword_sets,
                tokenizer=simple_tokenizer,
            ),
            "english",
        )

    def test_sparse_stopword_evidence_returns_unknown(self):
        self.assertEqual(
            detect_language(
                "the and alpha beta gamma delta epsilon zeta eta theta iota kappa",
                stopword_sets=self.stopword_sets,
                tokenizer=simple_tokenizer,
            ),
            UNKNOWN_LANGUAGE,
        )

    def test_stopword_entries_are_normalized_and_blank_entries_ignored(self):
        stopword_sets = load_stopword_sets(NoisyStopwords())

        self.assertEqual(stopword_sets["english"], {"the", "and", "you"})
        self.assertEqual(
            detect_language(
                "the and you",
                stopword_sets=stopword_sets,
                tokenizer=simple_tokenizer,
            ),
            "english",
        )

    def test_explicit_stopword_sets_are_normalized_before_scoring(self):
        stopword_sets = {
            "english": [" The ", "\tAND\n", "YOU", "", "  ", None, 123],
            "french": {"une"},
        }

        self.assertEqual(
            _calculate_languages_ratios(
                "the and you",
                stopword_sets=stopword_sets,
                tokenizer=simple_tokenizer,
            ),
            {"english": 3, "french": 0},
        )
        self.assertEqual(
            detect_language(
                "the and you",
                stopword_sets=stopword_sets,
                tokenizer=simple_tokenizer,
            ),
            "english",
        )

    def test_explicit_stopword_language_labels_are_normalized_before_scoring(self):
        stopword_sets = {
            " English ": {" The ", "AND"},
            "ENGLISH": {"you"},
            " French ": {"une"},
            "  ": {"ignored"},
        }

        self.assertEqual(
            _calculate_languages_ratios(
                "the and you",
                stopword_sets=stopword_sets,
                tokenizer=simple_tokenizer,
            ),
            {"english": 3, "french": 0},
        )
        self.assertEqual(
            detect_language(
                "the and you",
                stopword_sets=stopword_sets,
                tokenizer=simple_tokenizer,
            ),
            "english",
        )

    def test_invalid_language_labels_are_ignored(self):
        stopword_sets = {
            None: {"the", "and", "you"},
            123: {"the", "and", "you"},
            "---": {"the", "and", "you"},
            " English ": {"the", "and", "you"},
        }

        self.assertEqual(
            _calculate_languages_ratios(
                "the and you",
                stopword_sets=stopword_sets,
                tokenizer=simple_tokenizer,
            ),
            {"english": 3},
        )
        self.assertEqual(
            detect_language(
                "the and you",
                stopword_sets=stopword_sets,
                tokenizer=simple_tokenizer,
            ),
            "english",
        )

    def test_control_character_language_labels_are_ignored(self):
        stopword_sets = {
            "eng\nlish": {"the", "and", "you"},
            "eng\x1b[31m": {"the", "and", "you"},
            " English ": {"the", "and", "you"},
        }

        self.assertEqual(
            _calculate_languages_ratios(
                "the and you",
                stopword_sets=stopword_sets,
                tokenizer=simple_tokenizer,
            ),
            {"english": 3},
        )
        self.assertEqual(
            detect_language(
                "the and you",
                stopword_sets=stopword_sets,
                tokenizer=simple_tokenizer,
            ),
            "english",
        )

    def test_provider_language_labels_are_normalized_before_scoring(self):
        stopword_sets = load_stopword_sets(NoisyLanguageStopwords())

        self.assertEqual(
            stopword_sets,
            {"english": {"the", "and", "you"}, "french": {"une"}},
        )
        self.assertEqual(
            detect_language(
                "the and you",
                stopword_sets=stopword_sets,
                tokenizer=simple_tokenizer,
            ),
            "english",
        )

    def test_non_string_mapping_stopword_entries_are_ignored(self):
        stopword_sets = {
            "english": [" The ", None, 123, b"and", object(), "AND", "you"],
            "french": ["une"],
        }

        self.assertEqual(
            _calculate_languages_ratios(
                "the and you",
                stopword_sets=stopword_sets,
                tokenizer=simple_tokenizer,
            ),
            {"english": 3, "french": 0},
        )

    def test_non_string_provider_stopword_entries_are_ignored(self):
        stopword_sets = load_stopword_sets(MalformedEntryStopwords())

        self.assertEqual(
            stopword_sets,
            {"english": {"the", "and", "you"}, "french": {"une"}},
        )
        self.assertEqual(
            detect_language(
                "the and you",
                stopword_sets=stopword_sets,
                tokenizer=simple_tokenizer,
            ),
            "english",
        )

    def test_scalar_stopword_collections_are_empty_evidence(self):
        for malformed_collection in ("the", b"the"):
            with self.subTest(collection_type=type(malformed_collection).__name__):
                explicit_sets = {"english": malformed_collection}
                provider_sets = load_stopword_sets(
                    ScalarCollectionStopwords(malformed_collection)
                )

                self.assertEqual(provider_sets, {"english": set()})
                for stopword_sets in (explicit_sets, provider_sets):
                    self.assertEqual(
                        _calculate_languages_ratios(
                            "t h",
                            stopword_sets=stopword_sets,
                            tokenizer=simple_tokenizer,
                        ),
                        {"english": 0},
                    )
                    self.assertEqual(
                        detect_language(
                            "t h",
                            stopword_sets=stopword_sets,
                            tokenizer=simple_tokenizer,
                        ),
                        UNKNOWN_LANGUAGE,
                    )

    def test_mapping_stopword_collections_are_empty_evidence(self):
        stopword_sets = {
            "english": {"the": True, "and": True, "you": True},
            "french": ["une", "deux", "trois"],
        }

        self.assertEqual(
            _calculate_languages_ratios(
                "the and you une deux trois",
                stopword_sets=stopword_sets,
                tokenizer=simple_tokenizer,
            ),
            {"english": 0, "french": 3},
        )
        self.assertEqual(
            detect_language(
                "the and you une deux trois",
                stopword_sets=stopword_sets,
                tokenizer=simple_tokenizer,
            ),
            "french",
        )

    def test_text_tokens_are_normalized_before_scoring(self):
        self.assertEqual(
            _calculate_languages_ratios(
                "ignored input",
                stopword_sets=self.stopword_sets,
                tokenizer=padded_tokenizer,
            )["english"],
            2,
        )
        self.assertEqual(
            detect_language(
                "ignored input",
                stopword_sets=self.stopword_sets,
                tokenizer=padded_tokenizer,
            ),
            "english",
        )

    def test_non_string_tokenizer_entries_are_ignored(self):
        self.assertEqual(
            _calculate_languages_ratios(
                "ignored input",
                stopword_sets=self.stopword_sets,
                tokenizer=malformed_entry_tokenizer,
            ),
            {"english": 3, "french": 0, "spanish": 0},
        )
        self.assertEqual(
            detect_language(
                "ignored input",
                stopword_sets=self.stopword_sets,
                tokenizer=malformed_entry_tokenizer,
            ),
            "english",
        )

    def test_stopword_iteration_failure_discards_partial_language_evidence(self):
        stopword_sets = {
            "english": FailingStopwordIterable(),
            "french": {"une", "deux", "trois"},
        }

        self.assertEqual(
            _calculate_languages_ratios(
                "the and une deux trois",
                stopword_sets=stopword_sets,
                tokenizer=simple_tokenizer,
            ),
            {"english": 0, "french": 3},
        )
        self.assertEqual(
            detect_language(
                "the and une deux trois",
                stopword_sets=stopword_sets,
                tokenizer=simple_tokenizer,
            ),
            "french",
        )

    def test_malformed_tokenizer_output_collections_return_unknown(self):
        malformed_outputs = [None, 123, object(), "the and you", b"the and you"]

        for malformed_output in malformed_outputs:
            with self.subTest(output_type=type(malformed_output).__name__):
                def malformed_output_tokenizer(_text):
                    return malformed_output

                self.assertEqual(
                    _calculate_languages_ratios(
                        "ignored input",
                        stopword_sets=self.stopword_sets,
                        tokenizer=malformed_output_tokenizer,
                    ),
                    {"english": 0, "french": 0, "spanish": 0},
                )
                self.assertEqual(
                    detect_language(
                        "ignored input",
                        stopword_sets=self.stopword_sets,
                        tokenizer=malformed_output_tokenizer,
                    ),
                    UNKNOWN_LANGUAGE,
                )

    def test_mapping_tokenizer_output_collections_return_unknown(self):
        def mapping_output_tokenizer(_text):
            return {"the": object(), "and": object(), "you": object()}

        self.assertEqual(
            _calculate_languages_ratios(
                "ignored input",
                stopword_sets=self.stopword_sets,
                tokenizer=mapping_output_tokenizer,
            ),
            {"english": 0, "french": 0, "spanish": 0},
        )
        self.assertEqual(
            detect_language(
                "ignored input",
                stopword_sets=self.stopword_sets,
                tokenizer=mapping_output_tokenizer,
            ),
            UNKNOWN_LANGUAGE,
        )

    def test_tokenizer_iteration_failure_discards_partial_evidence(self):
        def failing_tokenizer(_text):
            yield "the"
            yield "and"
            raise RuntimeError("private tokenizer failure")

        self.assertEqual(
            _calculate_languages_ratios(
                "ignored input",
                stopword_sets=self.stopword_sets,
                tokenizer=failing_tokenizer,
            ),
            {"english": 0, "french": 0, "spanish": 0},
        )
        self.assertEqual(
            detect_language(
                "ignored input",
                stopword_sets=self.stopword_sets,
                tokenizer=failing_tokenizer,
            ),
            UNKNOWN_LANGUAGE,
        )

    def test_tokenizer_invocation_failure_returns_unknown(self):
        def failing_tokenizer(_text):
            raise RuntimeError("private tokenizer invocation failure")

        self.assertEqual(
            _calculate_languages_ratios(
                "private input",
                stopword_sets=self.stopword_sets,
                tokenizer=failing_tokenizer,
            ),
            {"english": 0, "french": 0, "spanish": 0},
        )
        self.assertEqual(
            detect_language(
                "private input",
                stopword_sets=self.stopword_sets,
                tokenizer=failing_tokenizer,
            ),
            UNKNOWN_LANGUAGE,
        )

    def test_text_character_limit_is_checked_before_tokenization(self):
        tokenizer_calls = []

        def recording_tokenizer(text):
            tokenizer_calls.append(text)
            return []

        boundary_text = "x" * MAXIMUM_TEXT_CHARACTERS
        self.assertEqual(
            _calculate_languages_ratios(
                boundary_text,
                stopword_sets=self.stopword_sets,
                tokenizer=recording_tokenizer,
            ),
            {"english": 0, "french": 0, "spanish": 0},
        )
        self.assertEqual(tokenizer_calls, [boundary_text])

        with self.assertRaisesRegex(ValueError, "text exceeds 100000 character limit"):
            detect_language(
                boundary_text + "x",
                stopword_sets=self.stopword_sets,
                tokenizer=recording_tokenizer,
            )
        self.assertEqual(tokenizer_calls, [boundary_text])

    def test_invalid_text_types_are_rejected_without_echoing_values(self):
        with self.assertRaisesRegex(ValueError, "^text must be a string$"):
            detect_language(123, stopword_sets=self.stopword_sets)

    def test_none_text_retains_empty_text_behavior(self):
        self.assertEqual(detect_language(None, stopword_sets=self.stopword_sets), UNKNOWN_LANGUAGE)

    def test_checked_in_stop_words(self):
        words = load_checked_in_stop_words()

        self.assertIn("the", words)
        self.assertIn("and", words)

    def test_nltk_strict_path_enforcement_blocks_encoded_absolute_paths(self):
        if language_detection._nltk_pathsec is None:
            self.skipTest("NLTK strict path enforcement is unavailable")

        from nltk import data

        self.assertTrue(language_detection._nltk_pathsec.ENFORCE)
        encoded_path = quote(str(Path(__file__).resolve()), safe="")
        with patch.object(
            language_detection._nltk_pathsec,
            "_get_allowed_roots",
            return_value=set(),
        ):
            with self.assertRaises((PermissionError, ValueError)) as blocked:
                data.load(f"file://{encoded_path}", format="raw")

        self.assertRegex(
            str(blocked.exception),
            r"Unauthorized path|Unsafe resource path",
        )

    def test_nltk_strict_path_enforcement_does_not_implicitly_trust_temp(self):
        if language_detection._nltk_pathsec is None:
            self.skipTest("NLTK strict path enforcement is unavailable")

        from nltk import data

        with tempfile.TemporaryDirectory() as temporary_directory:
            temporary_path = Path(temporary_directory)
            trusted_root = temporary_path / "trusted"
            trusted_root.mkdir()
            secret_path = temporary_path / "secret.txt"
            secret_path.write_bytes(b"private")
            symlink_path = trusted_root / "link.txt"
            try:
                symlink_path.symlink_to(secret_path)
            except (NotImplementedError, OSError):
                symlink_path = None

            encoded_secret_path = quote(str(secret_path.resolve()), safe="")
            double_encoded_secret_path = quote(encoded_secret_path, safe="")
            hostile_resources = [
                f"file://{encoded_secret_path}",
                f"file://{encoded_secret_path.replace('%2F', '%2f')}",
                f"file://{double_encoded_secret_path}",
                f"nltk:{encoded_secret_path}",
                f"nltk:{encoded_secret_path.replace('%2F', '%2f')}",
                f"nltk:{double_encoded_secret_path}",
                "nltk:%2e%2e/secret.txt",
                "nltk:..%2fsecret.txt",
                "nltk:%252e%252e%252fsecret.txt",
                "nltk:..∕secret.txt",
                "nltk:..⁄secret.txt",
                "nltk:..%E2%88%95secret.txt",
                "nltk:..%E2%81%84secret.txt",
                str(secret_path.resolve()),
                "nltk:C:/Windows/win.ini",
                r"nltk:C:\Windows\win.ini",
                "C:/Windows/win.ini",
                r"C:\Windows\win.ini",
                r"\\server\share\file.txt",
                "file://server/share/file.txt",
            ]
            if symlink_path is not None:
                hostile_resources.append(f"file://{symlink_path.absolute()}")

            with patch.object(data, "path", [str(trusted_root)]), patch.dict(
                os.environ,
                {"NLTK_DATA": ""},
            ):
                data.clear_cache()
                for resource_name in hostile_resources:
                    with self.subTest(resource_name=resource_name):
                        with self.assertRaises((LookupError, PermissionError, ValueError)):
                            data.load(resource_name, format="raw", cache=False)

    def test_nltk_strict_path_enforcement_preserves_legitimate_resources(self):
        if language_detection._nltk_pathsec is None:
            self.skipTest("NLTK strict path enforcement is unavailable")

        from nltk import data

        with tempfile.TemporaryDirectory() as temporary_directory:
            trusted_root = Path(temporary_directory) / "trusted"
            resource_path = trusted_root / "corpora" / "demo" / "words.txt"
            resource_path.parent.mkdir(parents=True)
            resource_path.write_bytes(b"directory resource")
            archive_path = trusted_root / "corpora" / "archive.zip"
            with zipfile.ZipFile(archive_path, "w") as archive:
                archive.writestr("archive/words.txt", b"zip resource")
                archive.writestr("../outside.txt", b"not a filesystem escape")

            with patch.object(data, "path", [str(trusted_root)]), patch.dict(
                os.environ,
                {"NLTK_DATA": ""},
            ):
                data.clear_cache()
                self.assertEqual(
                    data.load("corpora/demo/words.txt", format="raw", cache=False),
                    b"directory resource",
                )
                self.assertEqual(
                    data.load(
                        "corpora/archive.zip/archive/words.txt",
                        format="raw",
                        cache=False,
                    ),
                    b"zip resource",
                )
                for resource_name in (
                    "corpora/archive.zip/../outside.txt",
                    "corpora/archive.zip/%2e%2e/outside.txt",
                    "corpora/archive.zip/..%2foutside.txt",
                ):
                    with self.subTest(resource_name=resource_name):
                        with self.assertRaises((LookupError, PermissionError, ValueError)):
                            data.load(resource_name, format="raw", cache=False)

    def test_nltk_trusted_root_configuration_is_bounded(self):
        if language_detection._nltk_pathsec is None:
            self.skipTest("NLTK strict path enforcement is unavailable")

        from nltk import data

        excessive_roots = [f"/tmp/nltk-root-{index}" for index in range(65)]
        with patch.object(data, "path", excessive_roots), patch.dict(
            os.environ,
            {"NLTK_DATA": ""},
        ):
            with self.assertRaisesRegex(ValueError, "at most 64 trusted data roots"):
                language_detection._nltk_allowed_roots()

        oversized_root = "/" + "x" * 4097
        with patch.object(data, "path", [oversized_root]), patch.dict(
            os.environ,
            {"NLTK_DATA": ""},
        ):
            with self.assertRaisesRegex(ValueError, "trusted data root exceeds 4096 characters"):
                language_detection._nltk_allowed_roots()

        with patch.object(data, "path", [Path(Path.cwd().anchor)]), patch.dict(
            os.environ,
            {"NLTK_DATA": ""},
        ):
            with self.assertRaisesRegex(ValueError, "filesystem roots cannot be trusted"):
                language_detection._nltk_allowed_roots()


if __name__ == "__main__":
    unittest.main()
