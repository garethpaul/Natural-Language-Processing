---
title: Stopword Collection Type Guard
status: completed
date: 2026-06-16
---

# Stopword Collection Type Guard

## Priority

P1 correctness and reliability. A malformed stopword provider can return a
scalar string or bytes value where a collection is expected. Strings can create
character-level stopword evidence, while bytes are needlessly iterated before
their integer entries are discarded.

## Problem

`_normalise_stopwords()` validates iteration failures and individual entry
types, but it does not reject scalar `str` or `bytes` collections before
iteration. This differs from tokenizer-output normalization and lets malformed
provider or explicit mapping strings create character-level language evidence.

## Approach

- Reject scalar `str` and `bytes` stopword collections before requesting an
  iterator.
- Preserve valid iterable normalization, malformed-entry filtering, and
  all-or-nothing iteration failure behavior.
- Add executable coverage for explicit mappings and provider-loaded stopwords.
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
- `docs/plans/2026-06-16-stopword-collection-type-guard.md`

## Verification

- First prove scalar strings currently produce character-level evidence.
- Cover both explicit mapping and provider paths with `str` and `bytes`
  collections.
- Run focused tests, the complete offline suite, every repository Make gate,
  and the absolute-Makefile external-directory gate.
- Reject isolated guard, test, checker, guidance, changelog, and completed-plan
  mutations.
- Audit the exact diff, generated artifacts, credentials, conflict markers,
  binaries, large files, and whitespace.

## Scope Boundaries

- Do not change tokenization, scoring thresholds, language labels, valid
  stopword entry normalization, dependencies, CLI output, or workflow shape.
- Do not download NLTK corpora or contact a network provider.
- Keep PR #14 and its predecessors open and retain base-first stack ordering.

## Success Criteria

- Scalar `str` and `bytes` stopword collections produce no language evidence.
- Valid iterable stopword collections retain their existing behavior.
- Provider and explicit mapping paths enforce the same collection boundary.

## Verification Completed

- The focused scalar-collection regression passed for explicit mappings and
  provider-loaded `str` and `bytes` values.
- The complete suite confirmed that 31 offline tests passed without a corpus
  download or network provider.
- Application, test, and checker sources compiled with bytecode disabled.
- Seven isolated hostile mutations were rejected across runtime guard removal,
  disabled guard behavior, bytes coverage, provider coverage, guidance,
  changelog evidence, and completed plan status.
- All repository Make gates and the absolute Makefile `check` gate from an
  external directory passed.
- Exact diff, generated-artifact, credential-pattern, conflict-marker, binary,
  large-file, and whitespace audits passed.
