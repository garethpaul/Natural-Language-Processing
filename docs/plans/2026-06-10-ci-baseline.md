# Natural Language Processing CI Baseline

status: completed

## Context

The stopword detector has deterministic unit tests and a static baseline through
`make check`. Hosted CI repeats that same gate for pushes and pull requests
without downloading corpora or using private text.

## Changes

- Added `.github/workflows/check.yml` for GitHub Actions.
- Pinned checkout and Python setup actions.
- Disabled persisted checkout credentials.
- Installed `requirements.txt` through the reviewed `constraints.txt` graph on
  Python 3.12.
- Ran `python -m pip check` and `make check` in the hosted workflow.
- Kept the workflow limited to read-only contents permissions.

## Verification

- `make check`
- `git diff --check`
- Hosted push and pull-request baseline checks on the stack branches
