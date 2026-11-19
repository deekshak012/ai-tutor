# Data Guide

The canonical list of every table and field in the system. The `doc-writer` subagent adds a section here whenever a feature introduces or changes a table.

Schema changes are made only through Alembic migrations in `backend/migrations/versions/` (see [database migrations](../concepts/database-migrations.md)). Current head revision: `0001`.

## Format for each entry

```
## table_name

Purpose: one line.

| Column | Type | Description |
|---|---|---|
| id | uuid | ... |

Relationships: ...

Added by: [feature doc](../features/<slug>.md)
```

---

## Extensions

### vector (pgvector)

Purpose: adds the `vector(n)` column type, distance operators (`<->` L2, `<=>` cosine, `<#>` negative inner product), and HNSW/IVFFlat indexes for similarity search. Enabled now so the knowledge store can store embeddings in the same database as everything else. No column uses it yet.

Enabled by: migration `0001_enable_pgvector` (`CREATE EXTENSION IF NOT EXISTS vector`; downgrade drops it). Requires the `pgvector/pgvector:pg16` image, which ships the extension files. Version in the current image: 0.8.7.

Added by: [PLAT-01 backend skeleton](../features/PLAT-01-backend-skeleton.md). Concept: [pgvector](../concepts/pgvector.md).

## Tables

There are no application tables yet. The only table is Alembic's own bookkeeping table.

### alembic_version

Purpose: records which migration revision this database is at, so `alembic upgrade head` applies only the missing migrations. Managed by Alembic. Never edit it by hand except to repair a broken migration state.

| Column | Type | Description |
|---|---|---|
| version_num | varchar(32), primary key | The current head revision id (currently `0001`). There is exactly one row. |

Relationships: none.

Added by: [PLAT-01 backend skeleton](../features/PLAT-01-backend-skeleton.md)
