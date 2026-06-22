#!/usr/bin/env python3
"""Reject regressions in the no-argument CLI sample contract."""

import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SOURCE_PATH = Path("language_detection.py")
TEST_COMMAND = [
    sys.executable,
    "-m",
    "unittest",
    "discover",
    "-s",
    "tests",
    "-p",
    "test_language_detection.py",
]
MUTATIONS = [
    (
        "misaligned French default",
        "Don told Ma this is our English sample.",
        "Une adoption plus rapide que le telephone classique et mobile.",
        "test_no_argument_main_uses_english_when_nltk_is_unavailable",
    ),
    (
        "Hinglish full-corpus winner",
        "Don told Ma this is our English sample.",
        "This is the English sample, and you will see the result there.",
        "test_default_sample_leads_all_corpus_languages_by_required_margin",
    ),
    (
        "Hinglish sub-margin runner-up",
        "Don told Ma this is our English sample.",
        "Don told Ma this is our English sample, see.",
        "test_default_sample_leads_all_corpus_languages_by_required_margin",
    ),
    (
        "English Hinglish score tie",
        "Don told Ma this is our English sample.",
        "See told Ma this is our English sample.",
        "test_default_sample_leads_all_corpus_languages_by_required_margin",
    ),
    (
        "hardcoded CLI output",
        "print(detect_language(text))",
        'print("english")',
        "test_no_argument_main_prints_detector_result_for_default_sample",
    ),
    (
        "hardcoded no-argument input",
        'text = " ".join(args.text) if args.text else DEFAULT_SAMPLE',
        'text = " ".join(args.text) if args.text else "hardcoded default sample"',
        "test_no_argument_main_prints_detector_result_for_default_sample",
    ),
]


def apply_mutation(source, original, replacement, name):
    if source.count(original) != 1:
        raise RuntimeError(f"{name}: expected exactly one mutation target")
    return source.replace(original, replacement, 1)


def main():
    source = (ROOT / SOURCE_PATH).read_text(encoding="utf-8")
    environment = os.environ.copy()
    environment["PYTHONDONTWRITEBYTECODE"] = "1"
    environment["HTTP_PROXY"] = "http://127.0.0.1:9"
    environment["HTTPS_PROXY"] = "http://127.0.0.1:9"
    environment["NO_PROXY"] = ""

    for name, original, replacement, expected_test in MUTATIONS:
        with tempfile.TemporaryDirectory() as temporary_directory:
            checkout = Path(temporary_directory) / "checkout"
            shutil.copytree(
                ROOT,
                checkout,
                ignore=shutil.ignore_patterns(".git", "__pycache__", "*.pyc", "*.pyo"),
            )
            mutated_source = apply_mutation(source, original, replacement, name)
            (checkout / SOURCE_PATH).write_text(mutated_source, encoding="utf-8")
            result = subprocess.run(
                TEST_COMMAND,
                cwd=checkout,
                env=environment,
                capture_output=True,
                text=True,
                timeout=30,
                check=False,
            )
            output = result.stdout + result.stderr
            if result.returncode == 0 or expected_test not in output:
                print(f"mutation was not rejected: {name}", file=sys.stderr)
                print(output, file=sys.stderr)
                return 1

    print(f"Rejected {len(MUTATIONS)} default-sample mutations.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
