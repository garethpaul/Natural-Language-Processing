# Stopword Entry Type Guard

status: completed

## Summary

Ignore non-string stopword entries before normalization so malformed provider or
explicit data cannot crash language detection.

## Problem Frame

`_normalise_stopwords` calls `.strip()` on every entry. The public explicit
mapping path and injected provider path therefore raise `AttributeError` when a
collection contains `None`, numeric, bytes, or another non-string value, even
though invalid language labels are already ignored safely.

## Requirements

- Accept only string stopword entries and ignore other runtime types.
- Strip and lowercase each valid entry once, then ignore blank results.
- Preserve provider fallback, explicit mapping, token normalization, scoring,
  density, ambiguity, margin, and input-size behavior.
- Add runtime, static, documentation, and completed verification evidence.

## Key Technical Decisions

- Replace the set comprehension with an explicit loop so type validation and
  single-pass normalization remain clear.
- Treat invalid stopword entries as absent evidence rather than raising or
  coercing them to strings.

## Implementation Units

### U1: Guard stopword entry types

**Files:** `language_detection.py`, `tests/test_language_detection.py`

**Approach:** Add provider and explicit-mapping regressions first, then validate
entry type before normalization.

**Execution note:** Start with failing runtime tests.

**Test scenarios:**

- Provider collections containing valid strings plus `None` and integers load
  only normalized valid strings.
- Explicit mappings containing non-string entries score valid strings without
  raising or coercing invalid values.

**Verification:** Focused and full offline tests pass; removing the type guard
restores the original failure.

### U2: Protect and document the behavior

**Files:** `scripts/check-baseline.py`, `README.md`, `SECURITY.md`, `VISION.md`,
`CHANGES.md`, `docs/plans/2026-06-14-stopword-entry-type-guard.md`

**Approach:** Extend static contracts and maintained guidance for the new data
validation boundary.

**Test scenarios:**

- Targeted hostile mutations reject source, test, documentation, and plan drift.

**Verification:** All Make aliases, mutations, diff, artifact, and credential
audits pass.

## Scope Boundaries

- Do not coerce non-string values or expose them in errors.
- Do not change language label validation or detection thresholds.
- Do not require NLTK corpus or network access.

## Work Completed

- Replaced the stopword set comprehension with a single-pass loop that accepts
  strings, normalizes each once, and ignores all other runtime types.
- Added provider-loaded and explicit-mapping regression coverage for `None` and
  integer entries while preserving valid normalized values.
- Extended the static checker and maintained documentation with the entry-type
  boundary.

## Verification Completed

- `make lint`, `make test`, `make build`, and `make check` passed with nineteen
  offline tests, and the absolute Makefile check passed externally.
- Both focused regressions failed with `AttributeError` before implementation
  and passed after the type guard.
- Five hostile mutations covering source behavior, provider test, explicit test,
  documentation, and completed plan evidence were rejected.
- No NLTK corpus download, network access, or private text was used.
