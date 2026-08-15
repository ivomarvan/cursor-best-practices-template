---
name: docker-new-project
description: >-
  Set up Docker for a new project: create Dockerfile (multi-stage), docker-compose.yml,
  .dockerignore, and README.docker.md. Use when adding Docker to a project for the
  first time, or when asked to containerize a project or service.
---

# Docker New Project Setup

## Prerequisites

- Project type is not in the Docker Exclude List (see `03-docker-policy.mdc`).
- You know the primary runtime (Python, Node.js, etc.) and the required infrastructure services (DB, cache, etc.).

## Steps

### 1. Determine what to containerize

Ask the user (or infer from the codebase):

- What is the primary application runtime? (Python / Node / Go / …)
- What infrastructure services are needed? (PostgreSQL, Redis, Qdrant, …)
- Is native development environment sufficient, or should the app itself run in Docker?
  Use `profiles` for the app container if native env is preferred.

### 2. Create `.dockerignore`

```dockerignore
.git
.gitignore
__pycache__
*.pyc
*.pyo
.pytest_cache
.mypy_cache
.pyrefly_cache
.ty_cache
.ruff_cache
node_modules
dist
build
*.egg-info
data/
nogit_data/
.env
*.log
README*.md
```

### 3. Create `Dockerfile` (multi-stage)

Use the appropriate template from `04-docker-standards.mdc`.
Key requirements:

- Three stages: `builder` → `dev` → `production` (Python: **uv** + `uv.lock`, see `04-docker-standards.mdc`)
- Pinned base image version (never `latest`)
- Dependencies / lockfile copied before source code (cache optimization)
- Non-root user in `production` stage
- `HEALTHCHECK` without installing `curl` in slim images (use `python -c` / `pg_isready` / the runtime already in PATH)

### 4. Create `docker-compose.yml`

- No `version:` field.
- Application service uses `profiles: ["full"]` if native env is preferred for development.
- Every infrastructure service has a `healthcheck`.
- Secrets via `env_file: .env` — never hardcoded.
- Named volumes for persistent data.

### 5. Create `README.docker.md`

Use this structure:

```markdown
# Docker Usage

## Quick start
docker compose up

## Services
| Service | Port | Description |
|---------|------|-------------|
| api     | 8000 | ... |
| db      | 5432 | PostgreSQL  |

## Development vs Production build
# Development (with dev dependencies)
docker build --target dev -t myapp:dev .

# Production
docker build --target production -t myapp:prod .

## Common tasks
# Run database migrations
docker compose exec api <migration-command>

# Open database shell
docker compose exec db psql -U ${POSTGRES_USER} ${POSTGRES_DB}

# Rebuild after dependency changes
docker compose build --no-cache api

## Cleanup (free disk space)
docker system prune -f
docker volume prune -f
```

### 6. Verify

```bash
docker compose config          # validate compose syntax
docker compose build           # build all images
docker compose up -d           # start services
docker compose ps              # check all services are healthy
docker compose logs --tail=50  # check for startup errors
```

## Additional resources

- [04-docker-standards.mdc](../../rules/04-docker-standards.mdc) — Dockerfile and compose technical standards
- [03-docker-policy.mdc](../../rules/03-docker-policy.mdc) — when Docker is required and the exclude list
