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
python3 -m pip install -r requirements.txt
python3 -m nltk.downloader stopwords  # optional; falls back to stop_words.txt when absent
```

The setup commands above are derived from repository files. Legacy mobile, Python, or JavaScript samples may require older SDKs or package versions than a modern workstation uses by default.

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

## Testing and Verification

- `make lint`
- `make test`
- `make build`
- `make check`
- `python3 -m unittest discover -s tests`
- `python3 scripts/check-baseline.py`

When the required SDK or runtime is unavailable, use static checks and source review first, then verify on a machine that has the matching platform toolchain.

## Configuration and Secrets

- No required secret or credential file was identified in the repository scan. If you add integrations later, keep secrets out of git.

## Security and Privacy Notes

- Review changes touching network requests, sockets, or service endpoints; examples from the scan include language_detection.py.

## Maintenance Notes

- The unit tests use small injected stopword fixtures, so they do not require
  downloading NLTK corpora.
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
- See `docs/plans/2026-06-09-make-gate-aliases.md` for the local verification
  gate aliases.
- See `SECURITY.md` for vulnerability reporting and safe research guidance.
- See `VISION.md` for project direction and contribution guardrails.

## Contributing

Keep changes small and tied to the project that is already present in this repository. For code changes, document the toolchain used, avoid committing generated dependency directories or local configuration, and update this README when setup or verification steps change.
