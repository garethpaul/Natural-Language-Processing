---
title: Provider Language Collection Type Guard
status: planned
date: 2026-06-17
---

# Provider Language Collection Type Guard

## Priority

P1 correctness and reliability. A malformed stopword provider can return a
scalar string or bytes value from `fileids()`, causing the loader to iterate
characters or integers as if they were language identifiers.

## Problem

Provider invocation failures are contained, and provider language labels are
normalized before scoring, but `_load_provider_stopword_sets()` does not reject
scalar `fileids()` collections. A string such as `"english"` is therefore
expanded into one-character language buckets and can expose fabricated ratios.

## Approach

- Reject scalar `str` and `bytes` provider language collections before
  requesting an iterator.
- Preserve valid iterable providers, language-label normalization, stopword
  collection normalization, and all-or-nothing provider failure behavior.
- Add executable coverage for malformed scalar `fileids()` results.
- Extend the dependency-free checker, maintenance guidance, changelog, and
  completed verification evidence.

## Files

- `language_detection.py`
- `tests/test_language_detection.py`
- `scripts/check-baseline.py`
- `README.md`
- `SECURITY.md`
- `VISION.md`
- `CHANGES.md`
- `docs/plans/2026-06-17-provider-language-collection-type-guard.md`

## Verification

- First prove scalar provider language collections currently create malformed
  language-ratio buckets.
- Cover both `str` and `bytes` `fileids()` results while retaining valid list
  behavior.
- Run focused tests, the complete offline suite, every repository Make gate,
  and the absolute-Makefile external-directory gate.
- Reject isolated runtime, test, checker, guidance, changelog, and
  completed-plan mutations.
- Audit the exact diff, generated artifacts, credentials, conflict markers,
  binaries, large files, and whitespace.

## Scope Boundaries

- Do not change tokenization, scoring thresholds, language-label
  normalization, valid provider collections, dependencies, CLI output, or
  workflow shape.
- Do not download NLTK corpora or contact a network provider.
- Keep PR #15 and its predecessors open and retain base-first stack ordering.

## Success Criteria

- Scalar `str` and `bytes` provider language collections produce no language
  evidence.
- Valid iterable provider language collections retain their existing behavior.
- Ratio calculation and detection enforce the same provider boundary.

## Verification Completed

Pending implementation and bounded verification.
