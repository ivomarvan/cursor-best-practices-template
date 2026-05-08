---
name: docker-new-project
description: >-
  Set up Docker for a new project: create Dockerfile (multi-stage), docker-compose.yml,
  .dockerignore, and README.docker.md. Use when adding Docker to a project for the
  first time, or when asked to containerize a project or service.
---

# Docker New Project Setup

<!-- cs: Přidání Dockeru do nového projektu -->

## Prerequisites

<!-- cs: Předpoklady -->

- Project type is not in the Docker Exclude List (see `03-docker-policy.mdc`).
  <!-- cs: Typ projektu není v Docker Exclude List (viz 03-docker-policy.mdc). -->
- You know the primary runtime (Python, Node.js, etc.) and the required infrastructure services (DB, cache, etc.).
  <!-- cs: Znáš primární runtime a potřebné infrastrukturní služby. -->

## Steps

<!-- cs: Kroky -->

### 1. Determine what to containerize

<!-- cs: 1. Zjisti, co kontejnerizovat -->

Ask the user (or infer from the codebase):
<!-- cs: Zeptej se uživatele nebo zjisti z codebase: -->

- What is the primary application runtime? (Python / Node / Go / …)
- What infrastructure services are needed? (PostgreSQL, Redis, Qdrant, …)
- Is native development environment sufficient, or should the app itself run in Docker?
  Use `profiles` for the app container if native env is preferred.

### 2. Create `.dockerignore`

<!-- cs: 2. Vytvoř .dockerignore -->

```dockerignore
.git
.gitignore
__pycache__
*.pyc
*.pyo
.pytest_cache
.mypy_cache
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

<!-- cs: 3. Vytvoř Dockerfile (multi-stage) -->

Use the appropriate template from `04-docker-standards.mdc`.
Key requirements:
<!-- cs: Použij odpovídající šablonu z 04-docker-standards.mdc. Klíčové požadavky: -->

- Three stages: `builder` → `dev` → `production`
  <!-- cs: Tři fáze: builder → dev → production -->
- Pinned base image version (never `latest`)
  <!-- cs: Pinovaná verze base image (nikdy latest) -->
- Dependencies copied before source code (cache optimization)
  <!-- cs: Závislosti zkopírovány před zdrojovým kódem (cache optimalizace) -->
- Non-root user in `production` stage
  <!-- cs: Non-root user ve fázi production -->
- `HEALTHCHECK` for every service exposing an HTTP endpoint
  <!-- cs: HEALTHCHECK pro každou službu s HTTP endpointem -->

### 4. Create `docker-compose.yml`

<!-- cs: 4. Vytvoř docker-compose.yml -->

- No `version:` field.
  <!-- cs: Bez version: fieldu. -->
- Application service uses `profiles: ["full"]` if native env is preferred for development.
  <!-- cs: Aplikační service používá profiles: ["full"] pokud nativní prostředí postačuje pro vývoj. -->
- Every infrastructure service has a `healthcheck`.
  <!-- cs: Každá infrastrukturní služba má healthcheck. -->
- Secrets via `env_file: .env` — never hardcoded.
  <!-- cs: Secrets přes env_file: .env — nikdy hardcoded. -->
- Named volumes for persistent data.
  <!-- cs: Named volumes pro persistentní data. -->

### 5. Create `README.docker.md`

<!-- cs: 5. Vytvoř README.docker.md -->

Use this structure:
<!-- cs: Použij tuto strukturu: -->

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

<!-- cs: 6. Ověření -->

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
