# Empty Stopword Mapping Plan

status: completed

## Context

`_calculate_languages_ratios` accepts injected stopword sets for deterministic
tests and small experiments. An explicit empty mapping should mean there are no
languages to score, but the previous truthiness check treated it like omitted
configuration and loaded the default stopwords instead.

## Objectives

- Make `None` the only value that triggers default stopword loading.
- Preserve explicit empty stopword mappings as no-evidence inputs.
- Return `unknown` when detection receives an explicit empty mapping.
- Add regression tests and baseline checks for the injected fixture behavior.

## Verification

- `make check`
- `git diff --check`
