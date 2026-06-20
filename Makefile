override ROOT := $(abspath $(dir $(lastword $(MAKEFILE_LIST))))

.PHONY: build clean compile lint static-check test verify check

PYTHON ?= python3

check: clean verify
	$(MAKE) -f "$(ROOT)/Makefile" clean

clean:
	find "$(ROOT)" -type f \( -name '*.pyc' -o -name '*.pyo' \) -delete
	find "$(ROOT)" -type d -name '__pycache__' -prune -exec rm -rf {} +

compile:
	cd "$(ROOT)" && PYTHONDONTWRITEBYTECODE=1 $(PYTHON) -m py_compile language_detection.py tests/test_language_detection.py scripts/check-baseline.py

build: compile

test:
	cd "$(ROOT)" && PYTHONDONTWRITEBYTECODE=1 $(PYTHON) -m unittest discover -s tests

static-check:
	PYTHONDONTWRITEBYTECODE=1 $(PYTHON) "$(ROOT)/scripts/check-baseline.py"

lint: static-check

verify: compile test static-check
