# Tokenizer Iteration Failure Guard

Status: completed

## Problem

`_normalise_tokens` validates that tokenizer output is iterable, but an iterator
can still raise after yielding partial tokens. The detector currently propagates
that provider exception after accumulating partial evidence, making malformed
tokenizer behavior observable and potentially inconsistent.

## Scope

- Consume tokenizer iterators behind a stable fail-closed boundary.
- Return empty token evidence when iteration raises before completion.
- Discard partial tokens from a failed iterator.
- Preserve text validation, scalar-output rejection, token entry filtering,
  stopword scoring, and successful tokenizer behavior.
- Add executable regression coverage, mutation-sensitive contracts, and
  synchronized guidance.

## Verification

- Run focused tests, full offline discovery, checker compilation, and all four
  Make gates from the repository plus the canonical external-directory check.
- Reject isolated mutations for uncaught iteration, partial-evidence retention,
  weakened ratio/detection coverage, missing guidance, and stale plan status.
- Audit the exact diff, generated artifacts, credential patterns, dependency
  files, conflict markers, binaries, large files, and intended paths.

## Risks

- This boundary intentionally treats tokenizer iterator failure as no language
  evidence rather than exposing provider diagnostics.
- No NLTK corpus download, network provider, or private text will be used.
- The change must remain stacked on PR #9; neither pull request may be merged or
  closed without explicit owner authorization.

## Work Completed

- Wrapped tokenizer iterator consumption in a fail-closed boundary that returns
  an empty set and discards any partial tokens after an exception.
- Added ratio and final-detection coverage with a generator that yields valid
  stopwords before raising.
- Added mutation-sensitive contracts and synchronized guidance.

## Verification Completed

- All four Make gates passed from the repository and the canonical check passed
  from an external directory.
- 24 offline tests passed with no corpus download or network access.
- Six isolated hostile mutations were rejected for uncaught iteration, retained
  partial evidence, weakened ratio coverage, weakened detection coverage,
  missing guidance, and stale plan status.
- Checker compilation, exact diff, artifact, credential, dependency, conflict,
  binary, large-file, whitespace, and intended-path audits passed.
