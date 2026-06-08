#!/usr/bin/env python3
"""Static checks for the language detection sample."""

from pathlib import Path
import re
import sys


ROOT = Path(__file__).resolve().parents[1]
REQUIRED = [
    "CHANGES.md",
    "Makefile",
    "README.md",
    "requirements.txt",
    "docs/plans/2026-06-08-language-detection-baseline.md",
    "tests/test_language_detection.py",
]


def main() -> int:
    failures = []

    for relative_path in REQUIRED:
        if not (ROOT / relative_path).is_file():
            failures.append(f"required file missing: {relative_path}")

    source = (ROOT / "language_detection.py").read_text(encoding="utf-8")
    forbidden_patterns = [
        (r"print\s+[^\(]", "Python 2 print statement"),
        (r"except ImportError:\s*\n\s*print", "dependency failure should not print at import time"),
        (r"max\(ratios,\s*key=ratios\.get\)\s*\n\s*return", "empty input must not force a language"),
    ]
    for pattern, label in forbidden_patterns:
        if re.search(pattern, source):
            failures.append(f"forbidden legacy pattern remains: {label}")

    plan = (ROOT / "docs/plans/2026-06-08-language-detection-baseline.md").read_text(encoding="utf-8")
    if "status: completed" not in plan:
        failures.append("baseline plan must record completed status")

    requirements = (ROOT / "requirements.txt").read_text(encoding="utf-8")
    if "nltk" not in requirements.lower():
        failures.append("requirements.txt must document the NLTK dependency")
    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    if "nltk.downloader stopwords" not in readme:
        failures.append("README must document the NLTK stopwords corpus setup")
    if "MissingNltkError" not in source:
        failures.append("language_detection.py must raise a clear NLTK setup error")

    if failures:
        for failure in failures:
            print(failure, file=sys.stderr)
        return 1

    print("natural language processing baseline checks passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
