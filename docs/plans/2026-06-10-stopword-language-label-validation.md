# Stopword Language Label Validation

status: completed

## Problem

Language label normalization currently stringifies arbitrary mapping keys.
Values such as `None` and numeric IDs can therefore become detector output
labels even though they are not language names.

## Scope

- Accept only string language labels.
- Require at least one alphabetic character after trimming and lowercasing.
- Preserve valid normalized labels, including labels with spaces or hyphens.
- Ignore invalid labels before merging stopword sets or scoring text.
- Add deterministic tests and mutation-sensitive static guardrails.

## Verification

- `make lint`
- `make test`
- `make build`
- `make check`
- mutation checks for non-string and non-alphabetic label rejection
- `git diff --check`

## Work Completed

- Rejected non-string language labels before normalization.
- Required normalized labels to contain at least one alphabetic character.
- Preserved valid normalized labels and duplicate-label merging.
- Added deterministic custom-mapping tests for `None`, numeric, symbol-only,
  and valid labels.
- Extended baseline and documentation guardrails for the output-label contract.
