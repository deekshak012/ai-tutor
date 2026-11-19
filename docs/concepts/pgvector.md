# Concept: pgvector

## What it is

pgvector is a Postgres extension. It adds a `vector(n)` column type for fixed-length arrays of floats (embeddings), distance operators for comparing them, and index types that make "find the nearest vectors to this one" fast. With it, Postgres itself serves as the vector store.

An **embedding** is a list of numbers that a model produces from a piece of text. Texts with similar meanings get vectors that point in similar directions, so "nearest vector" works as a stand-in for "most related in meaning."

## Why it matters here

The knowledge store keeps content alongside its embedding, so the Tutor, Lesson Builder, and Reviewer can retrieve material by meaning rather than exact keywords. Keeping those vectors in the same Postgres as everything else is the [single-store](postgres-as-single-store.md) choice. [M03 — backend & data store](../curriculum/03-backend-and-data-store.md) shows where the extension is enabled and where a vector column would sit on a knowledge-store row.

## How it works

- **Installed vs enabled.** The extension's files must be present on the database server. The `pgvector/pgvector:pg16` image ships them; stock `postgres:16` doesn't. Then each database has to run `CREATE EXTENSION vector` once, typically as the very first [migration](database-migrations.md). You can check with `SELECT * FROM pg_extension;`.
- **Type.** `embedding vector(1536)` stores a 1536-dimensional vector. The dimension is fixed per column and must match the embedding model's output size. Switching to a model with a different dimension means a migration plus re-embedding the existing rows.
- **Distance operators** (smaller always means closer):
  - `<->`: Euclidean (L2) distance
  - `<=>`: cosine distance (1 − cosine similarity), the usual choice for text embeddings
  - `<#>`: negative inner product
- **Query shape.** `SELECT ... WHERE <filters> ORDER BY embedding <=> :query_vec LIMIT 10;`. The query vector comes from embedding the question with the *same* model through the [model gateway](gateway-pattern.md)'s `embed(...)` call ([M01](../curriculum/01-model-gateway.md)). The gateway uses one configured embedding model, and the column's dimension (`vector(n)`) is fixed by that model. Which provider and model to use is still open.
- **Indexes.** With no index, Postgres compares the query against every row: exact, but slow at scale. An HNSW index (`USING hnsw (embedding vector_cosine_ops)`) or an IVFFlat index gives *approximate* nearest-neighbour search, which is much faster but can occasionally miss a true neighbour. The index's operator class has to match the operator you query with, otherwise the index isn't used.
- **Python side.** The `pgvector` Python package provides a SQLAlchemy `Vector(1536)` column type for ORM models.

## Further reading

- pgvector README: https://github.com/pgvector/pgvector
- pgvector-python (SQLAlchemy integration): https://github.com/pgvector/pgvector-python
- HNSW explained: https://www.pinecone.io/learn/series/faiss/hnsw/
