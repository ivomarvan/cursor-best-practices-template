---
name: sqlalchemy-dev
description: >-
  Set up SQLAlchemy 2.x with async support, Alembic migrations, and Docker PostgreSQL
  for a Python project. Guides through project scaffolding, model definition, session
  factory, Alembic initialization, and day-to-day migration workflow.
  Use when: adding SQLAlchemy to a project, initializing Alembic, generating or applying
  migrations, or debugging session/transaction issues.
---

# Skill: SQLAlchemy + Alembic Development Workflow
<!-- cs: Skill: Vývojový workflow pro SQLAlchemy + Alembic -->

## Prerequisites
<!-- cs: Předpoklady -->

- Docker Compose with PostgreSQL is running (see `postgresql-dev` skill).
- `pyproject.toml` exists with Python 3.11+.
- Rule `16-sqlalchemy.mdc` is in context.

<!-- cs: Docker Compose s PostgreSQL běží (viz skill postgresql-dev).
     pyproject.toml existuje s Python 3.11+. Pravidlo 16-sqlalchemy.mdc je v kontextu. -->

## Step 1 — Install dependencies

```bash
# Core
pip install "sqlalchemy[asyncio]>=2.0" "alembic>=1.13" "asyncpg>=0.29"

# Add to pyproject.toml [project.dependencies]:
# "sqlalchemy[asyncio]>=2.0",
# "alembic>=1.13",
# "asyncpg>=0.29",        # async PostgreSQL driver
# "psycopg[binary]>=3.1", # optional: sync driver for Alembic offline mode
```

## Step 2 — Project structure

```
src/
├── db/
│   ├── __init__.py
│   ├── base.py          # DeclarativeBase + mixins
│   ├── session.py       # engine + AsyncSessionFactory + get_session()
│   └── models/
│       ├── __init__.py  # re-exports all models (Alembic needs to import them)
│       └── document.py  # one file per domain entity
├── <domain>/
│   └── <entity>_repository.py   # uses AsyncSession, no raw SQL outside here
alembic/
├── env.py
├── script.py.mako
└── versions/
```

## Step 3 — Base and mixins (`src/db/base.py`)

```python
from datetime import datetime
from sqlalchemy import text
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

class Base(DeclarativeBase):
    pass

class TimestampMixin:
    created_at: Mapped[datetime] = mapped_column(
        server_default=text("NOW()"), nullable=False
    )
    updated_at: Mapped[datetime | None] = mapped_column(onupdate=text("NOW()"))
```

## Step 4 — Session factory (`src/db/session.py`)

```python
from collections.abc import AsyncGenerator
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from src.config import settings  # pydantic-settings, DATABASE_URL from .env

engine = create_async_engine(settings.DATABASE_URL, pool_pre_ping=True, echo=False)
AsyncSessionFactory = async_sessionmaker(engine, expire_on_commit=False)

async def get_session() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSessionFactory() as session:
        yield session
```

`.env` variable: `DATABASE_URL=postgresql+asyncpg://user:pass@localhost:5432/mydb`

## Step 5 — Initialize Alembic

```bash
# Run once in project root
alembic init -t async alembic
```

Edit `alembic/env.py` — replace the default content with the async pattern from
rule `16-sqlalchemy.mdc` (section "Alembic — Autogenerate with Async Engine").

Key points:
- Set `target_metadata = Base.metadata`
- Import all models in `src/db/models/__init__.py` before `target_metadata` is read
- Set `sqlalchemy.url` in `alembic.ini` or override via `config.set_main_option()` from env

## Step 6 — Day-to-day migration workflow

```bash
# After changing a model in src/db/models/:
alembic revision --autogenerate -m "short description of change"

# Review the generated file in alembic/versions/ BEFORE applying!
# Check: correct table names, no dropped columns by mistake, indexes present.

# Apply to local dev DB
alembic upgrade head

# Rollback one step
alembic downgrade -1

# Show current state
alembic current

# Show history
alembic history --verbose
```

## Step 7 — Common patterns

### Get or 404 (FastAPI)

```python
from fastapi import HTTPException
from sqlalchemy import select

async def get_or_404(session: AsyncSession, model: type, id: UUID) -> Any:
    obj = await session.get(model, id)
    if obj is None:
        raise HTTPException(status_code=404, detail=f"{model.__name__} not found")
    return obj
```

### Transactional service method

```python
async def create_document(session: AsyncSession, data: DocumentCreate) -> Document:
    doc = Document(source_id=data.source_id, url=data.url)
    session.add(doc)
    await session.flush()   # get generated id without committing
    await session.refresh(doc)
    return doc
    # Caller commits: await session.commit()
```

### Bulk insert (performance path)

```python
from sqlalchemy.dialects.postgresql import insert as pg_insert

async def upsert_chunks(session: AsyncSession, rows: list[dict]) -> None:
    stmt = pg_insert(Chunk).values(rows)
    stmt = stmt.on_conflict_do_update(
        index_elements=["source_id"],
        set_={"content": stmt.excluded.content, "updated_at": text("NOW()")},
    )
    await session.execute(stmt)
```

## Troubleshooting

| Symptom | Likely cause | Fix |
|---------|-------------|-----|
| `MissingGreenlet` error | `asyncpg` called from sync context | wrap in `run_sync` or use sync engine |
| Objects expired after commit | `expire_on_commit=True` (default) | set `expire_on_commit=False` in sessionmaker |
| Alembic sees no changes | Models not imported in `env.py` | import all models in `src/db/models/__init__.py` |
| N+1 queries in logs | Lazy loading | add `selectinload` / `joinedload` to the query |
| `DetachedInstanceError` | Accessing relationship after session close | eager-load before closing, or use `expire_on_commit=False` |

## Additional resources
- [../../../rules/16-sqlalchemy.mdc](../../../rules/16-sqlalchemy.mdc)
- [../../../rules/13-sql-postgresql.mdc](../../../rules/13-sql-postgresql.mdc)
- [SQLAlchemy 2.x docs](https://docs.sqlalchemy.org/en/20/)
- [Alembic docs](https://alembic.sqlalchemy.org/en/latest/)
