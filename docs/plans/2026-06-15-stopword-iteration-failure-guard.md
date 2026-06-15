---
title: Stopword Iteration Failure Guard
type: reliability
status: completed
date: 2026-06-15
execution: code
---

# Stopword Iteration Failure Guard

## Problem

`_normalise_stopwords` iterates explicit and provider-backed stopword collections
without an exception boundary. A collection can yield partial entries and then
raise, leaking provider diagnostics and aborting detection instead of treating
that language as having no trustworthy stopword evidence.

## Approach

- Acquire and consume each stopword iterable behind one fail-closed boundary.
- Discard the affected language's partial normalized entries if iteration fails.
- Preserve valid stopword normalization, malformed-entry filtering, language
  labels, tokenizer behavior, scoring, and checked-in fallback data.
- Add ratio and detection regressions plus mutation-sensitive source, guidance,
  and completed-plan contracts.

## Files

- `language_detection.py`
- `tests/test_language_detection.py`
- `scripts/check-baseline.py`
- `README.md`
- `SECURITY.md`
- `VISION.md`
- `CHANGES.md`
- `docs/plans/2026-06-15-stopword-iteration-failure-guard.md`

## Verification

- Run the focused failure regression, full offline tests, checker compilation,
  all Make gates, and external-directory verification.
- Reject isolated exception-boundary, partial-evidence, test, guidance, and plan
  mutations.
- Audit the exact diff, dependencies, generated artifacts, credentials,
  conflicts, binaries, large files, modes, and whitespace.

## Risks

- A failed stopword collection intentionally contributes no evidence for its
  language instead of exposing provider diagnostics.
- No NLTK corpus download, network provider, or private text will be used.
- Keep this change stacked on PR #11; do not merge or close stacked pull
  requests without explicit authorization.

## Status: Completed

## Work Completed

- Acquire and consume every explicit or provider-backed stopword iterable behind
  one fail-closed normalization boundary.
- Discard the affected language's partial normalized entries when iterator
  acquisition or iteration raises while preserving other language evidence.
- Add ratio, detection, source, guidance, and completed-plan contracts.

## Verification Completed

- All four Make gates passed from the repository, and `make check` passed from
  an external directory.
- 26 offline tests passed without corpus downloads or network access.
- Six isolated hostile mutations were rejected for uncaught iteration, retained
  partial evidence, weakened ratio and detection assertions, missing guidance,
  and reopened plan status.
- Checker compilation, exact diff, artifact, credential, dependency, conflict,
  binary, large-file, mode, whitespace, and intended-path audits passed.
- No NLTK corpus download, network provider, or private text was used.
