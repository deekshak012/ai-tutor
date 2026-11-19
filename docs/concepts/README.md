# Concepts

Standalone explainers for concepts used in the curriculum, created on demand by the `doc-writer` subagent and linked from `docs/curriculum/` modules. Start from `docs/templates/concept-doc-template.md`.

## Model calls (M01)
- [Gateway pattern](gateway-pattern.md) — one module the app owns wraps every call to the model provider.
- [Direct provider API calls](direct-provider-api-calls.md) — calling the provider's API or thin SDK with no framework in between.
- [Model tiers](model-tiers.md) — `strong` / `mid` / `fast` capability classes requested instead of model IDs.
- [Retries and backoff](retries-and-backoff.md) — repeating transient failures with growing, jittered delays.
- [Timeouts](timeouts.md) — an upper bound on how long a caller waits before treating a call as failed.
- [Token and cost accounting](token-and-cost-accounting.md) — per-call token counts converted to cost and attributed to a caller.

## Observability (M02)
- [Observability and tracing](observability-and-tracing.md) — answering "what did the system do?" from what it emits.
- [Spans](spans.md) — one timed step inside a trace.
- [Prompt versioning](prompt-versioning.md) — prompts as named artifacts with immutable versions, recorded on every call.

## Backend and data store (M03)
- [FastAPI app structure](fastapi-app-structure.md) — app object, routes, settings, dependency injection.
- [Postgres as the single store](postgres-as-single-store.md) — relational state, shared agent state and vectors in one database.
- [pgvector](pgvector.md) — the Postgres extension for embedding columns and similarity search.
- [Database migrations](database-migrations.md) — versioned, reversible schema changes.
- [Containerized local dev](containerized-local-dev.md) — running the stack's services in Docker from files in the repo.
- [Health checks](health-checks.md) — liveness vs readiness probes.

## Evaluation (M17, M18)
- [Offline evals](offline-evals.md) — scoring a model-driven component on a fixed dataset ahead of time.
- [Eval datasets](eval-datasets.md) — versioned lists of items with inputs and expectations.
- [I/O contracts](io-contracts.md) — the defined input and output that make a workflow evaluable on its own.
- [Regression thresholds](regression-thresholds.md) — the rule that turns scores into pass or fail.
- [Evals vs unit tests](evals-vs-unit-tests.md) — measuring stochastic behavior vs asserting deterministic behavior.
- [LLM-as-judge](llm-as-judge.md) — a model used as a scorer, and why it needs calibration.
- [Gold datasets](gold-datasets.md) — small, curated inputs with trusted expected outputs.
- [Fact-check design](fact-check-design.md) — self-contained claims with known verdicts, tagged to a topic.
- [Subject profiles](subject-profiles.md) — the kind of material a subject mostly consists of (text, visual, math, …).
