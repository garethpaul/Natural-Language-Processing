# Language Label Control Character Guard

status: planned

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
