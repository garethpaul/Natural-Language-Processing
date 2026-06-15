# Tokenizer Iteration Failure Guard

Status: planned

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
