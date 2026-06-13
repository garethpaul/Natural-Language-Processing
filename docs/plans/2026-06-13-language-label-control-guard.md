# Language Label Control Character Guard

status: completed

## Context

Caller-provided or provider-loaded stopword language labels can become detector
output and are printed by the CLI. Existing validation requires alphabetic
content but still accepts embedded newline or terminal escape controls.

## Requirements

- Reject normalized language labels containing non-printable control
  characters before merging or scoring stopword sets.
- Preserve ordinary printable labels, normalization, duplicate merging, and
  unknown-result behavior.
- Add focused tests, mutation-sensitive static contracts, documentation, and
  completed verification evidence.

## Scope Boundaries

- Do not download NLTK data, change token scoring thresholds, or add model-based
  language detection.

## Verification

- Run all Make gates, focused unit tests, Python compilation, hostile
  mutations, diff checks, artifact scans, and secret scans.

## Work Completed

- Rejected normalized language labels containing non-printable characters
  before stopword-set merging or scoring.
- Added focused newline and terminal escape cases while preserving printable
  labels, duplicate merging, and unknown-result behavior.
- Added mutation-sensitive static contracts and matching output-safety docs.

## Verification Completed

- `make lint`, `make test`, `make build`, and `make check` passed with nineteen
  offline tests.
- Focused unit tests, Python compilation, dependency constraint contracts, diff
  checks, artifact scans, and secret scans passed.
- Six hostile mutations covering the printable-label guard, newline case,
  escape case, focused test contract, documentation contract, and completed
  plan evidence were rejected.
