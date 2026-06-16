# Security Policy

## Supported Versions

The supported security scope for `Natural-Language-Processing` is the current default branch, `master`. Older commits, tags, branches, forks, demos, and generated artifacts are not actively supported unless the repository explicitly marks them as maintained.

Project summary: NLTK via Python

## Reporting a Vulnerability

Please report suspected vulnerabilities through GitHub's private vulnerability reporting or by opening a draft GitHub Security Advisory for `garethpaul/Natural-Language-Processing` when that option is available. If GitHub does not show a private reporting option for this repository, contact the repository owner through GitHub and avoid posting exploit details publicly until the issue can be assessed.

Do not open a public issue that includes exploit code, secrets, personal data, or detailed reproduction steps for an unpatched vulnerability.

## What to Include

Helpful reports include:

- the affected file, endpoint, permission, dependency, or workflow
- a concise impact statement explaining what an attacker could do
- reproduction steps using test data and accounts you control
- the branch, commit SHA, platform version, device, runtime, or dependency versions used
- logs, screenshots, or proof-of-concept snippets that demonstrate impact without exposing private data

## Project Security Posture

- This repository appears to be a public sample, documentation, or utility project. The active security scope is the code and documentation on the default branch.
- Review found network clients, sockets, web APIs, or service endpoints; changes in those areas should receive security-focused review before merge.
- Dependency manifest detected: requirements.txt. Dependency updates should preserve reproducible installation instructions and avoid introducing packages without a clear maintenance reason.
- `constraints.txt` records the reviewed exact Python 3.12 dependency graph
  used by CI. Exact versions reduce resolver drift but do not authenticate
  downloaded package artifacts; review package provenance separately.
- Run `make lint`, `make test`, `make build`, and `make check` after changing detector code, stopword data, dependencies, tests, or security docs.
- The pinned Linux workflow installs declared dependencies and runs local tests
  without private text, external service calls, or NLTK corpus downloads.
- Text samples can contain private text. Tests and examples should use synthetic or public text, and errors should not dump private input.
- Bounded detector text should reject more than 100,000 characters before
  tokenization and keep validation errors free of private input content.
- Near-tie stopword scores should return `unknown` rather than overstating language confidence from weak evidence.
- Punctuation-only tokens should not create language evidence from fallback stopword symbols.
- Explicit empty stopword mappings should remain no-evidence inputs instead of falling back to default corpora.
- Sparse stopword evidence in mostly unrelated or synthetic text should return `unknown` instead of overstating confidence from a few common words.
- Stopword entry normalization should strip, lowercase, and ignore blank corpus
  entries before scoring so provider formatting does not change evidence.
- The stopword entry type guard should ignore non-string provider and explicit
  values without logging or coercing their contents.
- Scalar stopword collections should be rejected before iteration so malformed
  strings cannot create character-level language evidence.
- Text token normalization should strip and lowercase tokenizer output before
  scoring so whitespace-padded input does not change evidence.
- The token entry type guard should ignore non-string tokenizer output without
  logging or coercing attacker-controlled object values.
- The tokenizer output type guard should reject scalar and non-iterable return
  values without logging, coercing, or exposing their representations.
- The tokenizer iteration failure guard should discard partial token evidence
  without exposing iterator diagnostics.
- The tokenizer invocation failure guard should return empty evidence when a
  provider raises before returning tokens, without exposing its diagnostics.
- Stopword iterable failures should discard partial language evidence without
  exposing provider diagnostics.
- Stopword mapping iteration failures should discard all partial language
  evidence without exposing caller diagnostics or retaining order-dependent data.
- The stopword provider invocation failure guard should discard all provider
  evidence when `fileids()` or `words()` raises, without exposing diagnostics.
- Explicit stopword set normalization should strip, lowercase, and ignore blank
  caller-provided entries before scoring so custom mappings match provider behavior.
- Language label normalization should strip and lowercase caller-provided or
  provider-loaded language names, skip blank labels, and merge duplicate
  normalized labels before scoring.
- Language label validation should prevent non-string or non-alphabetic mapping
  keys from becoming output labels.
- The language label control character guard should prevent newline, terminal
  escape, and other non-printable mapping keys from becoming output labels.

## Service and API Notes

For web services, APIs, sockets, or scraping workflows, prioritize reports involving authentication bypass, authorization errors, injection, server-side request forgery, unsafe deserialization, credential leakage, data exposure, or denial-of-service conditions. Use test accounts and minimal proof-of-concept traffic only.

For this detector, reports involving explicit stopword set normalization should
state whether custom mappings can bypass provider-equivalent normalization.
Reports involving language label normalization should state whether noisy or
duplicate custom language labels can change the selected language.
Reports involving language label validation should state whether sentinel or
numeric mapping keys can escape into detector output.

## Dependency and Supply Chain Security

Dependency updates should come from trusted package managers and should keep manifests in sync when manifests exist. Do not commit credentials, private keys, tokens, generated secrets, private text corpora, or machine-local configuration. If a vulnerability depends on a compromised package, typosquatting risk, insecure transitive dependency, or unsafe build step, include the package name, affected version, and the path through which it is used.

## Safe Research Guidelines

Good-faith research is welcome when it stays within these boundaries:

- use only accounts, devices, data, and infrastructure that you own or have explicit permission to test
- avoid destructive actions, persistence, spam, phishing, social engineering, or denial-of-service testing
- minimize access to personal data and stop testing immediately if private data is exposed
- do not exfiltrate secrets or third-party data; report the minimum evidence needed to verify impact
- keep vulnerability details confidential until the maintainer has assessed the report

## Maintainer Response

The maintainer will review complete reports as availability allows, prioritize issues by exploitability and impact, and coordinate a fix or mitigation when the affected code is still maintained. For sample, archived, or educational repositories, the likely remediation may be documentation, dependency updates, or clearly marking unsupported code rather than a production-style patch release.
