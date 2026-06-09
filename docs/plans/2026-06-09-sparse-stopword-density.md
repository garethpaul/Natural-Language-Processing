# Sparse Stopword Density Plan

status: completed

## Context

The detector requires a minimum stopword count and margin, but two common words
embedded in a much longer unrelated string can still satisfy those absolute
thresholds. That overstates confidence for synthetic, noisy, or mostly
out-of-language input.

## Objectives

- Preserve clear language detection when stopwords are a meaningful share of the
  unique alphabetic tokens.
- Return `unknown` when the winning language only has sparse stopword evidence.
- Keep existing tie, near-tie, punctuation-only, and empty-mapping safeguards.
- Cover sparse stopword evidence in unit tests and the static baseline.

## Verification

- `make check`
- `python3 -m unittest discover -s tests`
- `python3 scripts/check-baseline.py`
- `git diff --check`
