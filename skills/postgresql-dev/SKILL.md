---
name: postgresql-dev
description: >-
  PostgreSQL database workflow in Docker: psql interactive shell, Alembic migrations
  (upgrade, downgrade, autogenerate), database dump and restore, GUI tools (pgAdmin
  in Docker, DBeaver, TablePlus). Use when accessing the database, running or generating
  migrations, inspecting schema, or setting up a database GUI client.
---

# PostgreSQL Development Workflow

<!-- cs: Workflow pro přístup k PostgreSQL databázi v Dockeru -->

## Prerequisites

<!-- cs: Předpoklady -->

- PostgreSQL service running: `docker compose up -d db`
  <!-- cs: PostgreSQL služba běží: docker compose up -d db -->
- Credentials available in `.env`: `POSTGRES_USER`, `POSTGRES_PASSWORD`, `POSTGRES_DB`
  <!-- cs: Credentials v .env: POSTGRES_USER, POSTGRES_PASSWORD, POSTGRES_DB -->

## psql — Interactive Shell

<!-- cs: psql — interaktivní shell -->

```bash
# Connect to the database
docker compose exec -it db psql -U ${POSTGRES_USER} -d ${POSTGRES_DB}

# One-shot query (no interactive session)
docker compose exec db psql -U ${POSTGRES_USER} -d ${POSTGRES_DB} \
  -c "SELECT count(*) FROM documents;"

# Run a SQL file
docker compose exec -T db psql -U ${POSTGRES_USER} -d ${POSTGRES_DB} \
  < scripts/seed.sql
```

### Useful psql Meta-Commands

<!-- cs: Užitečné psql meta-příkazy -->

```sql
\dt                 -- list all tables
\d table_name       -- describe table (columns, types, indexes, constraints)
\di                 -- list indexes
\dn                 -- list schemas
\l                  -- list databases
\x                  -- toggle expanded output (useful for wide rows)
\timing             -- toggle query execution time
\q                  -- quit
```

## Alembic Migrations

<!-- cs: Alembic migrace -->

Alembic is run via the Python application service, not directly in `db`.
<!-- cs: Alembic se spouští přes Python aplikační službu, ne přímo v db. -->

```bash
# Apply all pending migrations
docker compose exec <api-service> alembic upgrade head

# Roll back one migration
docker compose exec <api-service> alembic downgrade -1

# Show current applied revision
docker compose exec <api-service> alembic current

# Show full migration history
docker compose exec <api-service> alembic history --verbose

# Auto-generate migration from SQLAlchemy model changes
docker compose exec <api-service> alembic revision --autogenerate -m "add users table"
```

> Always review auto-generated migrations before applying — Alembic may miss renames, constraint changes, or partial indexes.
> <!-- cs: Vždy zkontroluj automaticky generované migrace — Alembic může minout přejmenování, změny constraints nebo partial indexy. -->

## Dump and Restore

<!-- cs: Záloha a obnova -->

```bash
# Dump database to a SQL file (stored in nogit_data — never committed)
docker compose exec db pg_dump -U ${POSTGRES_USER} ${POSTGRES_DB} \
  > nogit_data/backup_$(date +%Y%m%d_%H%M%S).sql

# Restore from a dump
docker compose exec -T db psql -U ${POSTGRES_USER} -d ${POSTGRES_DB} \
  < nogit_data/backup_20260508_090000.sql
```

## GUI Tools

<!-- cs: GUI nástroje -->

### pgAdmin (Docker — recommended for shared environments)

<!-- cs: pgAdmin (Docker — doporučeno pro sdílená prostředí) -->

Add to `docker-compose.yml` under an opt-in `tools` profile:
<!-- cs: Přidej do docker-compose.yml pod opt-in profil tools: -->

```yaml
  pgadmin:
    image: dpage/pgadmin4:8.6
    environment:
      PGADMIN_DEFAULT_EMAIL: ${PGADMIN_EMAIL:-admin@local.dev}
      PGADMIN_DEFAULT_PASSWORD: ${PGADMIN_PASSWORD:-admin}
    ports:
      - "5050:80"
    depends_on:
      - db
    profiles: ["tools"]   # start with: docker compose --profile tools up
```

Access at `http://localhost:5050`.
When adding a server connection inside pgAdmin, use host `db` (Docker internal network name) and port `5432`.
<!-- cs: Přístup na http://localhost:5050. Při přidávání serveru použij host db (Docker network name) a port 5432. -->

### DBeaver (desktop — Linux / Windows / macOS)

<!-- cs: DBeaver (desktop — Linux / Windows / macOS) -->

Free, cross-platform. Connection parameters:
<!-- cs: Zdarma, multiplatformní. Parametry připojení: -->

| Parameter | Value |
|---|---|
| Host | `localhost` |
| Port | mapped port from `docker-compose.yml` (default `5432`) |
| Database | `POSTGRES_DB` from `.env` |
| User | `POSTGRES_USER` from `.env` |
| Password | `POSTGRES_PASSWORD` from `.env` |

### TablePlus (desktop — macOS / Linux)

<!-- cs: TablePlus (desktop — macOS / Linux) -->

Lightweight, fast, paid with a free tier. Same connection parameters as DBeaver.
<!-- cs: Lehký, rychlý, placený s free tier. Stejné parametry připojení jako DBeaver. -->
