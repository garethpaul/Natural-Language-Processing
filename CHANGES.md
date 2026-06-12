# Changes

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
