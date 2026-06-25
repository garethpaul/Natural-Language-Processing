ifneq ($(origin MAKEFILE_LIST),file)
$(error MAKEFILE_LIST must not be overridden)
endif
override ROOT := $(shell path='$(subst ','"'"',$(MAKEFILE_LIST))'; path=$$(printf '%s\n' "$$path" | sed 's/^ //'); dirname -- "$$path")

.PHONY: build clean compile lint static-check test verify check

PYTHON ?= python3

check: clean verify
	$(MAKE) -f "$(ROOT)/Makefile" clean

clean:
	find "$(ROOT)" -type f \( -name '*.pyc' -o -name '*.pyo' \) -delete
	find "$(ROOT)" -type d -name '__pycache__' -prune -exec rm -rf {} +

compile:
	cd "$(ROOT)" && PYTHONDONTWRITEBYTECODE=1 $(PYTHON) -m py_compile language_detection.py tests/test_language_detection.py tests/test_default_sample_mutations.py tests/test_makefile_root.py scripts/check-baseline.py scripts/test-default-sample-mutations.py

build: compile

test:
	cd "$(ROOT)" && PYTHONDONTWRITEBYTECODE=1 $(PYTHON) -m unittest discover -s tests
	cd "$(ROOT)" && PYTHONDONTWRITEBYTECODE=1 $(PYTHON) scripts/test-default-sample-mutations.py

static-check:
	PYTHONDONTWRITEBYTECODE=1 $(PYTHON) "$(ROOT)/scripts/check-baseline.py"

lint: static-check

verify: compile test static-check
