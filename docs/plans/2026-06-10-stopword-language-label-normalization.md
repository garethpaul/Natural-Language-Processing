# Stopword Language Label Normalization

status: completed

## Context

Stopword mappings already normalize their stopword entries before scoring, but
caller-provided and provider-loaded language labels can still include casing or
padding differences. That can split evidence across labels such as `English`
and ` english `, creating false ambiguity or returning noisy labels.

## Objectives

- Strip and lowercase caller-provided and provider-loaded language labels
  before scoring.
- Skip blank normalized language labels.
- Merge stopword entries when multiple labels normalize to the same language.
- Extend tests, docs, and the active baseline checker for the new behavior.

## Verification

- `make test`
- `make check`
- `git diff --check`
