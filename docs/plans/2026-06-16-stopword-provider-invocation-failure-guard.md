---
title: Stopword Provider Invocation Failure Guard
status: planned
date: 2026-06-16
---

# Stopword Provider Invocation Failure Guard

## Priority

P1 reliability and diagnostic privacy. Stopword-provider failures currently
escape before the all-or-nothing normalization boundary, aborting detection and
potentially exposing provider exception detail.

## Problem

`load_stopword_sets()` invokes `fileids()` and `words(language)` inside mapping
comprehensions. Explicit provider exceptions are not handled, while the default
NLTK path handles only a missing-corpus `LookupError`. Invocation failures
therefore bypass the existing mapping and iterable failure guards.

## Approach

- Isolate provider enumeration and per-language word retrieval behind one
  all-or-nothing loader.
- Return empty stopword evidence when an explicit provider raises during either
  invocation, allowing detection to return `unknown` without retaining partial
  languages or exposing diagnostics.
- Preserve the checked-in English fallback when the optional default NLTK
  corpus reports `LookupError`.
- Return empty evidence for other unexpected default-provider failures rather
  than substituting English evidence after a broken provider response.
- Add executable tests, mutation-sensitive baseline contracts, maintained
  guidance, changelog, and completed verification evidence.

## Files

- `language_detection.py`
- `tests/test_language_detection.py`
- `scripts/check-baseline.py`
- `README.md`
- `SECURITY.md`
- `VISION.md`
- `CHANGES.md`
- `docs/plans/2026-06-16-stopword-provider-invocation-failure-guard.md`

## Verification

- Cover `fileids()` and `words(language)` failures on the explicit provider
  path, including partial provider output before failure.
- Preserve the existing default-corpus `LookupError` fallback contract.
- Run the focused provider tests, complete offline suite, every repository Make
  gate, and the absolute-Makefile external-directory gate.
- Reject isolated provider-call, partial-evidence, guidance, changelog, and
  completed-plan mutations.
- Audit the exact diff, generated artifacts, credentials, conflict markers,
  binaries, large files, and whitespace.

## Scope Boundaries

- Do not change tokenization, scoring thresholds, label normalization, stopword
  entry normalization, dependencies, CLI output, or hosted workflow shape.
- Do not download NLTK corpora or contact a network provider.
- Keep PR #13 and its predecessors open and retain base-first stack ordering.

## Success Criteria

- Provider invocation failures cannot raise through ratio calculation or
  detection and cannot preserve partial language evidence.
- Explicit provider failures produce empty ratios and `unknown` detection.
- A missing optional default NLTK corpus still uses the checked-in English
  stopword list.
