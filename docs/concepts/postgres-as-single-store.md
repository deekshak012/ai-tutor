# Concept: Postgres as the single store

## What it is

This is the design choice to keep *all* of a system's persistent state in one Postgres database: ordinary relational records, the shared working state that agents hand off to each other, and vector embeddings for similarity search. The alternative is to spread that state across specialised stores, say a relational DB, a vector DB, a cache, and a message bus.

## Why it matters here

Two architecture principles depend on it:

- **Agents share state through the database** ([ADR 0001](../decisions/0001-agents-share-state-through-database.md)). The Researcher writes findings, the Lesson Builder reads them hours later, the Reviewer writes its verdicts, and the Tutor reads the finished lessons. The database is the only channel between these components, so it has to hold every kind of state they exchange.
- **The knowledge store doubles as a cache.** Before researching a concept, the system checks whether verified material already exists. The store row (content, concept tags, source type, verification status, date gathered, embedding) *is* the cache entry. No separate cache layer is needed.

[M03 — backend & data store](../curriculum/03-backend-and-data-store.md) shows the substrate. Later modules add the tables.

## How it works

- **One query can mix relational filters with vector ranking.** "The five chunks closest in meaning to this question, for course 42, verified, not yet taught to this learner" is a single SQL statement: `WHERE` clauses and a join for the filters, plus `ORDER BY embedding <=> :q LIMIT 5` for the ranking (via [pgvector](pgvector.md)). With a separate vector DB you'd query it, get IDs back, then filter in Postgres or in application code, and keep both stores' IDs in sync.
- **Transactions span everything.** Writing a knowledge row and its embedding happens in one commit, so a failure can't leave a row without its vector or a vector with no row.
- **One operational surface.** One backup, one set of [migrations](database-migrations.md), one connection string, one container in [local dev](containerized-local-dev.md).
- **Inspectable state.** Because every hand-off is a row, you can open `psql` at any point and see exactly what the Researcher wrote or what the Reviewer decided. That's the debugging benefit ADR 0001 calls out.
- **Trade-offs.** A dedicated vector database may scale further, or offer features like hybrid search out of the box. Postgres has to be tuned (HNSW index parameters, vacuum) as data grows. At the scale of a personal tutor, one store's simplicity is worth more than either of those. If that ever changes, the decision can be revisited.

## Further reading

- pgvector README: https://github.com/pgvector/pgvector
- Postgres transactions and DDL: https://www.postgresql.org/docs/current/tutorial-transactions.html
