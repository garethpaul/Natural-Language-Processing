# Language Detection Baseline Plan

Date: 2026-06-08

status: completed

## Context

`Natural-Language-Processing` is a compact Python/NLTK sample that detects
language by counting stopword overlap. The original script used Python 2 print
syntax, printed dependency errors at import time, and had no automated checks.

## Objectives

- Port the sample to Python 3 syntax.
- Keep NLTK as an explicit dependency while allowing tests to inject small
  stopword fixtures.
- Fall back to the checked-in English stop-word list when NLTK corpora are absent.
- Return `unknown` for empty, unsupported, or weak single-stopword input instead
  of claiming a language.
- Add automated tests for stopword ratios, clear detection, and no-match input.
- Add a local `make check` gate with compile, unit, and static baseline checks.

## Verification

- `make check`
- `python3 -m unittest discover -s tests`
- `python3 scripts/check-baseline.py`
- `git diff --check`
