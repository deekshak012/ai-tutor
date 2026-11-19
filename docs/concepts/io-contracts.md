# Concept: I/O contracts (defined input and output)

## What it is

An **I/O contract** is the agreed interface of an agent or workflow:

1. an **input schema**: everything the component needs, explicitly,
2. an **output schema**: the structured result it promises,
3. an **entry point**: one way to call it with an input and get an output (or a typed error).

It's the same idea as an API contract or a ServiceNow Flow Designer action's inputs/outputs, applied to model-driven components: the behavior inside can be stochastic, but the *shape* at the edges is fixed and validated.

## Why it matters here

The architecture principle *"every workflow has a defined input and output so it can be evaluated on its own"* ([architecture overview](../architecture/overview.md)) depends on this. Examples:

- **Lesson Builder:** context packet in, validated slide data out (LES-03).
- **Course Planner:** goal + context + include/skip topics in, plan hierarchy out (PLAN-01).
- **Reviewer:** lesson + sources + goal in, verdict + reasons out (LES-06).

[ADR 0001](../decisions/0001-agents-share-state-through-database.md) (shared state through the DB, not conversation passing) is what keeps these contracts *small*: a component's input is a defined slice of state, not "the whole transcript so far."

The eval runner ([M17](../curriculum/17-eval-runner.md)) is generic over contracts. It can evaluate any component that has one, and it scores `schema_valid` before anything else.

## How it works

- **Schemas are code** (e.g. Pydantic models in the Python backend). Model output is parsed and validated against the output schema. Invalid output is an error, not something to repair silently.
- **Isolation for evals:** because the input is explicit, a dataset item can provide it directly. You don't need to run the upstream components to evaluate the downstream one. A bad score points at one component.
- **Side effects:** if a component persists to the DB, the contract should make that separable (compute then persist), or evals need an ephemeral DB.
- **Versioning:** changing a contract is a breaking change for its datasets and its callers. Treat it like an API change.

Rejected alternative: evaluating only end to end. It's still useful as a final check, but it can't tell you which component regressed.

## Further reading

- [M17 — How the eval runner works](../curriculum/17-eval-runner.md)
- [M10 — Slide data contract](../curriculum/10-slide-data-contract.md)
- [ADR 0001](../decisions/0001-agents-share-state-through-database.md)
- "Design by contract" (Bertrand Meyer), the general software idea behind this
