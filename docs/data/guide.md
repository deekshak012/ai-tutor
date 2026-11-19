# Data Guide

The canonical list of every table and field in the system. In read-to-understand mode this describes the data of the system the curriculum explains; nothing is deployed. The `doc-writer` subagent adds a section whenever a module introduces a table. Entries marked **proposed** are illustrative shapes from a module whose design question is still open.

## Format for each entry

```
## table_name

Purpose: one line.

| Column | Type | Description |
|---|---|---|
| id | uuid | ... |

Relationships: ...

Added by: [module](../curriculum/<NN-slug>.md)
```

## Where data lives (v0.0 modules)

| Store | Holds | Explained in |
|---|---|---|
| Postgres (+ pgvector) | Product state: courses, plans, lessons, knowledge store, learner model — the shared state agents read and write ([ADR 0001](../decisions/0001-agents-share-state-through-database.md)) | [M03](../curriculum/03-backend-and-data-store.md) |
| Langfuse | Operational history: traces, spans/generations, eval dataset runs and scores, and a synced copy of the eval datasets. Prompt versions live here *if* Langfuse prompt management is chosen; the alternative is prompts in git with the version recorded on each trace (open: [M02](../curriculum/02-tracing-and-observability.md) open question 1). No Postgres tables for any of these. | [M02](../curriculum/02-tracing-and-observability.md), [M17](../curriculum/17-eval-runner.md) |
| Git (repo files) | Gold eval data: the three test courses with expected topics and fact checks. Proposed: git-first, mirrored to Langfuse (open; see [M17](../curriculum/17-eval-runner.md) open question 1). | [M18](../curriculum/18-test-courses-and-fact-checks.md) |

## Extension: `vector` (pgvector)

Enabled by the first migration (`CREATE EXTENSION vector`). Adds the `vector(n)` column type, the `<->` / `<=>` / `<#>` distance operators, and HNSW / IVFFlat indexes. No table uses it at the v0.0 layer; the knowledge store adds the first embedding column.

Added by: [M03](../curriculum/03-backend-and-data-store.md)

## alembic_version

Purpose: Alembic's record of which migration the database is at.

| Column | Type | Description |
|---|---|---|
| version_num | varchar(32), PK | Current head revision; a single row |

No application tables exist at this layer; later modules add them as new migrations.

Added by: [M03](../curriculum/03-backend-and-data-store.md)

## model_calls (proposed)

Purpose: one row per logical gateway call, an app-queryable usage and cost ledger alongside the full trace in Langfuse. **Proposed** — only exists if M01's open question "where is per-call usage stored?" is answered with "Postgres table + Langfuse".

| Column | Type | Description |
|---|---|---|
| id | uuid | Primary key |
| created_at | timestamptz | Call start |
| caller | text | e.g. `tutor`, `lesson_builder` |
| tier | text | `strong` / `mid` / `fast` |
| model | text | Concrete model the tier resolved to |
| prompt_ref | text, null | Prompt name@version |
| input_tokens / output_tokens / cached_input_tokens | int | From the provider response |
| cost_usd | numeric | Estimate from the gateway's price table |
| latency_ms | int | Total, including retries |
| attempts | int | 1 = no retries |
| outcome | text | `ok` or the typed exception class name |
| trace_id | text, null | Link to the Langfuse trace |

Added by: [M01](../curriculum/01-model-gateway.md)
