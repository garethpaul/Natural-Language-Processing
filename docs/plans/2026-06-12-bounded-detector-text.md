# Bounded Detector Text

status: completed

## Context

The detector passes caller text directly to NLTK or an injected tokenizer.
Library and CLI callers can therefore supply arbitrarily large strings and
drive unbounded tokenization work before any scoring guard applies.

## Priorities

1. Accept at most 100,000 text characters before tokenization.
2. Reject non-string text with a generic field-level error.
3. Preserve the existing `None`-as-empty behavior and normal scoring semantics.
4. Prove oversized text never reaches an injected tokenizer.

## Implementation Units

### Shared Text Boundary

File: `language_detection.py`

Validate and bound text in `_normalised_text_words`, the shared entry point for
ratio calculation and language detection. Raise stable errors without echoing
private input content.

### Offline Tests

File: `tests/test_language_detection.py`

Cover the exact boundary, oversized rejection before tokenizer invocation,
non-string rejection, and retained `None` behavior.

### Static Contract And Documentation

Files:

- `scripts/check-baseline.py`
- `README.md`
- `SECURITY.md`
- `VISION.md`
- `CHANGES.md`
- `docs/plans/2026-06-12-bounded-detector-text.md`

Protect the pre-tokenization ordering and document the private-text error
boundary.

## Verification

Completed locally on 2026-06-12:

- `python3 -m py_compile language_detection.py tests/test_language_detection.py scripts/check-baseline.py`
- focused detector tests (18 tests)
- `make lint`
- `make test` (18 tests)
- `make build`
- `make check`
- hostile mutations removing the size guard or moving validation after
  tokenization were each rejected by the static contract
- `git diff --check`

Hosted push and pull-request checks will be recorded after the branch is pushed.

## Boundaries

- Do not include input text in validation errors.
- Do not change stopword thresholds, density, tie, or margin semantics.
- Do not download NLTK corpora in tests or CI.
