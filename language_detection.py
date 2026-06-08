#!/usr/bin/env python3
# coding: utf-8
"""Stopword-overlap language detection sample."""

from __future__ import annotations

import re
import sys
from typing import Callable, Dict, Iterable, Optional

try:
    from nltk import wordpunct_tokenize as _nltk_wordpunct_tokenize
    from nltk.corpus import stopwords as _nltk_stopwords
except ImportError:  # pragma: no cover - exercised through dependency checks.
    _nltk_wordpunct_tokenize = None
    _nltk_stopwords = None


DEFAULT_SAMPLE = """
Une adoption plus rapide que le telephone classique et mobile.
Au petit jeu des chiffres qui impressionnent, Skype indique qu'il a fallu
104 ans au telephone pour atteindre 300 millions d'usagers.
"""


class MissingNltkError(RuntimeError):
    """Raised when the sample is run without its NLTK dependency."""


def _fallback_tokenize(text: str) -> Iterable[str]:
    return re.findall(r"\w+|[^\w\s]", text, flags=re.UNICODE)


def _default_tokenizer() -> Callable[[str], Iterable[str]]:
    return _nltk_wordpunct_tokenize or _fallback_tokenize


def _default_stopwords_provider():
    if _nltk_stopwords is None:
        raise MissingNltkError(
            "Install nltk and its stopwords corpus, or pass a stopwords provider."
        )
    try:
        _nltk_stopwords.fileids()
    except LookupError as error:
        raise MissingNltkError(
            "Install the NLTK stopwords corpus with: python3 -m nltk.downloader stopwords"
        ) from error
    return _nltk_stopwords


def _calculate_languages_ratios(
    text: str,
    stopwords_provider=None,
    tokenizer: Optional[Callable[[str], Iterable[str]]] = None,
) -> Dict[str, int]:
    """Return the number of unique stopwords matched for each language."""
    provider = stopwords_provider or _default_stopwords_provider()
    tokenize = tokenizer or _default_tokenizer()
    words = {word.lower() for word in tokenize(text or "")}

    languages_ratios = {}
    for language in provider.fileids():
        language_stopwords = {word.lower() for word in provider.words(language)}
        languages_ratios[language] = len(words.intersection(language_stopwords))

    return languages_ratios


def detect_language(
    text: str,
    stopwords_provider=None,
    tokenizer: Optional[Callable[[str], Iterable[str]]] = None,
) -> Optional[str]:
    """Return the highest-scoring language, or ``None`` when no stopwords match."""
    ratios = _calculate_languages_ratios(text, stopwords_provider, tokenizer)
    if not ratios:
        return None

    most_rated_language = max(ratios, key=ratios.get)
    if ratios[most_rated_language] <= 0:
        return None

    return most_rated_language


if __name__ == "__main__":
    try:
        print(detect_language(DEFAULT_SAMPLE))
    except MissingNltkError as error:
        print(error, file=sys.stderr)
        raise SystemExit(1)
