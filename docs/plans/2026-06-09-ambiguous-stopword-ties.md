# Ambiguous Stopword Tie Handling

Date: 2026-06-09

status: completed

## Context

The detector chooses the language with the highest stopword overlap. When two
languages have the same highest score, Python's mapping order determines the
result, which makes ambiguous multilingual input look more certain than it is.

## Objectives

- Preserve clear single-language detection.
- Return `unknown` when multiple languages tie for the strongest stopword
  evidence.
- Add fixture coverage for ambiguous multilingual input.
- Keep the behavior documented in the static baseline.

## Verification

- `make check`
- `python3 -m unittest discover -s tests`
- `python3 scripts/check-baseline.py`
- `git diff --check`
