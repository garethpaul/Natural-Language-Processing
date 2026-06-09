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

    def test_ambiguous_top_score_returns_unknown(self):
        self.assertEqual(
            detect_language(
                "the and une et",
                stopword_sets=self.stopword_sets,
                tokenizer=simple_tokenizer,
            ),
            UNKNOWN_LANGUAGE,
        )

    def test_checked_in_stop_words(self):
        words = load_checked_in_stop_words()

        self.assertIn("the", words)
        self.assertIn("and", words)


if __name__ == "__main__":
    unittest.main()
