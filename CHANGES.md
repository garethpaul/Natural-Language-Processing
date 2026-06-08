# Changes

## 2026-06-08

- Ported the stopword language detector to Python 3.
- Added injectable stopword/tokenizer dependencies for deterministic tests.
- Reported missing NLTK stopword corpus setup without dumping a traceback.
- Returned `None` for empty or unsupported text instead of forcing a language.
- Added `requirements.txt`, unit tests, and a local `make check` gate.
- Documented private-text handling and dependency verification in the security policy.
