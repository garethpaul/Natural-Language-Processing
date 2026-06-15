# Ignore Non-String Tokenizer Entries

status: completed

## Problem

The detector accepts injected tokenizers for deterministic tests and alternate
tokenization strategies. `_normalise_tokens` currently calls `.strip()` on
every yielded value, so one `None`, bytes value, or arbitrary object raises an
`AttributeError` instead of being ignored like malformed stopword entries.

## Requirements

- Ignore non-string tokenizer entries before string normalization.
- Preserve trimming, lowercasing, alphabetic filtering, uniqueness, density,
  score, tie, and margin behavior for valid string tokens.
- Cover mixed valid strings, blanks, punctuation, `None`, numeric, bytes, and
  arbitrary object values through both ratio calculation and detection.
- Add mutation-sensitive portable checker contracts and maintenance guidance.
- Do not change stopword loading, language-label validation, dependencies, or
  scoring thresholds.

## Implementation Units

### U1: Token entry boundary

Files:

- `language_detection.py`

Apply the existing string-only normalization boundary before calling string
methods on tokenizer output.

### U2: Regression coverage

Files:

- `tests/test_language_detection.py`

Add a mixed tokenizer fixture and prove malformed entries are ignored while
valid normalized tokens still select English.

### U3: Contracts and evidence

Files:

- `scripts/check-baseline.py`
- `README.md`
- `SECURITY.md`
- `VISION.md`
- `CHANGES.md`
- `docs/plans/2026-06-15-token-entry-type-guard.md`

Require the production type guard, regression path, completed verification,
and maintainer guidance.

## Verification

- Run the focused regression, the full offline suite, every non-destructive
  Make gate, and the rooted canonical gate from an external directory.
- Reject isolated mutations that remove the type guard, coerce malformed
  entries, weaken ratio or detection assertions, remove guidance, or reopen
  the plan.
- Audit checker compilation, the exact diff, generated artifacts, credential
  patterns, conflict markers, binaries, large files, and intended paths.

## Risks

- Injected tokenizers remain responsible for returning a finite iterable.
- Silently ignoring malformed entries matches stopword normalization and keeps
  errors independent of attacker-controlled object representations.
- The stacked base pull request must remain available and merge first.

## Work Completed

- Added a string-only boundary before tokenizer entries reach string methods.
- Added a mixed tokenizer fixture covering valid strings, blanks, punctuation,
  `None`, numeric, bytes, and arbitrary object values.
- Covered both ratio calculation and final language detection.
- Extended checker contracts and maintainer guidance.

## Verification Completed

- The focused regression and all 22 offline tests passed.
- All four Make gates passed from the checkout with broad cleanup explicitly
  disabled; the same non-destructive canonical gate passed from an external directory.
- Six isolated hostile mutations were rejected: missing type guard, coercion,
  weakened ratio and detection assertions, missing guidance, and stale plan status.
- Checker compilation, `git diff --check`, and exact intended-path,
  generated-artifact, secret-pattern, conflict-marker, binary, and large-file
  audits passed.
- No NLTK corpus download, network access, or private text was used.
