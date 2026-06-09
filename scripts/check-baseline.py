#!/usr/bin/env python3
"""Static baseline checks for the stopword language detector."""

from pathlib import Path
import ast
import sys
import xml.etree.ElementTree as ET


ROOT = Path(__file__).resolve().parents[1]


def read(relative_path):
    return (ROOT / relative_path).read_text(encoding="utf-8", errors="replace")


def require(condition, message, failures):
    if not condition:
        failures.append(message)


def main():
    failures = []
    required = [
        ".gitignore",
        "CHANGES.md",
        "Makefile",
        "README.md",
        "SECURITY.md",
        "VISION.md",
        "requirements.txt",
        "language_detection.py",
        "stop_words.txt",
        "tests/test_language_detection.py",
        "docs/plans/2026-06-08-language-detection-baseline.md",
        "docs/plans/2026-06-09-ambiguous-stopword-ties.md",
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
    require("highest_scoring_languages" in source and "len(highest_scoring_languages) != 1" in source,
            "detector must return unknown for ambiguous top-score ties",
            failures)
    require("argparse" in source and "if __name__ == \"__main__\"" in source,
            "detector must expose a small CLI", failures)

    tests = read("tests/test_language_detection.py")
    for expected in [
        "test_detect_language",
        "test_unknown",
        "test_calculate_language_ratios",
        "test_ambiguous_top_score_returns_unknown",
        "test_checked_in_stop_words",
    ]:
        require(expected in tests, f"tests must include {expected}", failures)

    requirements = read("requirements.txt")
    require("nltk" in requirements.lower(), "requirements must document nltk", failures)
    gitignore = read(".gitignore")
    for expected in ["__pycache__/", "*.pyc", ".env"]:
        require(expected in gitignore, f".gitignore must include {expected}", failures)

    docs = read("README.md") + "\n" + read("VISION.md") + "\n" + read("SECURITY.md")
    for phrase in ["make check", "language_detection.py", "stopword", "ambiguous", "private text"]:
        require(phrase in docs.lower(), f"docs must mention {phrase}", failures)

    plan = read("docs/plans/2026-06-08-language-detection-baseline.md")
    require("status: completed" in plan and "Verification" in plan,
            "plan must be completed and include verification", failures)
    require("scripts/check-baseline.py" in plan,
            "plan must reference the active baseline checker", failures)
    ambiguity_plan = read("docs/plans/2026-06-09-ambiguous-stopword-ties.md")
    require("status: completed" in ambiguity_plan and "make check" in ambiguity_plan,
            "ambiguity plan must be completed and include verification", failures)

    if failures:
        for failure in failures:
            print(failure, file=sys.stderr)
        return 1

    print("NLP baseline checks passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
