# Architecture Overview

## Principles

- Use agents only where the next step can't be known in advance. Everything else is a fixed workflow or plain code.
- Agents share state through the database, not by passing conversations to each other. See [ADR 0001](../decisions/0001-agents-share-state-through-database.md).
- Expensive work (research, lesson building, review) happens ahead of the learner. Only the Tutor runs live.
- Model tiers match the job. All model calls go through one internal gateway module.
- The knowledge store doubles as a cache.
- Every workflow has a defined input and output so it can be evaluated on its own.

## Agents

Agents are used where the next step genuinely can't be known in advance.

- **Course Planner** (strongest model) — turns goal, context, and sources into a course plan; edits on request; replans after assessments.
- **Researcher** (mid-tier model) — finds, vets, and summarizes web information for upcoming concepts in the background, writing to the knowledge store.
- **Tutor** (fast model) — the live chat and voice conversation; decides when to answer, retrieve, search, show a figure, or start an exercise.

## Workflows

Workflows are fixed pipelines with a defined input and output, prepared ahead of the learner's session.

- **Lesson Builder** (mid-tier) — context packet in, validated slide data out.
- **Reviewer** (strong) — checks lessons for accuracy against sources and alignment with the course goal; sends them back for fixes.
- **Assessor** (mid-tier, vision when needed) — grades exercises, observation answers, and homework against rubrics.

## Services

- **Knowledge store** — content, concept tags, source type, verification status, date gathered, taught-to-learner status. Doubles as a cache.
- **Learner model** — statistics first, then a trained knowledge-tracing model.
- **Source ingestion** — background processing, relevance checks, concept extraction.

## Data flow

```mermaid
flowchart TB
    Learner((Learner))

    subgraph Agents
        CP[Course Planner]
        RS[Researcher]
        TU[Tutor]
    end

    subgraph Workflows
        LB[Lesson Builder]
        RV[Reviewer]
        AS[Assessor]
    end

    subgraph Services
        SI[Source Ingestion]
    end

    DB[(Postgres + pgvector:<br/>knowledge store, learner model,<br/>course plans, lessons)]
    GW[/Model Gateway/]

    Learner <--> TU
    TU --> DB
    TU --> GW

    CP --> DB
    CP --> GW
    RS --> DB
    RS --> GW
    SI --> DB

    LB --> DB
    LB --> GW
    RV --> DB
    RV --> GW
    RV -. sends back for fixes .-> LB
    AS --> DB
    AS --> GW

    TU -. reads lessons built ahead of time .-> DB
```

All agents and workflows read and write the shared database; none pass conversation state directly to one another. All model calls route through the gateway, regardless of which agent or workflow is calling.
