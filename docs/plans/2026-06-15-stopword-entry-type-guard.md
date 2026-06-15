# Heterogeneous Stopword Entry Coverage

status: completed

## Context

The existing stopword entry type guard is terminal-green and covers `None` and
integer values on explicit mapping and provider paths. Bytes and arbitrary
objects are also non-string values, but those heterogeneous cases are not
represented directly in the maintained tests or static contract.

## Requirements

- Preserve the existing production type guard without changing detector logic.
- Cover bytes and arbitrary objects alongside valid strings, blanks, `None`,
  and numeric entries.
- Exercise both explicit mapping and injected provider loading paths.
- Add mutation-sensitive static contracts and a changelog record.
- Do not change scoring thresholds, tokenization, language-label validation, or
  dependency resolution.

## Implementation

1. Add mixed valid, blank, `None`, numeric, bytes, and object fixtures.
2. Verify both explicit mapping and provider loading paths continue scoring with
   only normalized valid strings.
3. Extend the checker with exact test-name and heterogeneous-value contracts.
4. Record that the existing production guard is unchanged.

## Verification

- Run focused normalization tests, the full offline suite, every
  non-destructive Make gate, and the rooted canonical gate externally.
- Verify isolated mutations that remove the type guard, coerce invalid entries,
  restore direct `.strip()` access, remove mapping/provider coverage, remove
  guidance, or leave this plan incomplete are rejected.
- Run checker compilation plus exact diff, generated-artifact, secret-pattern,
  conflict-marker, binary, large-file, and intended-path audits.

## Risks

- The tests strengthen supported input coverage but do not add corpus diagnostics.
- The stacked base pull request must remain available and merge first.

## Work Completed

- Integrated the existing terminal-green stopword type guard and
  location-independent Makefile branch without changing production detector
  behavior.
- Added bytes and arbitrary object values to dedicated explicit mapping and
  provider regression paths.
- Added static contracts for both test paths and heterogeneous values.
- Recorded the incremental coverage in the changelog.

## Verification Completed

- Both focused heterogeneous-entry tests and all 21 offline tests passed.
- All four Make gates passed from the checkout with broad cleanup explicitly
  disabled; the same non-destructive canonical gate passed from an external directory
  through the absolute Makefile path.
- Six isolated hostile mutations were rejected: missing mapping coverage,
  missing provider coverage, missing bytes, missing arbitrary objects, missing
  production type guard, and stale plan status.
- Checker compilation and `git diff --check` passed. Exact intended-path,
  generated-artifact, secret-pattern, conflict-marker, binary, and large-file
  audits found no issues.
- No NLTK corpus download, network access, or private text was used.
