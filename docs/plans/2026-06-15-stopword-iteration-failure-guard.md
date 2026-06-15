---
title: Stopword Iteration Failure Guard
type: reliability
status: in_progress
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

## Status: In Progress
