# Natural Language Processing CI Baseline

status: completed

## Context

The stopword detector already has deterministic unit tests and a static
baseline through `make check`. The missing maintenance guard was hosted CI that
repeats that same gate for pushes and pull requests.

## Changes

- Added `.github/workflows/check.yml` for GitHub Actions.
- Installed `requirements.txt` on Python 3.12.
- Ran `make check` in the hosted workflow.
- Extended the baseline checker and docs so hosted CI stays part of the
  maintained project contract.

## Verification

- `make check`
- `git diff --check`
