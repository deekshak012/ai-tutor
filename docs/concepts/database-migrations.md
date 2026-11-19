# Concept: Database migrations

## What it is

A migration is a small, versioned script that moves a database schema from one state to the next (for example, "add a `courses` table") and, ideally, back again. Migrations are applied in order, and the database records which ones it has already run. Any copy of the database (a laptop, CI, production) can then be brought to the same schema by running only the missing steps. In Python, the standard tool is **Alembic**, which pairs with SQLAlchemy.

## Why it matters here

The ai-tutor schema grows with every release: courses and plans, knowledge store rows with embeddings, lessons, learner-model statistics. Each feature adds its tables as a new migration on top of the previous one. The first migration in the substrate just enables the [pgvector](pgvector.md) extension. See [M03 — backend & data store](../curriculum/03-backend-and-data-store.md).

## How it works

- **A chain of revisions.** Each script has a `revision` id and a `down_revision` pointing to its parent. The first has `down_revision = None`, which makes it the root. "Head" is the newest script.
- **Each script has an `upgrade()` and a `downgrade()`.** For example, `upgrade()` runs `CREATE EXTENSION IF NOT EXISTS vector` and `downgrade()` runs `DROP EXTENSION IF EXISTS vector`.
- **The version table.** Alembic owns a one-row table, `alembic_version`, holding the revision this database is at. `alembic upgrade head` walks the chain from there to head, calling each `upgrade()`. `alembic downgrade -1` undoes the latest one.
- **Transactions.** Postgres runs most DDL inside a transaction, so a migration that fails partway rolls back completely and `alembic_version` isn't bumped. On a brand-new database, even the creation of `alembic_version` itself rolls back.
- **Autogenerate.** Alembic can compare the ORM models with the live database and *draft* a migration containing the difference. It's only a draft. A rename, for example, often shows up as a drop plus an add, which would lose data.
- **Why not `create_all()`?** SQLAlchemy's `create_all()` creates missing tables and does nothing else. It can't add a column, change a type, or backfill data in a table that already exists, and it keeps no history. That's fine for throwaway test databases, but not for data you care about.
- **Testing migrations.** A round-trip test (upgrade to head, downgrade to base, upgrade again) catches broken `downgrade()` functions and scripts that can't be re-applied.
- **When they run.** In local dev, often on container start (`alembic upgrade head && uvicorn ...`). In production, usually as a single deploy step, so that several replicas don't race to migrate.

## Further reading

- Alembic tutorial: https://alembic.sqlalchemy.org/en/latest/tutorial.html
- What autogenerate can and can't detect: https://alembic.sqlalchemy.org/en/latest/autogenerate.html
