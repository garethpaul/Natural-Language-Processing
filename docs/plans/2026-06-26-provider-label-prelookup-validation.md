# Provider Label Pre-Lookup Validation

Status: Completed

## Problem

Provider labels were normalized only after every `provider.words(language)`
call. A blank, control-bearing, or otherwise invalid label could therefore
trigger a resource lookup and one provider exception discarded valid evidence
from all earlier languages.

## Decision

Normalize and validate each provider label before lookup. Skip invalid labels,
merge valid normalized duplicates, and retain fail-closed handling for genuine
provider invocation failures.

## Scope

- `language_detection.py`
- `tests/test_language_detection.py`
- `scripts/check-baseline.py`
- `README.md`, `SECURITY.md`, `VISION.md`, and `CHANGES.md`

## Verification

- The failing-first regression returned empty evidence because a blank label
  reached provider lookup and raised.
- Repository and external-directory `make check` passed all 54 offline tests.
- Three hostile mutations were rejected: lookup before validation, missing
  invalid-label skipping, and raw-label result keys.
- No NLTK downloads, private text, or live external resources were used.
