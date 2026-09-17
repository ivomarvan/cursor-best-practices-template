# Deterministic quality gate for Python projects.
#
# `make check` is the single command the Coder, the Reviewer, and CI all run — see
# skills/python-dev/SKILL.md and rules/090-apm-orchestration.mdc. "Passes" means the
# same thing in every one of those three contexts, because it is the same target.
#
# Copy this file to your project root and adjust SERVICE to your docker-compose.yml
# service name (commonly api, backend, app).

SERVICE ?= app
COMPOSE := docker compose exec -T $(SERVICE)

.PHONY: lint format-check typecheck test check

lint:
	$(COMPOSE) ruff check .

format-check:
	$(COMPOSE) ruff format --check .

typecheck:
	$(COMPOSE) mypy src/ --strict

test:
	$(COMPOSE) pytest -v

## check — the deterministic gate: everything must pass, in this order, before a Task
## is considered done (Coder) or approved (Reviewer).
check: lint format-check typecheck test
