# Tokenizer Output Type Guard

status: completed

## Problem

The token entry guard safely ignores malformed values yielded by a tokenizer,
but `_normalise_tokens` still assumes the tokenizer itself returns an iterable.
A `None`, numeric, bytes, plain string, or arbitrary scalar result either raises
before scoring or is incorrectly consumed as individual characters.

## Requirements

- Treat non-iterable tokenizer results as empty token evidence.
- Treat scalar string and bytes results as malformed collections rather than
  iterating their characters.
- Preserve valid lists, tuples, sets, generators, token normalization, density,
  score, tie, margin, and bounded-text behavior.
- Cover ratio calculation and final detection with mutation-sensitive tests.
- Add portable checker contracts and synchronized maintenance guidance.

## Non-Goals

- Catching exceptions raised while a valid tokenizer iterable is consumed.
- Changing stopword collection handling, language labels, dependencies, or
  scoring thresholds.
- Logging or coercing malformed tokenizer return values.

## Implementation

1. Reject string and bytes collection values before iteration.
2. Attempt `iter()` once and return an empty set when the result is not
   iterable.
3. Normalize only entries yielded by the validated iterator.
4. Extend tests, checker contracts, completed evidence, and project guidance.

## Verification

- Run the focused regression, full offline suite, every non-destructive Make
  gate, and the rooted canonical gate from an external directory.
- Reject isolated mutations that remove scalar rejection, remove the iterable
  guard, restore direct iteration, weaken ratio or detection assertions, remove
  guidance, or leave the plan incomplete.
- Audit checker compilation, exact paths, generated artifacts, credential
  patterns, conflict markers, binaries, large files, and dependencies.

## Risks

- A tokenizer may still raise while producing or consuming an otherwise valid
  iterable; this change only guards the returned collection shape.
- Malformed output becomes unknown language rather than an implementation error.
- The stacked base pull request must remain available and merge first.

## Work Completed

- Rejected scalar string and bytes tokenizer results before token iteration.
- Probed other tokenizer results with `iter()` and converted non-iterable values
  to empty token evidence without logging or coercion.
- Added ratio and final-detection coverage for `None`, integer, object, string,
  and bytes results while preserving valid iterable behavior.
- Extended checker contracts and synchronized maintainer guidance.

## Verification Completed

- The focused regression and all 23 offline tests passed.
- All four Make gates passed from the checkout with broad cleanup explicitly
  disabled; the same non-destructive canonical gate passed from an external directory.
- Seven isolated hostile mutations were rejected: missing scalar rejection,
  missing iterable guard, restored direct iteration, weakened ratio assertion,
  weakened detection assertion, missing guidance, and stale plan status.
- Checker compilation, `git diff --check`, and exact intended-path,
  generated-artifact, credential-pattern, conflict-marker, binary, large-file,
  and dependency audits passed.
- No NLTK corpus download, network access, or private text was used.
