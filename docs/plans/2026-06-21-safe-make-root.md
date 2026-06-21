# Safe Make Root

## Problem

GNU Make list functions split absolute Makefile paths on whitespace. Because
`make check` invokes a recursive cleanup target, a malformed or caller-replaced
`MAKEFILE_LIST` value could redirect deletion outside the checkout.

## Change

- Derive the repository root from the raw, shell-quoted Makefile path.
- Remove GNU Make's leading list separator with POSIX shell-compatible tooling
  before resolving the directory.
- Reject non-file origins for the automatic `MAKEFILE_LIST` value.
- Dry-run cleanup, compilation, tests, and static checks from paths containing
  spaces and a literal apostrophe without executing deletion.

## Validation

- Run the Python unit suite and static baseline without creating bytecode.
- Verify hostile `MAKEFILE_LIST` overrides fail before a `find` recipe appears.
- Use hosted CI to run the complete clean, compile, test, and static sequence on
  every supported Python version.
