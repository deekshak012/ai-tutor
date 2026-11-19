# ai-tutor

A generic, course-based AI tutor: slides, chat, voice, exercises, and homework feedback, adapting to how the learner performs. Full product spec: [docs/product-spec.md](docs/product-spec.md). Release plan: [docs/release-plan.md](docs/release-plan.md). Architecture: [docs/architecture/overview.md](docs/architecture/overview.md).

> **Project mode: read-to-understand (no code is built).** This is a learning project for Deeksha to understand *how* a system like this works by reading detailed explainer docs — not to build it. Claude (`doc-writer`, always `owner:agent`) authors the explainers in `docs/curriculum/`; Deeksha reads them and answers the check-your-understanding questions. There is no application code, no `backend/`/`frontend/`, no branches or PRs for code, and no `owner:deeksha`. The tech stack and architecture below are the *subject matter* the explainers describe, not something being implemented here. Start at the syllabus: [docs/curriculum/README.md](docs/curriculum/README.md).

## Architecture principles

- Use agents only where the next step can't be known in advance. Everything else is a fixed workflow or plain code.
- Agents (Course Planner, Researcher, Tutor) and workflows (Lesson Builder, Reviewer, Assessor) share state through the database, not by passing conversations to each other — [ADR 0001](docs/decisions/0001-agents-share-state-through-database.md).
- Expensive work (research, lesson building, review) happens ahead of the learner; only the Tutor runs live.
- Model tiers match the job. All model calls go through one internal gateway module.
- The knowledge store doubles as a cache.
- Every workflow has a defined input and output so it can be evaluated on its own.

## Tech stack

The stack the system is *designed around* — i.e. what the curriculum explainers describe. Nothing here is installed or built in this project.

- Backend: Python, FastAPI
- Database: Postgres + pgvector
- Frontend: React + TypeScript (Vite)
- Model calls: direct API calls through the internal gateway module — no agent frameworks at first ([ADR 0003](docs/decisions/0003-no-agent-frameworks-at-first.md))
- Tracing, prompt versioning, evals: Langfuse
- Testing/lint: pytest, ruff (+ frontend equivalent once the frontend exists)
- Containers: Docker

## Repo layout

```
docs/
  product-spec.md, release-plan.md
  architecture/overview.md
  data/guide.md            reference: tables/fields of the system being explained
  features/                (legacy) per-feature docs — superseded by curriculum/ in read-to-understand mode
  releases/                (legacy) per-version overviews — superseded by curriculum parts
  curriculum/              the read-to-understand syllabus: README.md + one explainer per module
  concepts/                standalone concept explainers, linked from curriculum modules
  decisions/                ADRs
  backlog/                 the curriculum backlog draft (module list)
  templates/                doc + concept + decision + release templates; curriculum-module template
learning-log.md            personal notes, mine to edit, not touched by Claude after creation
.claude/
  skills/                   backlog-writer (writes module issues), explain
  agents/                   reviewer, doc-writer (authors the explainers)
  settings.json             hooks
.github/
  ISSUE_TEMPLATE/feature.md
  pull_request_template.md
  workflows/ci.yml
```

There is no `backend/` or `frontend/` — no application code is written in this project.

## Coding conventions

No application code is written here, so these are dormant. If an explainer includes a short illustrative Python snippet, keep it readable and idiomatic; otherwise these don't apply.

## Read-to-understand rules

This project exists for Deeksha to **understand how a course-based AI tutor works by reading**, not to build one.

- Deeksha does not write code. Claude (`doc-writer`, `owner:agent`) authors a detailed explainer doc for each curriculum module; Deeksha reads it and answers the check-your-understanding questions.
- Every module explainer must make Deeksha come away understanding what the component is, how it works, how data flows, where data is stored, and every concept involved — with a Mermaid diagram and a worked example.
- The conceptually rich components (model gateway, agent loops, research, grounding, knowledge store, lesson builder, evals, voice, learner model) get deep dives; pure UI/plumbing gets shorter explainers.
- `owner:deeksha` no longer exists; there are no build tasks, branches, or code PRs.

## Workflow

1. Plan the curriculum in chat.
2. `backlog-writer` skill turns modules into GitHub issues (one per module, `owner:agent`, explainer-doc deliverable).
3. Pick a module issue. `doc-writer` authors the explainer at `docs/curriculum/NN-slug.md`.
4. `reviewer` checks the explainer for accuracy and that it matches the architecture/data references.
5. Deeksha reads it, answers the check-your-understanding questions, and closes the issue.

Every module ships its explainer doc — that *is* the deliverable.

## Hooks

- The `PostToolUse` ruff hook in `.claude/settings.json` is dormant (no `*.py` files are edited in this project). Harmless if left in place.

## Worktrees

Not applicable in read-to-understand mode (no parallel build work).
