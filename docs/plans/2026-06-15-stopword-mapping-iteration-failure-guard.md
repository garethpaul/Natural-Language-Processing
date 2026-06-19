---
title: Stopword Mapping Iteration Failure Guard
type: reliability
status: completed
date: 2026-06-15
execution: code
---

# Stopword Mapping Iteration Failure Guard

## Problem

`_normalise_stopword_sets` consumes an explicit mapping's `items()` iterator
without an exception boundary. A custom mapping can yield one language and then
raise, leaking provider diagnostics and aborting detection after partial
language evidence has already been accumulated.

## Approach

- Consume mapping entries behind one fail-closed boundary.
- Discard all partial language evidence if mapping enumeration raises.
- Preserve language-label merging, per-language stopword normalization,
  tokenizer behavior, scoring, and checked-in fallback data.
- Add focused ratio and detection regressions plus mutation-sensitive source,
  guidance, and completed-plan contracts.

## Files

- `language_detection.py`
- `tests/test_language_detection.py`
- `scripts/check-baseline.py`
- `README.md`
- `SECURITY.md`
- `VISION.md`
- `CHANGES.md`
- `docs/plans/2026-06-15-stopword-mapping-iteration-failure-guard.md`

## Verification

- Run focused regressions, the full offline suite, all Make gates, and the
  location-independent external-directory gate.
- Reject isolated exception-boundary, partial-evidence, test, guidance, and
  plan-status mutations.
- Audit the exact diff, generated artifacts, credentials, conflicts, binaries,
  large files, modes, and whitespace.

## Risks

- A mapping enumeration failure intentionally produces no stopword evidence
  instead of retaining a partial language set or exposing diagnostics.
- No NLTK corpus download, network provider, or private text will be used.
- Keep this change stacked on PR #12; do not merge or close stacked pull
  requests without explicit authorization.

## Status: Completed

## Work Completed

- Consume explicit stopword mapping entries behind one fail-closed boundary.
- Discard all partially normalized languages when mapping enumeration raises.
- Add ratio, detection, source, guidance, and completed-plan contracts.

## Verification Completed

- All four Make gates passed from the repository, and `make check` passed from
  an external directory.
- 27 offline tests passed without corpus downloads or network access.
- Six isolated hostile mutations were rejected for retained partial evidence,
  narrowed exception handling, weakened ratio and detection assertions,
  missing guidance, and reopened plan status.
- Checker compilation, exact diff, artifact, credential, dependency, conflict,
  binary, large-file, mode, whitespace, and intended-path audits passed.
- No NLTK corpus download, network provider, or private text was used.
