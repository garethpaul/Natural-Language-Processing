# Hosted Python Validation

status: completed

## Context

The repository has a bounded NLTK dependency, deterministic unittest coverage,
Python compilation, and a canonical local gate, but no hosted validation.

## Priorities

1. Install and validate declared dependencies on Python 3.12.
2. Run the canonical `make check` gate on hosted Linux.
3. Enforce a pinned, read-only, bounded workflow from the baseline checker.
4. Keep private text, external services, and NLTK corpus downloads out of CI.

## Implementation Units

Files:

- `.github/workflows/check.yml`
- `scripts/check-baseline.py`
- `README.md`
- `VISION.md`
- `SECURITY.md`
- `CHANGES.md`

Add push, pull-request, and manual triggers; read-only permissions; concurrency
cancellation; a bounded `ubuntu-24.04` job; commit-pinned checkout and Python
setup; dependency caching; requirements installation; `pip check`; and
`make check`. Require that contract from the baseline checker.

## Verification

- `make lint`
- `make test`
- `make build`
- `make check`
- workflow YAML parse
- `git diff --check`
- successful hosted Linux `Check` workflow for the pushed commit

## Boundaries

- Do not provide or upload private text.
- Do not download NLTK corpora or contact external services in CI.
