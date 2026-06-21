# Changes

## 2026-06-21

- Made absolute Makefile verification safe for checkout paths containing spaces
  or apostrophes and rejected `MAKEFILE_LIST` injection before cleanup.
- Added dry-run regression coverage that verifies cleanup remains rooted in the
  checkout without deleting files during the test.

## 2026-06-19

- Enabled NLTK strict path enforcement before tokenizer or corpus imports,
  removed NLTK 3.9.4's implicit temp-directory trust, bounded explicit data
  roots, and added hostile encoded-path, symlink, ZIP, and compatibility tests.
- Rejected mapping-shaped tokenizer output, stopword collections, and provider
  language collections before iteration so mapping keys cannot become evidence.
- Integrated the read-only hosted CI ownership contract with CODEOWNERS, agent
  guidance, and a completed CI baseline plan.

## 2026-06-17

- Added a provider language collection type guard so malformed scalar
  `fileids()` results become empty evidence instead of language identifiers.

## 2026-06-16

- Added a scalar stopword collection type guard so malformed strings and bytes
  become empty evidence instead of being iterated as stopword entries.
- Added a stopword provider invocation failure guard so `fileids()` and
  `words()` errors discard all provider evidence without leaking diagnostics.

## 2026-06-15

- Discarded all partial language evidence when explicit stopword mapping
  enumeration fails instead of leaking diagnostics or retaining order-dependent data.
- Discarded partial stopword evidence when explicit or provider collections fail
  during iteration.
- Added a tokenizer output type guard so scalar and non-iterable return values
  become empty evidence instead of raising or being split into characters.
- Added a tokenizer iteration failure guard so failed generators discard
  partial language evidence and return `unknown`.
- Added a tokenizer invocation failure guard so provider call errors become
  empty evidence instead of leaking diagnostics or aborting detection.
- Added a token entry type guard so non-string injected tokenizer output is
  ignored before string normalization instead of raising.
- Expanded stopword entry type guard coverage to include bytes and arbitrary
  object values on both explicit mapping and provider paths.

## 2026-06-14

- Added a stopword entry type guard so non-string provider and explicit values
  are ignored before normalization instead of raising.

## 2026-06-13

- Made cleanup, compilation, tests, static checks, and recursive verification
  resolve from the checkout for absolute Makefile invocations.
- Added a language label control character guard so newline and terminal escape
  labels cannot become detector or CLI output.

## 2026-06-12

- Added `constraints.txt` for the reviewed five-package Python 3.12 graph,
  applied it to hosted installation and caching, and documented that exact
  versions reduce resolver drift but do not authenticate package artifacts.

## 2026-06-10

- Added bounded detector text validation at 100,000 characters before
  tokenization, with generic type and size errors.
- Added language label validation so non-string and non-alphabetic stopword
  mapping keys cannot become detector outputs.
- Added pinned, read-only Python 3.12 hosted validation for dependency
  installation, `pip check`, and deterministic local tests.
- Added language label normalization so caller-provided and provider-loaded
  stopword mappings strip and lowercase language names while merging duplicate
  normalized labels.

## 2026-06-09

- Ignored punctuation-only tokens before stopword scoring so fallback symbols do not create language evidence.
- Returned `unknown` for near-tie stopword scores that do not clear the minimum margin.
- Preserved explicit empty stopword mappings as no-evidence inputs instead of falling back to default corpora.
- Returned `unknown` for sparse stopword evidence embedded in mostly unrelated text.
- Added stopword entry normalization so provider stopwords are stripped,
  lowercased, and blank entries are ignored before scoring.
- Added text token normalization so tokenizer output is stripped and lowercased
  before stopword scoring.
- Added explicit stopword set normalization so caller-provided stopword mappings
  follow the same strip/lowercase rules as provider-loaded stopwords.
- Added `make lint` and `make build` aliases alongside `make test` and
  `make check` for consistent local verification.

## 2026-06-08

- Ported the stopword language detector to Python 3.
- Added injectable stopword/tokenizer dependencies for deterministic tests.
- Added a fallback to the checked-in English stop-word list when NLTK corpora are absent.
- Returned `unknown` for empty, unsupported, or single-stopword evidence instead of forcing a language.
- Returned `unknown` for ambiguous tied stopword evidence instead of relying on mapping order.
- Added `requirements.txt`, unit tests, and a local `make check` gate.
- Documented private-text handling and dependency verification in the security policy.
