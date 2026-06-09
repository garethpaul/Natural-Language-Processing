# Punctuation Token Filter

Date: 2026-06-09

status: completed

## Context

The detector compares unique tokenizer outputs against stopword sets. The
checked-in fallback stopword list contains legacy social-text symbols such as
`-` and `&`, so punctuation-only text could create false stopword evidence.

## Objectives

- Preserve word-based stopword overlap behavior.
- Ignore tokens that contain no alphabetic characters before scoring language
  matches.
- Keep punctuation-only input classified as `unknown`.
- Add fixture coverage for punctuation-only fallback stopword matches.
- Extend the static baseline so future token changes keep this filter.

## Verification

- `make check`
- `python3 -m unittest discover -s tests`
- `python3 scripts/check-baseline.py`
- `git diff --check`
