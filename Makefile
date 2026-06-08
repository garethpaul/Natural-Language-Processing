.PHONY: clean compile static-check test verify check

PYTHON ?= python3

check: clean verify
	$(MAKE) clean

clean:
	find . -type f \( -name '*.pyc' -o -name '*.pyo' \) -delete
	find . -type d -name '__pycache__' -prune -exec rm -rf {} +

compile:
	PYTHONDONTWRITEBYTECODE=1 $(PYTHON) -m py_compile language_detection.py tests/test_language_detection.py scripts/check-baseline.py

test:
	PYTHONDONTWRITEBYTECODE=1 $(PYTHON) -m unittest discover -s tests

static-check:
	PYTHONDONTWRITEBYTECODE=1 $(PYTHON) scripts/check-baseline.py

verify: compile test static-check
