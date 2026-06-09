# Make Gate Aliases Plan

status: completed

## Context

The repository already has a local `make check` gate with compile, unit-test,
and static baseline coverage. Fleet maintenance is easier when small projects
also expose the common `make lint`, `make test`, and `make build` aliases that
map to the same underlying checks.

## Objectives

- Add `make lint` as an alias for the static baseline checker.
- Add `make build` as an alias for Python compilation.
- Keep `make test`, `make verify`, and `make check` behavior unchanged.
- Document the alias set in the README, vision, security policy, changelog, and
  static baseline.

## Verification

- `make lint`
- `make test`
- `make build`
- `make check`
- `git diff --check`
