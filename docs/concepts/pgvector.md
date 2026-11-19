# Concept: pgvector

## What it is

pgvector is a Postgres extension that adds a `vector(n)` column type for fixed-length arrays of floats (embeddings), distance operators to compare them, and indexes that make "find the nearest vectors to this one" fast. With it, Postgres can act as the vector store, so there's no separate vector database to run.

## Why it matters here

The knowledge store keeps content chunks alongside their embeddings so the Tutor, Lesson Builder, and Reviewer can retrieve relevant material. Keeping vectors in the same Postgres as courses, lessons, and the learner model means one database, one backup, one set of migrations, and the ability to join a similarity search with ordinary filters (for example "chunks for this course that the learner hasn't been taught yet") in a single SQL query. That fits [ADR 0001](../decisions/0001-agents-share-state-through-database.md).

[PLAT-01](../features/PLAT-01-backend-skeleton.md) only enables the extension (`CREATE EXTENSION vector` in migration `0001`). No table uses it yet.

## How it works

- **Installed vs enabled.** The extension's files must be present on the database server. The `pgvector/pgvector:pg16` image ships them, which stock `postgres:16` doesn't. Then each database must run `CREATE EXTENSION vector` once, which is what migration `0001` does. You can check with `SELECT * FROM pg_extension;`.
- **Type.** `embedding vector(1536)` stores a 1536-dimensional vector. The dimension is fixed per column and must match your embedding model's output.
- **Distance operators.**
  - `<->`: Euclidean (L2) distance
  - `<=>`: cosine distance (1 − cosine similarity), the usual choice for text embeddings
  - `<#>`: negative inner product (negated so that "smaller is closer" holds for every operator)
- **Query shape.** `SELECT ... ORDER BY embedding <=> :query_vec LIMIT 10;` gives the 10 nearest chunks.
- **Indexes.** Without an index, the query compares the query vector against every row (exact, and slow at scale). An HNSW index (`CREATE INDEX ... USING hnsw (embedding vector_cosine_ops)`) or an IVFFlat index gives *approximate* nearest-neighbour search, which is much faster but can occasionally miss a true neighbour. The index's operator class must match the operator you query with.
- **Python side.** The `pgvector` Python package (already a dependency) provides a SQLAlchemy `Vector` column type, so models can declare `embedding: Mapped[list[float]] = mapped_column(Vector(1536))`.

## Further reading

- pgvector README: https://github.com/pgvector/pgvector
- pgvector-python (SQLAlchemy integration): https://github.com/pgvector/pgvector-python
