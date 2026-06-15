# Stopword Entry Type Guard

status: in progress

## Context

Stopword normalization calls `.strip()` on every provider or mapping entry.
Malformed corpus data containing `None`, numbers, bytes, or other non-string
values therefore raises before language scoring instead of being ignored.

## Requirements

- Ignore non-string stopword entries before stripping or lowercasing.
- Preserve normalization and deduplication for valid string entries.
- Apply the behavior consistently to explicit mappings, injected providers,
  NLTK corpora, and the checked-in fallback loader.
- Add focused mixed-entry tests, static contracts, and maintenance guidance.
- Do not change scoring thresholds, tokenization, language-label validation, or
  dependency resolution.

## Implementation

1. Add an explicit string type guard inside `_normalise_stopwords`.
2. Cover mixed valid, blank, `None`, numeric, bytes, and object entries.
3. Verify both explicit mapping and provider loading paths continue scoring with
   only normalized valid strings.
4. Extend the checker and project guidance with exact contracts.

## Verification

- Run focused normalization tests, the full offline suite, every
  non-destructive Make gate, and the rooted canonical gate externally.
- Verify isolated mutations that remove the type guard, coerce invalid entries,
  restore direct `.strip()` access, remove mapping/provider coverage, remove
  guidance, or leave this plan incomplete are rejected.
- Run checker compilation plus exact diff, generated-artifact, secret-pattern,
  conflict-marker, binary, large-file, and intended-path audits.

## Risks

- Invalid corpus entries are skipped rather than surfaced; operators should use
  corpus validation when malformed upstream data must be diagnosed.
- The stacked base pull request must remain available and merge first.

## Work Completed

- Pending implementation.

## Verification Completed

- Pending validation.
