# Spaced Absolute Makefile Path Verification

status: completed

## Context

GNU Make list functions split a loaded absolute Makefile path at spaces. A
checkout path containing spaces, brackets, and an apostrophe redirected every
verification gate and broke the recursive cleanup invocation.

## Scope

1. Derive the checkout root from the complete `MAKEFILE_LIST` value.
2. Preserve the authoritative root against command-line and environment input.
3. Reject command-line or environment-preferred `MAKEFILE_LIST` overrides.
4. Exercise all eight Make aliases from an external working directory.

## Verification

- Root and external hostile-path gates passed on supported Python versions.
- All eight Make aliases retained the checkout with no override and with
  command-line or environment `ROOT` input.
- Both tested `MAKEFILE_LIST` override paths failed closed.
- Existing NLTK path-containment tests and dependency checks remained green.

## Risk And Rollback

This changes verification root discovery only. It does not alter language
detection, NLTK resource containment, dependency constraints, or alert policy.
