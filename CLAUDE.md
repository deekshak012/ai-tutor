# ai-tutor

A generic, course-based AI tutor: slides, chat, voice, exercises, and homework feedback, adapting to how the learner performs. Full product spec: [docs/product-spec.md](docs/product-spec.md). Release plan: [docs/release-plan.md](docs/release-plan.md). Architecture: [docs/architecture/overview.md](docs/architecture/overview.md).

## Architecture principles

- Use agents only where the next step can't be known in advance. Everything else is a fixed workflow or plain code.
- Agents (Course Planner, Researcher, Tutor) and workflows (Lesson Builder, Reviewer, Assessor) share state through the database, not by passing conversations to each other — [ADR 0001](docs/decisions/0001-agents-share-state-through-database.md).
- Expensive work (research, lesson building, review) happens ahead of the learner; only the Tutor runs live.
- Model tiers match the job. All model calls go through one internal gateway module.
- The knowledge store doubles as a cache.
- Every workflow has a defined input and output so it can be evaluated on its own.

## Tech stack

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
  data/guide.md            every table and field, filled in as features land
  features/                one doc per shipped feature
  concepts/                standalone concept explainers
  decisions/                ADRs
  backlog/                 written by the backlog-planner session, not here
  templates/                feature doc, concept doc, decision record templates
learning-log.md            personal notes, mine to edit, not touched by Claude after creation
.claude/
  skills/                   backlog-writer, explain
  agents/                   reviewer, doc-writer
  settings.json             hooks
.github/
  ISSUE_TEMPLATE/feature.md
  pull_request_template.md
  workflows/ci.yml
```

`backend/` and `frontend/` don't exist yet — they're scaffolded as v0.0 backlog work, not part of this setup.

## Coding conventions

- Python: ruff for lint and format, enforced by a post-edit hook (see Hooks below). Type hints throughout.
- All model calls go through the one internal gateway module — never call provider SDKs directly from agent or workflow code.
- Every agent/workflow has a documented input and output contract.
- Follow existing patterns in the repo; don't introduce a new library or abstraction for something one file already does.

## Learning-mode rules

This project exists for Deeksha to learn how to build these systems end to end, not to have them built for her.

- Deeksha writes the core AI pieces herself, with Claude as a pair programmer who explains and reviews, not a replacement author, for: the agent loops (Tutor, Course Planner, Researcher), retrieval and grounding, knowledge store design, the learner model and knowledge tracing, evals and judge calibration, and the core voice pipeline.
- Claude may build scaffolding, boilerplate, frontend wiring, infrastructure, and tests.
- For every feature, Deeksha must come away understanding what was built, how data is stored, and every concept used. This is why the `doc-writer` subagent exists and why every feature ships with docs.

## Workflow

1. Plan in chat.
2. `backlog-writer` skill turns decisions into GitHub issues.
3. Pick an issue. Implement on a branch named `feature/<ID>-<short-name>` (e.g. `feature/RET-02-hybrid-search`), or pair with Deeksha directly on `owner:deeksha` issues.
4. `doc-writer` subagent documents the change in the same PR.
5. `reviewer` subagent checks the code and docs. Hooks and CI run lint, tests, docs-check, and evals.
6. Deeksha reviews and merges. Merging closes the issue.

Every feature ships with docs in the same PR — no exceptions.

## Hooks

- `PostToolUse` on `Edit`/`Write`, filtered to `*.py` files via the hook's `if` field: runs `ruff format` then `ruff check` on the touched file. Configured in `.claude/settings.json`. Non-blocking (`onFailure: continue`) — it won't stop an edit, and no test suites run on every edit.
- Add the frontend equivalent (eslint/prettier or biome) once the frontend exists.

## Worktrees

Not set up yet. Introduce once there are independent issues to run in parallel, with a setup script handling per-worktree env vars, ports, and databases.
