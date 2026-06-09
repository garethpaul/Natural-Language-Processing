# Stopword Entry Normalization

status: completed

## Context

Text tokens are normalized before stopword scoring, but stopword entries loaded
from injected providers or corpora were only lowercased. Whitespace-padded or
blank entries could drift from the checked-in stopword loader behavior and
change evidence unexpectedly.

## Objectives

- Strip and lowercase stopword entries from every loader path.
- Ignore blank stopword entries.
- Preserve explicit empty stopword mappings as no-evidence inputs.
- Add fixture coverage for noisy provider stopword data.
- Extend the static baseline and docs for stopword entry normalization.

## Verification

- `make check`
- `python3 -m unittest discover -s tests`
- `python3 scripts/check-baseline.py`
- `git diff --check`
