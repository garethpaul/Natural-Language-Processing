# Mixed-Language Passage Coverage And Accuracy Limits

Status: completed

## Scope

Complete the two bounded roadmap items for longer mixed-language passage tests
and documentation of the stopword detector's limitations relative to
model-based language detection, without changing detector thresholds or output
rules.

## Work Completed

- Add a synthetic balanced English/French passage that must remain `unknown`.
- Add a synthetic mixed passage whose English evidence clears the existing
  stopword density and runner-up margin rules.
- Explain that scoring uses unique normalized word sets rather than frequency,
  syntax, word order, context, dialect, or code-switching patterns.
- Preserve the educational offline scope and avoid production accuracy claims.

## Verification Completed

- Both focused mixed-language regression tests passed.
- `make test` passed 52 tests with four environment-dependent NLTK checks
  skipped and rejected all six default-sample mutations.
- `make build` compiled the detector, tests, baseline checker, and mutation
  runner.
- `make check` passed from the repository root and through an absolute Makefile
  path from an external directory.
- `git diff --check` reported no whitespace errors.

## Residual Risk

Two synthetic English/French examples do not measure real-world accuracy or
cover all language pairs, dialects, transliteration, short text, or code
switching. The detector may still assign a single label to multilingual text
when one stopword set wins by the configured margin and density thresholds.
