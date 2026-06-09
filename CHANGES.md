# Changes

## 2026-06-09

- Ignored punctuation-only tokens before stopword scoring so fallback symbols do not create language evidence.
- Returned `unknown` for near-tie stopword scores that do not clear the minimum margin.
- Preserved explicit empty stopword mappings as no-evidence inputs instead of falling back to default corpora.
- Returned `unknown` for sparse stopword evidence embedded in mostly unrelated text.

## 2026-06-08

- Ported the stopword language detector to Python 3.
- Added injectable stopword/tokenizer dependencies for deterministic tests.
- Added a fallback to the checked-in English stop-word list when NLTK corpora are absent.
- Returned `unknown` for empty, unsupported, or single-stopword evidence instead of forcing a language.
- Returned `unknown` for ambiguous tied stopword evidence instead of relying on mapping order.
- Added `requirements.txt`, unit tests, and a local `make check` gate.
- Documented private-text handling and dependency verification in the security policy.
