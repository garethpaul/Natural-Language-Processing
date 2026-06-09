import unittest

from language_detection import (
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
        "english": [" The ", "AND", "", "  ", "\tyou\n"],
        "french": ["une"],
    }

    def fileids(self):
        return list(self.DATA)

    def words(self, language):
        return self.DATA[language]


def simple_tokenizer(text):
    return text.replace(".", " ").replace(",", " ").split()


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

    def test_checked_in_stop_words(self):
        words = load_checked_in_stop_words()

        self.assertIn("the", words)
        self.assertIn("and", words)


if __name__ == "__main__":
    unittest.main()
