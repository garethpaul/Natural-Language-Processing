import unittest

from language_detection import (
    MAXIMUM_TEXT_CHARACTERS,
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


def simple_tokenizer(text):
    return text.replace(".", " ").replace(",", " ").split()


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


if __name__ == "__main__":
    unittest.main()
