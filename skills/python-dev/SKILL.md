---
name: python-dev
description: >-
  Python development workflow in Docker: uv, pytest (by marker, file, coverage),
  Ruff linter + formatter, Pyrefly type checking, ty editor notes.
  Use when running Python scripts, tests, or code quality checks inside the project.
---

# Python Development Workflow

## Prerequisites

- Docker Compose environment is running: `docker compose up -d`
- Check `docker-compose.yml` for the Python service name (commonly `api`, `backend`, `app`).
- The service image is installed via **uv** (`uv.lock` copied at build time). After `pyproject.toml` / `uv.lock` changes: `docker compose build <service>`.

## Running Scripts

The project is installed in the image (`uv sync`). Absolute `src.*` imports work; do not use `git_root_to_syspath`.

```bash
docker compose exec <service> python src/module/script.py
docker compose exec <service> python src/module/script.py --arg value
docker compose exec -it <service> python src/module/script.py
docker compose exec -it <service> python
```

Native (no Docker app container): `uv run python src/module/script.py`

## Running Tests (pytest)

```bash
docker compose exec <service> pytest
docker compose exec <service> pytest -m unit
docker compose exec <service> pytest -m integration
docker compose exec <service> pytest -m "not slow"
docker compose exec <service> pytest tests/module/test_parser.py
docker compose exec <service> pytest -v -x
docker compose exec <service> pytest --cov=src --cov-report=term-missing
```

## Code Quality

### Ruff — Linter and Formatter

```bash
docker compose exec <service> ruff check --fix .
docker compose exec <service> ruff format .
docker compose exec <service> ruff check .
docker compose exec <service> ruff format --check .
```

### Pyrefly — Type Checking (CI)

```bash
docker compose exec <service> pyrefly check
docker compose exec <service> pyrefly check src/module/parser.py
```

Editor: **ty** language server (not a substitute for `pyrefly check` in CI).

### Full Quality Gate

```bash
docker compose exec <service> ruff check --fix . \
  && docker compose exec <service> ruff format . \
  && docker compose exec <service> pyrefly check
```

## Dependency Management

```bash
# Add a dependency on the host, then rebuild the image
uv add <package>          # updates pyproject.toml + uv.lock
uv lock
docker compose build <service>
docker compose up -d <service>

# Audit
uv pip audit
```

Never `uv add` / `pip install` only inside a running container — it is lost on restart.

## Container Shell

```bash
docker compose exec -it <service> bash
docker compose exec -it -u root <service> bash
```
