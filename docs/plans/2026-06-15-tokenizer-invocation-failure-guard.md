# Tokenizer Invocation Failure Guard

Status: completed

## Problem

`_normalised_text_words` invokes the selected tokenizer outside the existing
token-iteration failure boundary. A tokenizer that raises before returning an
iterable leaks provider diagnostics and aborts both ratio calculation and final
detection instead of producing the detector's fail-closed unknown result.

## Scope

- Invoke the selected tokenizer behind a narrow exception boundary.
- Convert tokenizer invocation failure to empty token evidence without exposing
  provider exception text.
- Preserve text type/size validation, malformed-output rejection, iterator
  failure handling, token normalization, scoring, and successful tokenizers.
- Add executable regression coverage, mutation-sensitive contracts, and
  synchronized maintenance guidance.

## Files

- `language_detection.py`
- `tests/test_language_detection.py`
- `scripts/check-baseline.py`
- `README.md`
- `SECURITY.md`
- `VISION.md`
- `CHANGES.md`
- `docs/plans/2026-06-15-tokenizer-invocation-failure-guard.md`

## Verification

- Run the focused invocation-failure regression, full offline tests, checker
  compilation, all four Make gates, and the external-directory check.
- Reject isolated mutations for uncaught invocation, weakened ratio/detection
  assertions, ordering drift, missing guidance, and stale plan status.
- Audit the exact diff, dependencies, generated artifacts, credentials,
  conflicts, binaries, large files, modes, and whitespace.

## Risks

- Provider invocation failures intentionally become no language evidence rather
  than caller-visible diagnostics.
- No NLTK corpus download, network provider, or private text will be used.
- The change must remain stacked on PR #10; neither pull request may be merged
  or closed without explicit owner authorization.

## Success Criteria

- A tokenizer that raises before returning produces zero ratios and `unknown`.
- Text validation still runs before tokenizer selection and invocation.
- Existing malformed-output, iterator-failure, and successful-tokenizer behavior
  remains unchanged.

## Work Completed

- Wrapped tokenizer selection and invocation in a fail-closed exception boundary
  after text validation and before output normalization.
- Added ratio and final-detection coverage for a tokenizer that raises before
  returning an iterable.
- Added mutation-sensitive contracts and synchronized maintenance guidance.

## Verification Completed

- All four Make gates passed from the repository and the canonical check passed
  from an external directory.
- 25 offline tests passed with no corpus download or network access.
- Seven isolated hostile mutations were rejected for uncaught invocation,
  ordering drift, weakened ratio coverage, weakened detection coverage, missing
  guidance, and stale plan status.
- Checker compilation, exact diff, artifact, credential, dependency, conflict,
  binary, large-file, mode, whitespace, and intended-path audits passed.
