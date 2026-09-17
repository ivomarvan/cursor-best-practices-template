# Deterministic gate for the template's own tooling (scripts/, tests/).
# Same shape as skills/python-dev/templates/Makefile, but runs natively — the template
# is a documentation-plus-scripts repository and is Docker-exempt (030-docker-policy).
#
#   make check          lint + format-check + typecheck + test
#   make audit P=path   read-only audit of an installed project

RUNNER ?=

.PHONY: lint format-check typecheck test check audit

lint:
	$(RUNNER) ruff check scripts tests

format-check:
	$(RUNNER) ruff format --check scripts tests

typecheck:
	$(RUNNER) mypy

test:
	$(RUNNER) pytest

## check — everything must pass before a template change is pushed (CI runs the same).
check: lint format-check typecheck test

audit:
	python3 scripts/check_installation.py $(P)
