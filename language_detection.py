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


def load_checked_in_stop_words(path: Path = STOP_WORDS_PATH) -> Set[str]:
    """Load the small checked-in English stopword list."""
    return {
        line.strip().lower()
        for line in path.read_text(encoding="utf-8").splitlines()
        if line.strip()
    }


def load_stopword_sets(stopwords_provider=None) -> Dict[str, Set[str]]:
    """Load NLTK stopwords, falling back to the checked-in English list."""
    if stopwords_provider is not None:
        return {
            language: {word.lower() for word in stopwords_provider.words(language)}
            for language in stopwords_provider.fileids()
        }

    if _nltk_stopwords is not None:
        try:
            return {
                language: {word.lower() for word in _nltk_stopwords.words(language)}
                for language in _nltk_stopwords.fileids()
            }
        except LookupError:
            pass

    return {"english": load_checked_in_stop_words()}


def _calculate_languages_ratios(
    text: str,
    stopword_sets: Optional[Mapping[str, Set[str]]] = None,
    stopwords_provider=None,
    tokenizer: Optional[Callable[[str], Iterable[str]]] = None,
) -> Dict[str, int]:
    """Return the number of unique stopwords matched for each language."""
    words = {word.lower() for word in (tokenizer or _default_tokenizer())(text or "")}
    language_stopwords = stopword_sets or load_stopword_sets(stopwords_provider)

    return {
        language: len(words.intersection(stopwords))
        for language, stopwords in language_stopwords.items()
    }


def detect_language(
    text: str,
    stopword_sets: Optional[Mapping[str, Set[str]]] = None,
    stopwords_provider=None,
    tokenizer: Optional[Callable[[str], Iterable[str]]] = None,
) -> str:
    """Return the highest-scoring language, or ``unknown`` for zero matches."""
    ratios = _calculate_languages_ratios(text, stopword_sets, stopwords_provider, tokenizer)
    if not ratios:
        return UNKNOWN_LANGUAGE

    most_rated_language = max(ratios, key=ratios.get)
    if ratios[most_rated_language] < MIN_STOPWORD_MATCHES:
        return UNKNOWN_LANGUAGE

    return most_rated_language


def main(argv: Optional[Iterable[str]] = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("text", nargs="*", help="Text to classify. Uses sample text when omitted.")
    args = parser.parse_args(argv)
    text = " ".join(args.text) if args.text else DEFAULT_SAMPLE
    print(detect_language(text))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
