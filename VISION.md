## Natural Language Processing Vision

This document explains the current state and direction of the project.
Project overview and developer docs: [`README.md`](README.md)

Natural Language Processing is a Python/NLTK sample for language detection using
stopword overlap.

The repository is useful as a compact example of tokenizing text, comparing
words against NLTK stopword lists, and returning the highest-scoring language.

The goal is to keep the sample educational, reproducible, and honest about the
limits of a stopword-based approach.

The current focus is:

Priority:

- Preserve the stopword-ratio language detection example
- Keep NLTK dependency requirements visible
- Keep the reviewed Python 3.12 dependency graph in `constraints.txt` while
  acknowledging that exact versions do not authenticate package artifacts
- Avoid claiming production-level language detection accuracy
- Keep sample text and stop-word data reviewable
- Keep deterministic fixture tests for clear and no-match input
- Return an explicit unknown result when stopword evidence is absent or too weak
- Return unknown for ambiguous tied stopword evidence
- Return unknown for near-tie stopword evidence that does not clear the margin
- Ignore punctuation-only tokens before stopword scoring
- Preserve explicit empty stopword mappings as no evidence
- Return unknown when stopword evidence is too sparse for the amount of text
- Preserve stopword entry normalization before scoring provider data
- Preserve the stopword entry type guard for provider and explicit collections
- Preserve text token normalization before stopword scoring
- Preserve the token entry type guard for injected tokenizer output
- Preserve the tokenizer output type guard before token iteration
- Preserve the tokenizer iteration failure guard during token consumption
- Preserve the tokenizer invocation failure guard around provider calls
- Preserve all-or-nothing stopword normalization when iterables fail
- Preserve explicit stopword set normalization before scoring custom mappings
- Preserve stopword mapping iteration failure isolation before scoring partial data
- Preserve language label normalization before scoring custom mappings
- Preserve language label validation before exposing detector output labels
- Preserve the language label control character guard before CLI output
- Preserve bounded detector text before invoking tokenizers
- Keep `make lint`, `make test`, `make build`, and `make check` available
- Keep pinned, read-only Python 3.12 hosted validation dependency-aware and
  independent of private text or NLTK corpus downloads

Next priorities:

- Add tests for longer mixed-language passages
- Document known limitations compared with model-based language detection

Contribution rules:

- One PR = one focused detector, data, test, or documentation change.
- Use small text fixtures for examples.
- Keep dependency changes documented.
- Explain accuracy claims with tests or references.
- Preserve punctuation-only token filtering when changing tokenization.
- Preserve explicit empty stopword mappings when changing injected fixtures.
- Preserve sparse stopword density checks when changing scoring thresholds.
- Preserve stopword entry normalization when changing corpus loading.
- Preserve text token normalization when changing tokenization.
- Preserve explicit stopword set normalization when changing custom stopword inputs.
- Preserve language label normalization when changing custom stopword inputs.
- Preserve language label validation when changing provider or custom mapping keys.
- Run the Makefile verification aliases before merging detector changes.

## Security And Responsible Use

Canonical security policy and reporting:

- [`SECURITY.md`](SECURITY.md)

Text samples may contain personal content. Tests and examples should use public
or synthetic text, and error output should avoid dumping private input.
Explicit stopword set normalization should keep caller-provided mappings on the
same normalization path as provider-loaded stopwords.
Language label normalization should keep caller-provided and provider-loaded
language names deterministic and merge duplicate normalized labels before scoring.
Language label validation should ignore non-string or non-alphabetic labels
before they can appear in detector output.

## What We Will Not Merge (For Now)

- Production accuracy claims without evaluation
- Private text corpora
- Large model dependencies without a clear reason
- Behavior changes without test fixtures

This list is a roadmap guardrail, not a permanent rule.
Strong user demand and strong technical rationale can change it.
