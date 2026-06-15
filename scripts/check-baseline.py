#!/usr/bin/env python3
"""Static baseline checks for the stopword language detector."""

from pathlib import Path
import ast
import re
import sys
import xml.etree.ElementTree as ET


ROOT = Path(__file__).resolve().parents[1]
EXPECTED_MAKEFILE = """ROOT := $(abspath $(dir $(lastword $(MAKEFILE_LIST))))

.PHONY: build clean compile lint static-check test verify check

PYTHON ?= python3

check: clean verify
\t$(MAKE) -f "$(ROOT)/Makefile" clean

clean:
\tfind "$(ROOT)" -type f \\( -name '*.pyc' -o -name '*.pyo' \\) -delete
\tfind "$(ROOT)" -type d -name '__pycache__' -prune -exec rm -rf {} +

compile:
\tcd "$(ROOT)" && PYTHONDONTWRITEBYTECODE=1 $(PYTHON) -m py_compile language_detection.py tests/test_language_detection.py scripts/check-baseline.py

build: compile

test:
\tcd "$(ROOT)" && PYTHONDONTWRITEBYTECODE=1 $(PYTHON) -m unittest discover -s tests

static-check:
\tPYTHONDONTWRITEBYTECODE=1 $(PYTHON) "$(ROOT)/scripts/check-baseline.py"

lint: static-check

verify: compile test static-check
"""


def read(relative_path):
    return (ROOT / relative_path).read_text(encoding="utf-8", errors="replace")


def require(condition, message, failures):
    if not condition:
        failures.append(message)


def markdown_section(document, heading):
    match = re.search(
        rf"(?ms)^## {re.escape(heading)}\s*$\n(.*?)(?=^## |\Z)",
        document,
    )
    return match.group(1).strip() if match else ""


def main():
    failures = []
    required = [
        ".gitignore",
        ".github/workflows/check.yml",
        "CHANGES.md",
        "Makefile",
        "README.md",
        "SECURITY.md",
        "VISION.md",
        "constraints.txt",
        "requirements.txt",
        "language_detection.py",
        "stop_words.txt",
        "tests/test_language_detection.py",
        "docs/plans/2026-06-08-language-detection-baseline.md",
        "docs/plans/2026-06-09-ambiguous-stopword-ties.md",
        "docs/plans/2026-06-09-empty-stopword-mapping.md",
        "docs/plans/2026-06-09-make-gate-aliases.md",
        "docs/plans/2026-06-09-near-tie-stopword-margin.md",
        "docs/plans/2026-06-09-punctuation-token-filter.md",
        "docs/plans/2026-06-09-sparse-stopword-density.md",
        "docs/plans/2026-06-09-stopword-entry-normalization.md",
        "docs/plans/2026-06-09-text-token-normalization.md",
        "docs/plans/2026-06-09-explicit-stopword-set-normalization.md",
        "docs/plans/2026-06-10-stopword-language-label-normalization.md",
        "docs/plans/2026-06-10-stopword-language-label-validation.md",
        "docs/plans/2026-06-10-hosted-python-validation.md",
        "docs/plans/2026-06-12-bounded-detector-text.md",
        "docs/plans/2026-06-12-python-dependency-constraints.md",
        "docs/plans/2026-06-13-language-label-control-guard.md",
        "docs/plans/2026-06-13-location-independent-make.md",
        "docs/plans/2026-06-14-stopword-entry-type-guard.md",
        "docs/plans/2026-06-15-stopword-entry-type-guard.md",
        "docs/plans/2026-06-15-token-entry-type-guard.md",
        "docs/readme-overview.svg",
        "scripts/check-baseline.py",
    ]
    for path in required:
        require((ROOT / path).is_file(), f"required file missing: {path}", failures)

    for path in ["language_detection.py", "tests/test_language_detection.py", "scripts/check-baseline.py"]:
        try:
            ast.parse(read(path), filename=path)
        except SyntaxError as error:
            failures.append(f"{path} must parse as Python 3: {error}")

    try:
        ET.parse(ROOT / "docs/readme-overview.svg")
    except ET.ParseError as error:
        failures.append(f"docs/readme-overview.svg must parse as XML: {error}")

    source = read("language_detection.py")
    require("print " not in source, "language_detection.py must not use Python 2 print syntax", failures)
    require("def load_stopword_sets" in source and "LookupError" in source,
            "detector must have an NLTK corpus fallback", failures)
    require("UNKNOWN_LANGUAGE" in source,
            "detector must return an explicit unknown result for zero-score input",
            failures)
    require("def _normalise_tokens" in source and "character.isalpha()" in source,
            "detector must ignore punctuation-only tokens before stopword scoring",
            failures)
    require("def _normalise_tokens" in source and "token.strip().lower()" in source,
            "detector must strip and lowercase text tokens before stopword scoring",
            failures)
    require("if not isinstance(token, str):" in source and
            source.find("if not isinstance(token, str):") < source.find("normalised_token = token.strip().lower()"),
            "detector must ignore non-string tokenizer entries before normalization",
            failures)
    token_normalizer = source.split("def _normalise_tokens", 1)[1].split("def _normalise_stopwords", 1)[0]
    require("if isinstance(tokens, (str, bytes)):" in token_normalizer and
            "token_iterator = iter(tokens)" in token_normalizer and
            "except TypeError:" in token_normalizer and
            "for token in token_iterator:" in token_normalizer and
            "for token in tokens:" not in token_normalizer,
            "detector must reject scalar and non-iterable tokenizer output before entry normalization",
            failures)
    require("def _normalise_stopwords" in source and "word.strip().lower()" in source,
            "detector must strip, lowercase, and drop blank stopword entries",
            failures)
    require("if not isinstance(word, str):" in source and "normalised_word = word.strip().lower()" in source,
            "detector must ignore non-string stopword entries before normalization",
            failures)
    require("def _normalise_stopword_sets" in source and "_normalise_stopword_sets(stopword_sets)" in source,
            "detector must normalize explicit stopword set mappings",
            failures)
    require("def _normalise_language_name" in source and "normalised_sets.setdefault" in source and "return _normalise_stopword_sets({" in source,
            "detector must normalize and merge stopword language labels",
            failures)
    require("if not isinstance(language, str)" in source and
            "not normalised_language.isprintable()" in source and
            "character.isalpha() for character in normalised_language" in source,
            "detector must reject non-string, control-bearing, and non-alphabetic language labels",
            failures)
    require("highest_scoring_languages" in source and "len(highest_scoring_languages) != 1" in source,
            "detector must return unknown for ambiguous top-score ties",
            failures)
    require("MIN_STOPWORD_MARGIN" in source and "runner_up_score" in source,
            "detector must return unknown for near-tie stopword scores",
            failures)
    require("MIN_STOPWORD_DENSITY" in source and "_has_enough_stopword_density" in source,
            "detector must return unknown for sparse stopword evidence",
            failures)
    require("stopword_sets is not None" in source,
            "detector must preserve explicit empty stopword mappings",
            failures)
    validation_index = source.find("if len(text) > MAXIMUM_TEXT_CHARACTERS")
    tokenizer_index = source.find("(tokenizer or _default_tokenizer())(text)")
    require("MAXIMUM_TEXT_CHARACTERS = 100_000" in source and
            "if not isinstance(text, str)" in source and
            "text exceeds 100000 character limit" in source and
            0 <= validation_index < tokenizer_index,
            "detector text must be typed and bounded before tokenization",
            failures)
    require("argparse" in source and "if __name__ == \"__main__\"" in source,
            "detector must expose a small CLI", failures)

    tests = read("tests/test_language_detection.py")
    for expected in [
        "test_detect_language",
        "test_unknown",
        "test_calculate_language_ratios",
        "test_ambiguous_top_score_returns_unknown",
        "test_near_tie_stopword_scores_return_unknown",
        "test_empty_stopword_mapping_is_no_evidence",
        "test_punctuation_only_tokens_do_not_create_stopword_evidence",
        "test_sparse_stopword_evidence_returns_unknown",
        "test_stopword_entries_are_normalized_and_blank_entries_ignored",
        "test_explicit_stopword_sets_are_normalized_before_scoring",
        "test_explicit_stopword_language_labels_are_normalized_before_scoring",
        "test_invalid_language_labels_are_ignored",
        "test_control_character_language_labels_are_ignored",
        "test_provider_language_labels_are_normalized_before_scoring",
        "test_text_tokens_are_normalized_before_scoring",
        "test_non_string_tokenizer_entries_are_ignored",
        "test_malformed_tokenizer_output_collections_return_unknown",
        "test_text_character_limit_is_checked_before_tokenization",
        "test_invalid_text_types_are_rejected_without_echoing_values",
        "test_none_text_retains_empty_text_behavior",
        "test_checked_in_stop_words",
    ]:
        require(expected in tests, f"tests must include {expected}", failures)

    requirements = read("requirements.txt")
    require("nltk" in requirements.lower(), "requirements must document nltk", failures)
    gitignore = read(".gitignore")
    for expected in ["__pycache__/", "*.pyc", ".env"]:
        require(expected in gitignore, f".gitignore must include {expected}", failures)

    makefile = read("Makefile")
    require(makefile == EXPECTED_MAKEFILE,
            "Makefile must exactly preserve rooted compile, test, check, and cleanup gates",
            failures)

    readme = read("README.md")
    docs = readme + "\n" + read("VISION.md") + "\n" + read("SECURITY.md")
    location_independent_make_plan = read(
        "docs/plans/2026-06-13-location-independent-make.md"
    )
    require("make -f /path/to/Natural-Language-Processing/Makefile check" in readme,
            "README must document location-independent Makefile invocation", failures)
    require(all(evidence in location_independent_make_plan.lower() for evidence in [
        "status: completed",
        "root and external-directory",
        "eight isolated hostile mutations",
    ]),
            "location-independent Make plan must record completed root, external, and mutation verification",
            failures)
    for phrase in ["make lint", "make test", "make build", "make check", "language_detection.py", "stopword", "ambiguous", "near-tie", "private text", "punctuation-only", "empty stopword", "sparse stopword", "stopword entry normalization", "text token normalization", "explicit stopword set normalization", "language label normalization", "language label validation", "language label control character guard", "bounded detector text"]:
        require(phrase in docs.lower(), f"docs must mention {phrase}", failures)
    for relative_path in ["README.md", "SECURITY.md", "VISION.md", "CHANGES.md"]:
        require("stopword entry type guard" in read(relative_path).lower(),
                f"{relative_path} must document the stopword entry type guard",
                failures)
        require("token entry type guard" in read(relative_path).lower(),
                f"{relative_path} must document the token entry type guard",
                failures)
        require("tokenizer output type guard" in read(relative_path).lower(),
                f"{relative_path} must document the tokenizer output type guard",
                failures)

    plan = read("docs/plans/2026-06-08-language-detection-baseline.md")
    require("status: completed" in plan and "Verification" in plan,
            "plan must be completed and include verification", failures)
    require("scripts/check-baseline.py" in plan,
            "plan must reference the active baseline checker", failures)
    ambiguity_plan = read("docs/plans/2026-06-09-ambiguous-stopword-ties.md")
    require("status: completed" in ambiguity_plan and "make check" in ambiguity_plan,
            "ambiguity plan must be completed and include verification", failures)
    margin_plan = read("docs/plans/2026-06-09-near-tie-stopword-margin.md")
    require("status: completed" in margin_plan and "make check" in margin_plan,
            "near-tie margin plan must be completed and include verification", failures)
    punctuation_plan = read("docs/plans/2026-06-09-punctuation-token-filter.md")
    require("status: completed" in punctuation_plan and "make check" in punctuation_plan,
            "punctuation token filter plan must be completed and include verification", failures)
    empty_mapping_plan = read("docs/plans/2026-06-09-empty-stopword-mapping.md")
    require("status: completed" in empty_mapping_plan and "make check" in empty_mapping_plan,
            "empty stopword mapping plan must be completed and include verification", failures)
    make_gate_plan = read("docs/plans/2026-06-09-make-gate-aliases.md")
    require("status: completed" in make_gate_plan and "make lint" in make_gate_plan and "make build" in make_gate_plan,
            "make gate aliases plan must be completed and include verification", failures)
    sparse_density_plan = read("docs/plans/2026-06-09-sparse-stopword-density.md")
    require("status: completed" in sparse_density_plan and "make check" in sparse_density_plan,
            "sparse stopword density plan must be completed and include verification", failures)
    stopword_normalization_plan = read("docs/plans/2026-06-09-stopword-entry-normalization.md")
    require("status: completed" in stopword_normalization_plan and "make check" in stopword_normalization_plan,
            "stopword entry normalization plan must be completed and include verification", failures)
    text_token_normalization_plan = read("docs/plans/2026-06-09-text-token-normalization.md")
    require("status: completed" in text_token_normalization_plan and "make check" in text_token_normalization_plan,
            "text token normalization plan must be completed and include verification", failures)
    explicit_stopword_plan = read("docs/plans/2026-06-09-explicit-stopword-set-normalization.md")
    require("status: completed" in explicit_stopword_plan and "make check" in explicit_stopword_plan,
            "explicit stopword set normalization plan must be completed and include verification", failures)
    language_label_plan = read("docs/plans/2026-06-10-stopword-language-label-normalization.md")
    require("status: completed" in language_label_plan and "make check" in language_label_plan,
            "stopword language label normalization plan must be completed and include verification", failures)
    language_label_validation_plan = read("docs/plans/2026-06-10-stopword-language-label-validation.md")
    require("status: completed" in language_label_validation_plan and "make check" in language_label_validation_plan,
            "stopword language label validation plan must be completed and include verification", failures)
    bounded_text_plan = read("docs/plans/2026-06-12-bounded-detector-text.md")
    require("status: completed" in bounded_text_plan and "hostile mutations" in bounded_text_plan,
            "bounded detector text plan must record completed verification", failures)
    language_label_control_plan = read("docs/plans/2026-06-13-language-label-control-guard.md")
    require("status: completed" in language_label_control_plan and "hostile mutations" in language_label_control_plan,
            "language label control character plan must record completed verification", failures)
    require('"eng\\nlish"' in tests and '"eng\\x1b[31m"' in tests,
            "tests must cover newline and terminal escape language labels", failures)
    require("test_non_string_mapping_stopword_entries_are_ignored" in tests and
            "test_non_string_provider_stopword_entries_are_ignored" in tests and
            'b"and"' in tests and "object()" in tests,
            "tests must cover malformed mapping and provider stopword entries", failures)
    require('"\\tyou\\n", None, 123' in tests and '"YOU", "", "  ", None, 123' in tests,
            "tests must cover non-string provider and explicit stopword entries", failures)
    stopword_entry_type_plan = read("docs/plans/2026-06-14-stopword-entry-type-guard.md")
    require("status: completed" in stopword_entry_type_plan and "hostile mutations" in stopword_entry_type_plan,
            "stopword entry type guard plan must record completed verification", failures)
    heterogeneous_entry_plan = read("docs/plans/2026-06-15-stopword-entry-type-guard.md")
    heterogeneous_entry_verification = markdown_section(
        heterogeneous_entry_plan, "Verification Completed"
    )
    require("status: completed" in heterogeneous_entry_plan and
            "All four Make gates passed" in heterogeneous_entry_verification and
            "Six isolated hostile mutations were rejected" in heterogeneous_entry_verification and
            "21 offline tests passed" in heterogeneous_entry_verification and
            "external directory" in heterogeneous_entry_verification and
            not re.search(r"(?i)\b(?:pending|todo|tbd|not run)\b", heterogeneous_entry_verification),
            "heterogeneous stopword entry coverage plan must record completed verification", failures)
    token_entry_plan = read("docs/plans/2026-06-15-token-entry-type-guard.md")
    token_entry_verification = markdown_section(token_entry_plan, "Verification Completed")
    require("status: completed" in token_entry_plan and
            "All four Make gates passed" in token_entry_verification and
            "Six isolated hostile mutations were rejected" in token_entry_verification and
            "22 offline tests passed" in token_entry_verification and
            "external directory" in token_entry_verification and
            not re.search(r"(?i)\b(?:pending|todo|tbd|not run)\b", token_entry_verification),
            "token entry type guard plan must record completed verification", failures)
    token_entry_test_match = re.search(
        r"(?ms)^    def test_non_string_tokenizer_entries_are_ignored\(self\):\n(.*?)(?=^    def test_|\Z)",
        tests,
    )
    token_entry_test = token_entry_test_match.group(1) if token_entry_test_match else ""
    require("def malformed_entry_tokenizer" in tests and
            'b"and"' in tests and "object()" in tests and
            "_calculate_languages_ratios(" in token_entry_test and
            '{"english": 3, "french": 0, "spanish": 0}' in token_entry_test and
            "detect_language(" in token_entry_test and
            '            "english",' in token_entry_test,
            "tests must cover malformed tokenizer entries through ratios and detection", failures)
    tokenizer_output_plan = read("docs/plans/2026-06-15-tokenizer-output-type-guard.md")
    tokenizer_output_verification = markdown_section(tokenizer_output_plan, "Verification Completed")
    require("status: completed" in tokenizer_output_plan and
            "All four Make gates passed" in tokenizer_output_verification and
            "Seven isolated hostile mutations were rejected" in tokenizer_output_verification and
            "23 offline tests passed" in tokenizer_output_verification and
            "external directory" in tokenizer_output_verification and
            not re.search(r"(?i)\b(?:pending|todo|tbd|not run)\b", tokenizer_output_verification),
            "tokenizer output type guard plan must record completed verification", failures)
    tokenizer_output_test_match = re.search(
        r"(?ms)^    def test_malformed_tokenizer_output_collections_return_unknown\(self\):\n(.*?)(?=^    def test_|\Z)",
        tests,
    )
    tokenizer_output_test = tokenizer_output_test_match.group(1) if tokenizer_output_test_match else ""
    require('malformed_outputs = [None, 123, object(), "the and you", b"the and you"]' in tokenizer_output_test and
            "tokenizer=malformed_output_tokenizer" in tokenizer_output_test and
            '{"english": 0, "french": 0, "spanish": 0}' in tokenizer_output_test and
            "UNKNOWN_LANGUAGE" in tokenizer_output_test,
            "tests must cover malformed tokenizer output collections through ratios and detection", failures)
    hosted_plan = read("docs/plans/2026-06-10-hosted-python-validation.md")
    constraints_plan = read("docs/plans/2026-06-12-python-dependency-constraints.md")
    requirements = read("requirements.txt")
    constraints = read("constraints.txt")
    docs = "\n".join(read(path) for path in ["README.md", "SECURITY.md", "VISION.md", "CHANGES.md"])
    workflow = read(".github/workflows/check.yml")
    require("status: completed" in hosted_plan and "make check" in hosted_plan,
            "hosted Python validation plan must be completed and include verification", failures)
    for expected in [
        "permissions:\n  contents: read",
        "cancel-in-progress: true",
        "runs-on: ubuntu-24.04",
        "timeout-minutes: 10",
        "actions/checkout@df4cb1c069e1874edd31b4311f1884172cec0e10",
        "actions/setup-python@a309ff8b426b58ec0e2a45f0f869d46889d02405",
        'python-version: "3.12"',
        "persist-credentials: false",
        "cache-dependency-path: |\n            requirements.txt\n            constraints.txt",
        "python -m pip install --requirement requirements.txt --constraint constraints.txt",
        "python -m pip check",
        "run: make check",
    ]:
        require(expected in workflow, f"Check workflow must keep {expected}", failures)
    expected_constraints = """# Reviewed CI resolution for Python 3.12.
click==8.4.1
joblib==1.5.3
nltk==3.9.4
regex==2026.5.9
tqdm==4.68.1
"""
    require(requirements == "nltk>=3.8,<4\n",
            "requirements.txt must preserve the NLTK 3.x compatibility range", failures)
    require(constraints == expected_constraints,
            "constraints.txt must match the reviewed Python 3.12 graph exactly", failures)
    require(workflow.count("python -m pip install") == 1,
            "Check workflow must contain exactly one constrained dependency installation", failures)
    require("constraints.txt" in docs,
            "README, security, vision, or change docs must describe dependency constraints", failures)
    require("do not authenticate" in docs.lower(),
            "docs must describe the constraints artifact-authentication boundary", failures)
    status = re.findall(r"(?mi)^status:\s*(.+?)\s*$", constraints_plan)
    completed_work = markdown_section(constraints_plan, "Work Completed")
    completed_verification = markdown_section(constraints_plan, "Verification Completed")
    require(status == ["completed"] and completed_work and "Pending" not in completed_work,
            "dependency constraints plan must record one completed status and completed work", failures)
    verification_evidence = [
        "Official PyPI metadata",
        "Python 3.12.8",
        "pip check",
        "pip-audit -r constraints.txt --no-deps",
        "make lint",
        "make test",
        "make build",
        "make check",
        "hostile mutations",
        "git diff --check",
    ]
    require(completed_verification and "Pending" not in completed_verification and
            all(item in completed_verification for item in verification_evidence),
            "dependency constraints plan must record finished local verification", failures)

    if failures:
        for failure in failures:
            print(failure, file=sys.stderr)
        return 1

    print("NLP baseline checks passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
