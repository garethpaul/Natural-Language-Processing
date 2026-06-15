#!/usr/bin/env python3
# coding: utf-8
"""Stopword-overlap language detection sample."""

from __future__ import annotations

import argparse
import re
from pathlib import Path
from typing import Callable, Dict, Iterable, Mapping, Optional, Set

try:
    from nltk import wordpunct_tokenize as _nltk_wordpunct_tokenize
    from nltk.corpus import stopwords as _nltk_stopwords
except ImportError:  # pragma: no cover - covered by fallback behavior.
    _nltk_wordpunct_tokenize = None
    _nltk_stopwords = None


UNKNOWN_LANGUAGE = "unknown"
MIN_STOPWORD_MATCHES = 2
MIN_STOPWORD_MARGIN = 2
MIN_STOPWORD_DENSITY = 0.2
MAXIMUM_TEXT_CHARACTERS = 100_000
STOP_WORDS_PATH = Path(__file__).with_name("stop_words.txt")
DEFAULT_SAMPLE = """
Une adoption plus rapide que le telephone classique et mobile.
Au petit jeu des chiffres qui impressionnent, Skype indique qu'il a fallu
104 ans au telephone pour atteindre 300 millions d'usagers.
"""


def _fallback_tokenize(text: str) -> Iterable[str]:
    return re.findall(r"\w+|[^\w\s]", text, flags=re.UNICODE)


def _default_tokenizer() -> Callable[[str], Iterable[str]]:
    return _nltk_wordpunct_tokenize or _fallback_tokenize


def _normalise_tokens(tokens: Iterable[str]) -> Set[str]:
    if isinstance(tokens, (str, bytes)):
        return set()
    try:
        token_iterator = iter(tokens)
    except TypeError:
        return set()

    normalised_tokens = set()
    for token in token_iterator:
        if not isinstance(token, str):
            continue
        normalised_token = token.strip().lower()
        if any(character.isalpha() for character in normalised_token):
            normalised_tokens.add(normalised_token)
    return normalised_tokens


def _normalise_stopwords(words: Iterable[str]) -> Set[str]:
    normalised_words = set()
    for word in words:
        if not isinstance(word, str):
            continue
        normalised_word = word.strip().lower()
        if normalised_word:
            normalised_words.add(normalised_word)
    return normalised_words


def _normalise_language_name(language: str) -> str:
    if not isinstance(language, str):
        return ""

    normalised_language = language.strip().lower()
    if (
        not normalised_language.isprintable()
        or not any(character.isalpha() for character in normalised_language)
    ):
        return ""
    return normalised_language


def _normalise_stopword_sets(stopword_sets: Mapping[str, Iterable[str]]) -> Dict[str, Set[str]]:
    normalised_sets: Dict[str, Set[str]] = {}
    for language, stopwords in stopword_sets.items():
        normalised_language = _normalise_language_name(language)
        if not normalised_language:
            continue
        normalised_sets.setdefault(normalised_language, set()).update(
            _normalise_stopwords(stopwords)
        )
    return normalised_sets


def _normalised_text_words(
    text: str,
    tokenizer: Optional[Callable[[str], Iterable[str]]],
) -> Set[str]:
    if text is None:
        text = ""
    if not isinstance(text, str):
        raise ValueError("text must be a string")
    if len(text) > MAXIMUM_TEXT_CHARACTERS:
        raise ValueError("text exceeds 100000 character limit")
    return _normalise_tokens((tokenizer or _default_tokenizer())(text))


def load_checked_in_stop_words(path: Path = STOP_WORDS_PATH) -> Set[str]:
    """Load the small checked-in English stopword list."""
    return _normalise_stopwords(path.read_text(encoding="utf-8").splitlines())


def load_stopword_sets(stopwords_provider=None) -> Dict[str, Set[str]]:
    """Load NLTK stopwords, falling back to the checked-in English list."""
    if stopwords_provider is not None:
        return _normalise_stopword_sets({
            language: stopwords_provider.words(language)
            for language in stopwords_provider.fileids()
        })

    if _nltk_stopwords is not None:
        try:
            return _normalise_stopword_sets({
                language: _nltk_stopwords.words(language)
                for language in _nltk_stopwords.fileids()
            })
        except LookupError:
            pass

    return {"english": load_checked_in_stop_words()}


def _language_stopword_sets(
    stopword_sets: Optional[Mapping[str, Iterable[str]]],
    stopwords_provider,
) -> Mapping[str, Set[str]]:
    if stopword_sets is not None:
        return _normalise_stopword_sets(stopword_sets)

    return load_stopword_sets(stopwords_provider)


def _score_languages(
    words: Set[str],
    language_stopwords: Mapping[str, Set[str]],
) -> Dict[str, int]:
    return {
        language: len(words.intersection(stopwords))
        for language, stopwords in language_stopwords.items()
    }


def _has_enough_stopword_density(stopword_matches: int, word_count: int) -> bool:
    return (
        word_count > 0
        and stopword_matches / word_count >= MIN_STOPWORD_DENSITY
    )


def _calculate_languages_ratios(
    text: str,
    stopword_sets: Optional[Mapping[str, Iterable[str]]] = None,
    stopwords_provider=None,
    tokenizer: Optional[Callable[[str], Iterable[str]]] = None,
) -> Dict[str, int]:
    """Return the number of unique stopwords matched for each language."""
    words = _normalised_text_words(text, tokenizer)
    language_stopwords = _language_stopword_sets(stopword_sets, stopwords_provider)
    return _score_languages(words, language_stopwords)


def detect_language(
    text: str,
    stopword_sets: Optional[Mapping[str, Iterable[str]]] = None,
    stopwords_provider=None,
    tokenizer: Optional[Callable[[str], Iterable[str]]] = None,
) -> str:
    """Return the highest-scoring language, or ``unknown`` for zero matches."""
    words = _normalised_text_words(text, tokenizer)
    language_stopwords = _language_stopword_sets(stopword_sets, stopwords_provider)
    ratios = _score_languages(words, language_stopwords)
    if not ratios:
        return UNKNOWN_LANGUAGE

    highest_score = max(ratios.values())
    if highest_score < MIN_STOPWORD_MATCHES:
        return UNKNOWN_LANGUAGE
    if not _has_enough_stopword_density(highest_score, len(words)):
        return UNKNOWN_LANGUAGE

    highest_scoring_languages = [
        language
        for language, score in ratios.items()
        if score == highest_score
    ]
    if len(highest_scoring_languages) != 1:
        return UNKNOWN_LANGUAGE

    runner_up_score = max(
        (score for score in ratios.values() if score != highest_score),
        default=0,
    )
    if highest_score - runner_up_score < MIN_STOPWORD_MARGIN:
        return UNKNOWN_LANGUAGE

    return highest_scoring_languages[0]


def main(argv: Optional[Iterable[str]] = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("text", nargs="*", help="Text to classify. Uses sample text when omitted.")
    args = parser.parse_args(argv)
    text = " ".join(args.text) if args.text else DEFAULT_SAMPLE
    print(detect_language(text))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
