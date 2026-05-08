---
name: python-dev
description: >-
  Python development workflow in Docker: run scripts, pytest tests (by marker, file,
  coverage), Ruff linter + formatter, mypy strict type checking, dependency management.
  Use when running Python scripts, tests, or code quality checks inside the project.
---

# Python Development Workflow

<!-- cs: Workflow pro vývoj v Pythonu v Dockeru -->

## Prerequisites

<!-- cs: Předpoklady -->

- Docker Compose environment is running: `docker compose up -d`
  <!-- cs: Docker Compose prostředí běží: docker compose up -d -->
- Check `docker-compose.yml` for the Python service name (commonly `api`, `backend`, `app`).
  <!-- cs: Zkontroluj docker-compose.yml pro název Python služby (typicky api, backend, app). -->

## Running Scripts

<!-- cs: Spouštění skriptů -->

```bash
# Run any script — absolute imports work regardless of cwd (git_root_to_syspath)
docker compose exec <service> python src/module/script.py

# Pass arguments
docker compose exec <service> python src/module/script.py --arg value

# Interactive (stdin open)
docker compose exec -it <service> python src/module/script.py

# Open REPL
docker compose exec -it <service> python
```

## Running Tests (pytest)

<!-- cs: Spouštění testů (pytest) -->

```bash
# All tests
docker compose exec <service> pytest

# By marker (defined in pyproject.toml)
docker compose exec <service> pytest -m unit
docker compose exec <service> pytest -m integration
docker compose exec <service> pytest -m "not slow"

# Single file or directory
docker compose exec <service> pytest tests/module/test_parser.py
docker compose exec <service> pytest tests/module/

# Verbose + stop on first failure
docker compose exec <service> pytest -v -x

# Coverage report
docker compose exec <service> pytest --cov=src --cov-report=term-missing
```

## Code Quality

<!-- cs: Kontrola kvality kódu -->

### Ruff — Linter and Formatter

<!-- cs: Ruff — linter a formatter -->

```bash
# Check and auto-fix linting issues
docker compose exec <service> ruff check --fix .

# Format code
docker compose exec <service> ruff format .

# Check only — no changes (for CI)
docker compose exec <service> ruff check .
docker compose exec <service> ruff format --check .
```

### mypy — Static Type Checking

<!-- cs: mypy — statická analýza typů -->

```bash
# Check src/ (uses settings from pyproject.toml)
docker compose exec <service> mypy src/

# Single file
docker compose exec <service> mypy src/module/parser.py

# Override to strict for one-off check
docker compose exec <service> mypy src/ --strict
```

### Full Quality Gate

<!-- cs: Plná kontrola před commitem -->

```bash
docker compose exec <service> ruff check --fix . \
  && docker compose exec <service> ruff format . \
  && docker compose exec <service> mypy src/
```

## Dependency Management

<!-- cs: Správa závislostí -->

```bash
# After changing requirements.txt / pyproject.toml — rebuild and restart
docker compose build <service>
docker compose up -d <service>

# Quick test of a new package inside a running container
docker compose exec <service> pip install <package>
# ⚠️ Then add to requirements.txt/pyproject.toml and rebuild — lost on container restart
```

## Container Shell

<!-- cs: Shell kontejneru -->

```bash
# Open bash in container
docker compose exec -it <service> bash

# As root (for debugging permission issues)
docker compose exec -it -u root <service> bash
```
