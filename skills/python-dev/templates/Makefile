# Deterministic quality gate for Python projects.
#
# `make check` is the single command the Coder, the Reviewer, and CI all run — see
# skills/python-dev/SKILL.md and rules/090-apm-orchestration.mdc. "Passes" means the
# same thing in every one of those three contexts, because it is the same target.
#
# Copy this file to your project root and adjust:
#   SERVICE     docker-compose.yml service name (commonly api, backend, app)
#   MYPY_PATHS  directories to type-check (default: src/)
#   RUNNER      how commands are executed. Default runs inside the compose service;
#               override for projects/spikes that run natively (Docker-exempt per
#               rules/030-docker-policy.mdc):  make check RUNNER=

SERVICE    ?= app
MYPY_PATHS ?= src/
RUNNER     ?= docker compose exec -T $(SERVICE)

.PHONY: lint format-check typecheck test check

lint:
	$(RUNNER) ruff check .

format-check:
	$(RUNNER) ruff format --check .

typecheck:
	$(RUNNER) mypy $(MYPY_PATHS) --strict

test:
	$(RUNNER) pytest -v

## check — the deterministic gate: everything must pass, in this order, before a Task
## is considered done (Coder) or approved (Reviewer).
check: lint format-check typecheck test
