import unittest

from language_detection import (
    _calculate_languages_ratios,
    detect_language,
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
        self.stopwords = FakeStopwords()

    def test_calculates_stopword_overlap_by_language(self):
        ratios = _calculate_languages_ratios(
            "une adoption et des chiffres",
            stopwords_provider=self.stopwords,
            tokenizer=simple_tokenizer,
        )

        self.assertEqual(ratios["french"], 3)
        self.assertEqual(ratios["english"], 0)

    def test_detects_highest_scoring_language(self):
        language = detect_language(
            "the quick example and you will see",
            stopwords_provider=self.stopwords,
            tokenizer=simple_tokenizer,
        )

        self.assertEqual(language, "english")

    def test_returns_none_for_empty_or_unknown_text(self):
        self.assertIsNone(
            detect_language(
                "",
                stopwords_provider=self.stopwords,
                tokenizer=simple_tokenizer,
            )
        )
        self.assertIsNone(
            detect_language(
                "xyzzy plugh",
                stopwords_provider=self.stopwords,
                tokenizer=simple_tokenizer,
            )
        )


if __name__ == "__main__":
    unittest.main()
