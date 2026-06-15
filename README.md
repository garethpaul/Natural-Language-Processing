# Natural-Language-Processing

<!-- README-OVERVIEW-IMAGE -->
![Project overview](docs/readme-overview.svg)

## Overview

`garethpaul/Natural-Language-Processing` is a public sample, documentation, or utility project. NLTK via Python

This README is based on the checked-in source, manifests, scripts, and repository metadata on the `master` branch. The project language mix found during review was: Python (1).

## Repository Contents

- `README.md` - project overview and local usage notes
- `SECURITY.md` - security reporting and disclosure guidance
- `VISION.md` - project direction and maintenance guardrails

Additional scan context:

- Source directories: no top-level source directories detected
- Dependency and build manifests: none detected
- Entry points or build surfaces: none detected
- Test-looking files: no obvious test files detected

## Getting Started

### Prerequisites

- Git
- Python 3
- NLTK for running the sample against the built-in stopword corpus

### Setup

```bash
git clone https://github.com/garethpaul/Natural-Language-Processing.git
cd Natural-Language-Processing
python3 -m pip install -r requirements.txt -c constraints.txt
python3 -m nltk.downloader stopwords  # optional; falls back to stop_words.txt when absent
```

The setup commands above are derived from repository files. Legacy mobile, Python, or JavaScript samples may require older SDKs or package versions than a modern workstation uses by default.

`requirements.txt` keeps the supported NLTK 3.x compatibility range public,
while `constraints.txt` records the reviewed exact Python 3.12 graph used by
CI. These version constraints reduce resolver drift but do not authenticate
downloaded package artifacts or make installation offline-reproducible.

## Running or Using the Project

- Run `python3 language_detection.py` to detect the language of the checked-in
  sample text.
- Run `python3 language_detection.py "the quick example and you"` to classify
  your own short text.
- Import `detect_language` from `language_detection.py` for small experiments.
- Ambiguous tied stopword scores return `unknown` instead of choosing by mapping
  order.
- Near-tie stopword scores return `unknown` unless the winning language clears
  the minimum margin.
- Punctuation-only tokens are ignored before stopword scoring, so symbols alone
  do not create language evidence.
- Explicit empty stopword mappings stay empty and return `unknown` rather than
  falling back to the default corpus.
- Sparse stopword evidence in mostly unrelated text returns `unknown` unless the
  winning language has enough density across the unique alphabetic tokens.
- Stopword entry normalization strips and lowercases provider entries while
  ignoring blank lines before scoring.
- Text token normalization strips and lowercases tokenizer output before
  stopword scoring so padded tokens match corpus entries.
- Explicit stopword set normalization applies the same strip/lowercase rules to
  caller-provided stopword mappings before scoring.
- The stopword entry type guard ignores non-string provider and explicit values
  before normalization instead of raising or coercing them.
- The token entry type guard ignores non-string tokenizer output before string
  normalization and scoring.
- The tokenizer output type guard treats scalar strings, bytes, and
  non-iterable return values as empty evidence instead of iterating or raising.
- The tokenizer iteration failure guard discards partial evidence when a custom
  tokenizer raises while its returned iterator is being consumed.
- Language label normalization strips and lowercases caller-provided or
  provider-loaded language names, merging duplicate normalized stopword
  mappings before scoring.
- Language label validation ignores non-string or non-alphabetic mapping keys
  so sentinel values and numeric IDs cannot become detector outputs.
- The language label control character guard ignores labels containing newline,
  terminal escape, or other non-printable characters before scoring or CLI output.
- Bounded detector text accepts at most 100,000 characters before tokenization
  and rejects invalid types without echoing private input.

## Testing and Verification

- `make lint`
- `make test`
- `make build`
- `make check`
- The Make gates are location-independent. From another directory, pass the
  checkout's Makefile by absolute path, such as
  `make -f /path/to/Natural-Language-Processing/Makefile check`.
- `python3 -m unittest discover -s tests`
- `python3 scripts/check-baseline.py`
- Pinned `ubuntu-24.04` GitHub Actions installs `requirements.txt` through
  `constraints.txt`, runs
  `pip check`, and executes `make check` on Python 3.12 without private text,
  external service calls, or NLTK corpus downloads.

When the required SDK or runtime is unavailable, use static checks and source review first, then verify on a machine that has the matching platform toolchain.

## Configuration and Secrets

- No required secret or credential file was identified in the repository scan. If you add integrations later, keep secrets out of git.

## Security and Privacy Notes

- Review changes touching network requests, sockets, or service endpoints; examples from the scan include language_detection.py.

## Maintenance Notes

- The unit tests use small injected stopword fixtures, so they do not require
  downloading NLTK corpora.
- Use an absolute Makefile path when running the verification gates outside the
  checkout.
- If NLTK or its stopwords corpus is unavailable, the sample falls back to the
  checked-in English stop-word list and returns `unknown` for zero-score input.
- See `docs/plans/2026-06-09-ambiguous-stopword-ties.md` for the ambiguous
  stopword tie behavior.
- See `docs/plans/2026-06-09-near-tie-stopword-margin.md` for the near-tie
  stopword margin behavior.
- See `docs/plans/2026-06-09-punctuation-token-filter.md` for punctuation-only
  token filtering behavior.
- See `docs/plans/2026-06-09-empty-stopword-mapping.md` for explicit empty
  stopword mapping behavior.
- See `docs/plans/2026-06-09-sparse-stopword-density.md` for sparse stopword
  evidence handling.
- See `docs/plans/2026-06-09-stopword-entry-normalization.md` for stopword
  entry normalization behavior.
- See `docs/plans/2026-06-14-stopword-entry-type-guard.md` for stopword entry
  type validation behavior.
- See `docs/plans/2026-06-09-text-token-normalization.md` for text token
  normalization behavior.
- See `docs/plans/2026-06-09-explicit-stopword-set-normalization.md` for
  explicit stopword set normalization behavior.
- See `docs/plans/2026-06-10-stopword-language-label-normalization.md` for
  language label normalization behavior.
- See `docs/plans/2026-06-10-stopword-language-label-validation.md` for
  language label validation behavior.
- See `docs/plans/2026-06-09-make-gate-aliases.md` for the local verification
  gate aliases.
- See `SECURITY.md` for vulnerability reporting and safe research guidance.
- See `VISION.md` for project direction and contribution guardrails.

## Contributing

Keep changes small and tied to the project that is already present in this repository. For code changes, document the toolchain used, avoid committing generated dependency directories or local configuration, and update this README when setup or verification steps change.
