# Near-Tie Stopword Margin Plan

status: completed

## Context

The detector already returns `unknown` when the highest stopword score is tied. A one-stopword margin can still be weak evidence for short or mixed-language text.

## Objectives

- Require the winning language to clear a minimum stopword margin.
- Return `unknown` for near-tie scores.
- Preserve exact-tie and punctuation-only safeguards.
- Cover near-tie behavior in unit tests and the static baseline.

## Verification

- `python3 -m unittest discover -s tests`
- `python3 scripts/check-baseline.py`
- `make check`
- `git diff --check`
