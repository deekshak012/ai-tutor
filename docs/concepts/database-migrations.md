# Concept: Database migrations

## What it is

A migration is a small, versioned script that moves a database schema from one state to the next (for example, "add a `courses` table") and, ideally, back again. Migrations are applied in order, and the database records which ones it has already run. That way any copy of the database (your laptop, CI, production) can be brought to the same schema just by running the missing steps.

## Why it matters here

The schema will grow with every release: courses, knowledge store chunks with embeddings, learner model statistics, lessons. Each feature adds its tables as a new migration. In ai-tutor this is done with Alembic, set up in [PLAT-01](../features/PLAT-01-backend-skeleton.md). The first migration, `backend/migrations/versions/0001_enable_pgvector.py`, enables the `vector` extension.

## How it works

- **Chain of revisions.** Each script has a `revision` id and a `down_revision` that points to its parent. `0001` has `down_revision = None`, so it's the root. "Head" is the newest script in the chain.
- **Version table.** Alembic keeps a one-row table, `alembic_version`, holding the revision the database is at. `alembic upgrade head` walks the chain from that revision to head and calls each script's `upgrade()`. `alembic downgrade -1` calls `downgrade()` on the current revision.
- **Transactions.** Postgres can run most DDL inside a transaction, so a migration that fails partway is rolled back entirely, and `alembic_version` isn't bumped.
- **Autogenerate.** `alembic revision --autogenerate -m "..."` compares the ORM models registered on `Base.metadata` with the live database and drafts a script containing the difference. It's a draft: always read it before you commit, because renames often show up as a drop plus an add.
- **Why not `create_all()`?** SQLAlchemy's `Base.metadata.create_all()` creates tables that are missing and does nothing else. It can't add a column, change a type, or backfill data in an existing table, and it keeps no history. That's fine for throwaway test databases and not enough for a database with data you care about.
- **Testing migrations.** A round-trip test (upgrade to head, downgrade to base, upgrade again) catches broken `downgrade()` functions and scripts that can't be re-applied. ai-tutor has one in `backend/tests/test_migrations.py`.

Useful commands (run from `backend/`):

```bash
alembic current            # which revision is this DB at?
alembic history            # the chain on disk
alembic upgrade head       # apply everything missing
alembic downgrade -1       # undo the latest
alembic upgrade head --sql # print the SQL without running it (offline mode)
```

## Further reading

- Alembic tutorial: https://alembic.sqlalchemy.org/en/latest/tutorial.html
- Alembic autogenerate, and what it can't detect: https://alembic.sqlalchemy.org/en/latest/autogenerate.html
