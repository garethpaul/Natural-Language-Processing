# Text Token Normalization

status: completed

## Context

Stopword entries are stripped and lowercased before scoring, but text tokens
from an injected tokenizer were only lowercased. Whitespace-padded tokenizer
output could miss valid stopword matches even when the token text was otherwise
the same.

## Objectives

- Strip and lowercase text tokens before stopword scoring.
- Preserve punctuation-only token filtering.
- Preserve explicit empty stopword mappings and sparse-evidence safeguards.
- Add unit coverage and static baseline checks for padded tokenizer output.

## Verification

- `make test`
- `make check`
- `git diff --check`
