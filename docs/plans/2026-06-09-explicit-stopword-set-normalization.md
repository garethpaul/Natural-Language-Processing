# Explicit Stopword Set Normalization

status: completed

## Context

Stopwords loaded from providers are stripped, lowercased, and filtered for blank
entries before scoring. Explicit `stopword_sets` passed into
`detect_language` or `_calculate_languages_ratios` bypassed that normalization,
so custom mappings could behave differently from provider-loaded mappings.

## Objectives

- Normalize explicit stopword-set mappings before scoring.
- Preserve explicit empty stopword mappings as no evidence.
- Keep provider-loaded stopword behavior unchanged.
- Add offline coverage for mixed-case, padded, and blank explicit stopword
  entries.
- Extend the static baseline and docs for the public custom stopword path.

## Verification

- `make lint`
- `make test`
- `make build`
- `make check`
- `git diff --check`
