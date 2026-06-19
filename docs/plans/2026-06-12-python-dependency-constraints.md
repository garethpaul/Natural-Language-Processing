---
title: Python Dependency Constraints
date: 2026-06-12
status: completed
execution: code
---

# Python Dependency Constraints

## Context

`requirements.txt` intentionally exposes the supported NLTK 3.x compatibility
range, but the Python 3.12 workflow resolved NLTK and its transitive packages
afresh on every run. The same commit could therefore receive a different
dependency graph as new compatible releases appeared.

## Priorities

1. Preserve the public `nltk>=3.8,<4` compatibility range.
2. Add one reviewed constraints artifact for the complete Python 3.12 graph.
3. Apply the constraints artifact to hosted installation and pip caching.
4. Make the dependency-free checker reject graph, workflow, documentation,
   and completed-evidence drift.
5. Document that exact versions reduce resolver drift but do not authenticate
   downloaded package artifacts.

## Implementation Units

### Dependency Graph

Files:

- `requirements.txt`
- `constraints.txt`

Keep NLTK as public compatibility metadata and record every direct and
transitive package selected by a clean Python 3.12 resolution in
`constraints.txt`.

### Hosted Installation

File: `.github/workflows/check.yml`

Apply the constraints file to the sole dependency installation and include
both dependency files in setup-python's pip cache key. Preserve the pinned,
read-only, timeout-bounded workflow and both canonical events. Explicitly
disable checkout credential persistence.

### Static Contract And Documentation

Files:

- `scripts/check-baseline.py`
- `README.md`
- `SECURITY.md`
- `VISION.md`
- `CHANGES.md`
- `docs/plans/2026-06-12-python-dependency-constraints.md`

Require the exact reviewed graph, compatibility range, constrained install,
cache inputs, documentation boundary, completed status, and exact verification
evidence. Keep the checker dependency-free.

## Verification

- Resolve the compatibility range for Python 3.12 and confirm the complete
  exact graph.
- Verify selected releases against official PyPI metadata.
- Install through `requirements.txt` and `constraints.txt`, then run
  `python -m pip check`.
- Run `make lint`, `make test`, `make build`, and `make check`.
- Exercise hostile mutations for graph, range, install, cache, checkout,
  documentation, and stale-plan-evidence drift.
- Run Python compilation and `git diff --check`.
- Require successful push, pull-request, and CodeQL checks on the exact final
  head before tracker reconciliation.

## Boundaries

- Do not change detector, tokenizer, stopword, or scoring behavior.
- Do not narrow the public NLTK 3.x compatibility range.
- Do not claim hash-locked or offline-reproducible installation.
- Do not merge or close existing pull requests without explicit authorization.

## Work Completed

- Preserved `nltk>=3.8,<4` as public compatibility metadata and added the
  reviewed five-package Python 3.12 graph in `constraints.txt`.
- Applied the constraints graph to the sole hosted installation and included
  both dependency files in the pip cache key.
- Disabled checkout credential persistence explicitly and extended the
  dependency-free checker to enforce the exact dependency and workflow shape.
- Updated setup, security, vision, and change guidance without changing
  detector runtime behavior.

## Verification Completed

- Official PyPI metadata verified non-yanked release artifacts and compatible
  Python metadata for all five selected packages.
- Resolver dry runs for Python 3.10 and 3.12 selected the same exact graph
  recorded in `constraints.txt`; the selected packages declare Python 3.10 or
  older as their minimum supported runtime.
- An isolated Python 3.12.8 environment installed through `requirements.txt`
  and `constraints.txt`; isolated-mode `python -I -m pip check` reported no
  broken requirements.
- `pip-audit -r constraints.txt --no-deps` reported no known vulnerabilities.
- `make lint`, `make test`, `make build`, and `make check` passed with all 18
  offline tests.
- Focused hostile mutations for constraints, compatibility range, install,
  cache, checkout, documentation, and stale plan evidence were rejected.
- Python checker compilation and `git diff --check` passed.
