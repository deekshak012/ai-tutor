# ai-tutor backlog draft

Status: **DRAFT for Deeksha's review.** v0.0 + v0.1 issues created in GitHub (#1–#20) and added to Project #1; later releases not yet created. Owner assignments, sizes, and priorities are my proposal; adjust freely. Each created feature below is marked with its issue number.

ID prefixes follow `.claude/skills/backlog-writer/SKILL.md`. Owner rule applied: `owner:deeksha` for the core-AI learning pieces (agent loops — Tutor/Course Planner/Researcher; retrieval & grounding; knowledge store design; learner model & knowledge tracing; evals & judge calibration; core voice pipeline); `owner:agent` for scaffolding, boilerplate, frontend wiring, infrastructure, and tests. Workflows (Lesson Builder, Reviewer, Assessor) default to `owner:agent` except the sub-parts that embody grounding, judge calibration, or the learner model, which go to Deeksha.

## Definition of Done (applies to every story)

Every feature below — regardless of owner — ships with these in the same PR. They are **not** repeated in each story's acceptance criteria; they are standing requirements the backlog-writer skill attaches to every issue:

- **A learning doc** by `doc-writer` at `docs/features/<ID>-<slug>.md` so Deeksha can understand what's going on: what & why, how it works (with file/function refs), a Mermaid data-flow diagram, data stored, concepts used (linked to concept explainers), design decisions + rejected alternatives, how to run & test, and a **"check your understanding"** section.
- `docs/data/guide.md` / `docs/architecture/overview.md` updated when data or architecture changes.
- Tests added/updated and passing; evals run where relevant.
- `reviewer` subagent run, confirming the doc matches the actual code.

Enforced by: CLAUDE.md ("every feature ships with docs — no exceptions"), the CI docs-check, the PR template, and the feature issue template's Definition-of-Done block.

**Per release (not per story):** when a version's stories are all merged, `doc-writer` writes a per-version overview at `docs/releases/<version>.md` — a higher-altitude "what this release adds and how the pieces connect" companion to the individual feature docs, with an end-to-end walkthrough and a release-level "check your understanding".

## Summary

| Release | Features | Theme |
|---|---|---|
| v0.0 | 5 | Foundations: gateway, tracing, eval runner, test courses |
| v0.1 | 15 | Thin end-to-end slice (create → outline → one researched slide lesson + chat) + E2E/test tooling |
| v0.2 | 13 | Memory & context: knowledge store, retrieval, context packets, reviewer |
| v0.3 | 8 | Optional sources: uploads, relevance, ingestion, source-grounded retrieval |
| v0.4 | 9 | Exercises & tracking: placement, exercises, grading, mastery |
| v0.5 | 5 | Voice |
| v1.0 | 7 | Adaptive & deployed: retention, adaptive sequencing, dashboard, deploy |
| v1.5 | 4 | Homework |
| v2.x | 6 | Hardening: trained KT model, routing, cost, multi-agent, study |
| **Total** | **72** | |

| Epic | Count | Epic | Count |
|---|---|---|---|
| E0 Platform (PLAT) | 4 | E8 Tutor & Chat (TUT) | 3 |
| E1 Courses (CRS) | 2 | E9 Exercises (EX) | 5 |
| E2 Course Planner (PLAN) | 4 | E10 Voice (VOI) | 5 |
| E3 Research & Web (RES) | 5 | E11 Learner Model (LRN) | 6 |
| E4 Knowledge Store (KS) | 4 | E12 Homework (HW) | 4 |
| E5 Sources & Ingestion (SRC) | 7 | E13 Quality & Evals (QA) | 4 |
| E6 Retrieval & Grounding (RET) | 5 | E14 Optimization (OPT) | 4 |
| E7 Lessons (LES) | 6 | E15 Dev Tooling & Docs (DEV) | 4 |

**Owner split (proposed):** ~38 `owner:deeksha`, ~34 `owner:agent`. The core AI surface (agents, retrieval/grounding, knowledge store, learner model, evals, voice, judge calibration) lands with you; UI, ingestion plumbing, slide rendering, test tooling, and infra land with the agent.

**Build order for the first two releases** (v0.0 → v0.1):
PLAT-01 → PLAT-02 → PLAT-03, QA-01 → QA-02, then DEV-01, CRS-01 → CRS-02, PLAN-01 → PLAN-02, RES-01 → RES-02, LES-01 → LES-02 → LES-03 (uses RET-03), TUT-01 → TUT-02.

---

## E0 — Platform and Infrastructure (PLAT)

### PLAT-01 — Backend skeleton + Postgres/pgvector + Docker · **Issue [#1](https://github.com/deekshak012/ai-tutor/issues/1)**
- **Release:** v0.0 · **Owner:** owner:agent (infrastructure/scaffolding) · **Size:** M
- **Description:** FastAPI app skeleton, config/settings, Dockerfile + docker-compose with Postgres + pgvector, migrations tooling, health check. The substrate every later feature builds on.
- **Owns (arch):** none (platform).
- **Acceptance criteria:** `docker compose up` starts API + Postgres with pgvector enabled; `/health` returns 200; migrations run clean; ruff + pytest wired and green on an empty suite.
- **Dependencies:** none.
- **Concepts:** FastAPI app structure, pgvector extension, containerized local dev.
- **Required eval:** n/a (no model call).

### PLAT-02 — Model gateway module (tiered routing) · **Issue [#2](https://github.com/deekshak012/ai-tutor/issues/2)**
- **Release:** v0.0 · **Owner:** owner:deeksha (foundation of the hand-built, no-framework model calls she wants to learn — ADR 0003) · **Size:** M
- **Description:** The single module all model calls route through. Direct API calls (no agent framework), model-tier selection (strong/mid/fast), retries/timeouts, token+cost capture, and a seam for Langfuse tracing.
- **Owns (arch):** the "one internal gateway module."
- **Acceptance criteria:** every model call in the codebase goes through the gateway (enforced by a lint/grep check); tiers selectable per call; a forced API error surfaces a typed exception; usage is recorded per call.
- **Dependencies:** PLAT-01.
- **Concepts:** direct provider API calls, model tiering, retries/backoff, the gateway pattern.
- **Required eval:** a smoke eval that each tier returns a well-formed completion for a fixed prompt.

### PLAT-03 — Langfuse tracing wired into the gateway · **Issue [#3](https://github.com/deekshak012/ai-tutor/issues/3)**
- **Release:** v0.0 · **Owner:** owner:agent (integration wiring; Deeksha reads the traces) · **Size:** S
- **Description:** Every gateway call emits a Langfuse trace/span with prompt version, tier, tokens, cost, and latency.
- **Owns (arch):** tracing cross-cut.
- **Acceptance criteria:** a model call produces a trace visible in Langfuse with tier, token, and latency fields; prompt version is attached.
- **Dependencies:** PLAT-02.
- **Concepts:** tracing/observability, prompt versioning.
- **Required eval:** n/a (verified by trace presence).

### PLAT-04 — Production deployment
- **Release:** v1.0 · **Owner:** owner:agent (infrastructure) · **Size:** L
- **Description:** Deploy API + frontend + Postgres to a hosting target, with env/secret management, migrations on deploy, and basic monitoring.
- **Acceptance criteria:** a tagged release deploys end to end; secrets are not in the repo; a smoke test passes against the deployed URL.
- **Dependencies:** PLAT-01, DEV-01, and a working v0.1 slice.
- **Concepts:** containerized deploy, secret management, migrations in CI/CD.
- **Required eval:** post-deploy smoke eval (create a course, build one lesson) against production.

---

## E13 — Quality and Evals (QA)

### QA-01 — Eval runner · **Issue [#4](https://github.com/deekshak012/ai-tutor/issues/4)**
- **Release:** v0.0 · **Owner:** owner:deeksha (evals are a core learning piece) · **Size:** M
- **Description:** A runner that takes a dataset + a workflow's defined input/output contract and produces scored results through Langfuse. The harness every per-feature eval plugs into.
- **Owns (arch):** evals cross-cut; enforces "every workflow has a defined input/output."
- **Acceptance criteria:** runner executes a dataset against a target workflow, records scores + traces in Langfuse, and exits non-zero on regression below a threshold; a placeholder dataset runs in CI (replaces the CI eval placeholder job).
- **Dependencies:** PLAT-02, PLAT-03.
- **Concepts:** offline evals, datasets, regression thresholds, defined I/O contracts.
- **Required eval:** self-test on a trivial fixture workflow.

### QA-02 — Three test courses (expected topics + fact checks) · **Issue [#5](https://github.com/deekshak012/ai-tutor/issues/5)**
- **Release:** v0.0 · **Owner:** owner:deeksha (eval dataset + judge-calibration foundation; she picks the courses) · **Size:** M
- **Description:** Define three courses spanning different subjects/goals, each with hand-written expected topics and fact checks, used as the backbone eval set across releases. **Proposed (replace any):** (1) *Intro Statistics for a data analyst* (math/text — hypothesis testing, regression basics); (2) *Reading financial statements* (text/visual/business — analyze a 10-K); (3) *Fundamentals of music theory* (visual/notation — read sheet music, analyze chord progressions). These span math, text/visual, and notation/visual to exercise subject profiling and ingestion later.
- **Acceptance criteria:** three course definitions committed with goal, context, expected topic list, and ≥5 fact checks each; wired as a dataset the eval runner can execute.
- **Dependencies:** QA-01.
- **Concepts:** gold datasets, fact-check design, coverage across subject profiles.
- **Required eval:** this *is* eval data; validated by the runner consuming it.

### QA-03 — LLM-as-judge harness + calibration against Deeksha's labels
- **Release:** v0.4 · **Owner:** owner:deeksha (judge calibration is a named core learning piece) · **Size:** M
- **Description:** A reusable judge for grading free-form answers/exercises, calibrated against a set of Deeksha's own labels, with agreement metrics.
- **Acceptance criteria:** judge produces scores on a labeled set; inter-rater agreement (judge vs Deeksha) is reported; calibration prompt/version tracked.
- **Dependencies:** QA-01, EX-05.
- **Concepts:** LLM-as-judge, calibration, inter-rater agreement.
- **Required eval:** agreement metric meets an agreed threshold on the held-out labels.

### QA-05 — Learning-outcome study
- **Release:** v2.x · **Owner:** owner:deeksha (evaluation/research) · **Size:** L
- **Description:** Measure whether the tutor actually improves learning outcomes (pre/post, retention) across the test courses.
- **Acceptance criteria:** a study design + results doc with pre/post and retention metrics.
- **Dependencies:** LRN-03, LRN-05.
- **Concepts:** outcome measurement, retention, study design.
- **Required eval:** the study itself.

---

## E15 — Dev Tooling and Docs (DEV)

### DEV-01 — Frontend skeleton (React + TS + Vite) · **Issue [#6](https://github.com/deekshak012/ai-tutor/issues/6)**
- **Release:** v0.1 · **Owner:** owner:agent (frontend wiring) · **Size:** M
- **Description:** Vite React+TS app shell, routing, API client, lint/format (eslint/prettier or biome), and the frontend post-edit hook noted in CLAUDE.md.
- **Acceptance criteria:** app builds and serves; calls the backend health endpoint; lint/format run in CI; frontend hook added to `.claude/settings.json`.
- **Dependencies:** PLAT-01.
- **Concepts:** Vite/React app structure, API client wiring.
- **Required eval:** n/a.

### DEV-02 — Worktree setup script
- **Release:** v1.0 (introduce once independent issues run in parallel) · **Owner:** owner:agent (tooling) · **Size:** S
- **Description:** Per-worktree env vars, ports, and database setup script, per the CLAUDE.md Worktrees note.
- **Acceptance criteria:** script spins up an isolated worktree env (distinct port + DB) and tears it down.
- **Dependencies:** PLAT-01.
- **Concepts:** git worktrees, env isolation.
- **Required eval:** n/a.

### DEV-03 — Playwright E2E harness + `e2e-tester` subagent · **Issue [#20](https://github.com/deekshak012/ai-tutor/issues/20)**
- **Release:** v0.1 (when the frontend first lands) · **Owner:** owner:agent (test tooling) · **Size:** M
- **Description:** Browser-based end-to-end testing with Playwright for the real user flows — course creation, outline view/edit, slide rendering, and the chat panel — plus an `e2e-tester` subagent that drives these flows and flags flakiness. Runs in CI. Timed to v0.1 because there is no frontend to test before then (DEV-01). Scope grows with the UI (voice flows in v0.5, dashboard in v1.0).
- **Owns (arch):** E2E test layer (complements unit tests + evals).
- **Acceptance criteria:** Playwright installed + configured; E2E specs cover create-course → outline → one slide lesson → chat; a `.claude/agents/e2e-tester.md` subagent (read-only on app code, allowed to run Playwright) can execute the flows and report pass/fail + flakiness; E2E job added to CI.
- **Dependencies:** DEV-01, CRS-02, PLAN-02, LES-02, TUT-02.
- **Concepts:** E2E/browser testing, Playwright, test flakiness, the unit-vs-eval-vs-E2E split.
- **Required eval:** n/a (this is the test layer; verified by the suite running green in CI).

### DEV-04 — `test-writer` subagent for pytest (optional) · **Issue [#7](https://github.com/deekshak012/ai-tutor/issues/7)**
- **Release:** v0.1 · **Owner:** owner:agent (test tooling) · **Size:** S
- **Description:** Optional subagent that drafts/extends pytest unit tests for deterministic logic. Complements — does not replace — the implementer (who writes tests today) and the `reviewer` (who verifies them). Model-dependent behavior stays with evals (QA-01), not unit tests. Only build this if the implementer+reviewer+CI loop proves insufficient.
- **Acceptance criteria:** a `.claude/agents/test-writer.md` subagent produces pytest tests for a target module that pass and raise coverage; it never edits application code, only tests.
- **Dependencies:** PLAT-01.
- **Concepts:** unit testing discipline, test/code separation, coverage.
- **Required eval:** n/a.

---

## E1 — Courses (CRS)

### CRS-01 — Course data model + create/read API · **Issue [#8](https://github.com/deekshak012/ai-tutor/issues/8)**
- **Release:** v0.1 · **Owner:** owner:agent (CRUD scaffolding) · **Size:** M
- **Description:** Course entity + API capturing all creation fields: learning goal, why/motivation, current level (self-reported in v0.1; confirmed by placement quiz in v0.4 — see EX-01), target outcome, time/week, deadline, preferred style, include/skip topics, and the per-course web mode (sources-only vs sources+web).
- **Owns (arch):** Course object (top of the hierarchy).
- **Acceptance criteria:** create + read a course with every field persisted; web-mode defaults to sources+web; validation on required fields; row visible in `docs/data/guide.md`.
- **Dependencies:** PLAT-01.
- **Concepts:** the course as central object (ADR 0002), schema design.
- **Required eval:** n/a (no model call).

### CRS-02 — Course creation UI · **Issue [#9](https://github.com/deekshak012/ai-tutor/issues/9)**
- **Release:** v0.1 · **Owner:** owner:agent (frontend wiring) · **Size:** M
- **Description:** The guided form for creating a course and setting all fields from CRS-01.
- **Acceptance criteria:** form creates a course via the API; validation + error states; web-mode toggle present.
- **Dependencies:** CRS-01, DEV-01.
- **Concepts:** form UX, controlled inputs.
- **Required eval:** n/a.

---

## E2 — Course Planner (PLAN)

### PLAN-01 — Course Planner agent (goal → skill map → modules → lessons) · **Issue [#10](https://github.com/deekshak012/ai-tutor/issues/10)**
- **Release:** v0.1 · **Owner:** owner:deeksha (agent loop — core learning) · **Size:** L
- **Description:** The strongest-tier agent that turns goal + context into a course plan: a skill map decomposed into modules and lesson outlines. Writes the plan to the DB (shared-state, ADR 0001).
- **Owns (arch):** Course Planner agent.
- **Acceptance criteria:** given a test-course goal+context, produces a valid hierarchy (goal → plan → modules → lessons) persisted to the DB; plan validates against a schema; respects include/skip topics.
- **Dependencies:** CRS-01, PLAT-02, QA-01.
- **Concepts:** agent loop, planning/decomposition, skill maps, structured output.
- **Required eval:** plan covers the expected topics for each test course (QA-02) above a coverage threshold; no skipped topics appear.

### PLAN-02 — Course outline view/edit UI · **Issue [#11](https://github.com/deekshak012/ai-tutor/issues/11)**
- **Release:** v0.1 · **Owner:** owner:agent (frontend wiring) · **Size:** M
- **Description:** View and edit the generated outline (reorder/rename/add/remove modules & lessons) at any time.
- **Acceptance criteria:** outline renders the hierarchy; edits persist; planner regeneration doesn't silently discard manual edits.
- **Dependencies:** PLAN-01, DEV-01.
- **Concepts:** tree editing UX, optimistic updates.
- **Required eval:** n/a.

### PLAN-03 — Replan after assessments (adaptive sequencing)
- **Release:** v1.0 · **Owner:** owner:deeksha (agent loop + learner model) · **Size:** L
- **Description:** Planner adjusts the plan based on mastery results (reorder, insert remediation, skip mastered concepts).
- **Acceptance criteria:** given mastery deltas, planner produces a revised plan with a diff + rationale; mastered concepts are not re-taught.
- **Dependencies:** PLAN-01, LRN-01, LRN-04.
- **Concepts:** adaptive sequencing, replanning.
- **Required eval:** on a simulated learner, replanning improves next-assessment coverage vs a fixed plan.

### PLAN-04 — Edit-on-request (conversational plan edits)
- **Release:** v1.0 · **Owner:** owner:deeksha (agent loop) · **Size:** M
- **Description:** The user asks the planner, in natural language, to change the plan ("add more on X", "go faster on Y").
- **Acceptance criteria:** a natural-language request yields a correct, validated plan change the user can accept/reject.
- **Dependencies:** PLAN-01, PLAN-02.
- **Concepts:** intent → structured edit, human-in-the-loop.
- **Required eval:** a set of request→expected-change cases pass above a threshold.

---

## E3 — Research and Web (RES)

### RES-01 — Researcher agent (search, fetch, summarize, cite) · **Issue [#13](https://github.com/deekshak012/ai-tutor/issues/13)**
- **Release:** v0.1 · **Owner:** owner:deeksha (agent loop + grounding — core learning) · **Size:** L
- **Description:** Mid-tier agent that searches the web for a concept, fetches pages, summarizes (not copies), and returns claims each linked to a source URL. In v0.1 it feeds the Lesson Builder directly; background scheduling + KS writes come in v0.2 (RES-05).
- **Owns (arch):** Researcher agent.
- **Acceptance criteria:** for a concept, returns summarized claims with source URLs; content is summarized, not pasted verbatim; output is a structured, citeable object.
- **Dependencies:** PLAT-02, RES-02.
- **Concepts:** agent loop, web search/fetch, summarization, citation.
- **Required eval:** on fixed concepts, claims are supported by their cited source (judge or fact-check) above a threshold.

### RES-02 — Web content as data / prompt-injection defense (+ tests) · **Issue [#12](https://github.com/deekshak012/ai-tutor/issues/12)**
- **Release:** v0.1 (minimal; deepened in v0.3) · **Owner:** owner:deeksha (grounding discipline she must understand) · **Size:** M
- **Description:** Treat all fetched web content strictly as data, never as instructions. Wrapping/escaping + a test suite of injection attempts.
- **Owns (arch):** safety cross-cut for research/ingestion.
- **Acceptance criteria:** a suite of injection payloads (e.g. "ignore previous instructions") in fetched content does not alter model behavior; tests are part of CI.
- **Dependencies:** PLAT-02.
- **Concepts:** prompt injection, data/instruction separation, adversarial testing.
- **Required eval:** injection test suite passes (0 successful injections).

### RES-03 — Source quality scoring + filtering
- **Release:** v0.2 · **Owner:** owner:deeksha (grounding) · **Size:** M
- **Description:** Score web sources for quality and filter low-quality ones before they inform lessons/answers.
- **Acceptance criteria:** low-quality sources are down-ranked/filtered on a labeled set; scores stored with the source.
- **Dependencies:** RES-01, KS-01.
- **Concepts:** source credibility signals, filtering.
- **Required eval:** precision/recall of filtering on a hand-labeled source set above a threshold.

### RES-04 — Conflict detection (show both views + explain)
- **Release:** v0.2 · **Owner:** owner:deeksha (grounding) · **Size:** M
- **Description:** When sources disagree, surface both views and explain the difference rather than silently picking one.
- **Acceptance criteria:** on constructed conflicting sources, output presents both positions + an explanation of the difference.
- **Dependencies:** RES-01, KS-01.
- **Concepts:** disagreement detection, balanced synthesis.
- **Required eval:** conflict cases are flagged (not collapsed) above a threshold.

### RES-05 — Background research scheduling (writes to knowledge store)
- **Release:** v0.2 · **Owner:** owner:deeksha (agent loop + knowledge store) · **Size:** M
- **Description:** Researcher runs ahead of the learner for upcoming concepts and writes results to the knowledge store (expensive work happens ahead of time).
- **Acceptance criteria:** upcoming concepts trigger background research; results land in the KS with verification status + citations; the Tutor reads them later without live search.
- **Dependencies:** RES-01, KS-01, KS-02, PLAN-01.
- **Concepts:** background jobs, work-ahead pipeline, shared-state (ADR 0001).
- **Required eval:** KS is pre-populated for a plan's next N concepts before the lesson is requested.

---

## E4 — Knowledge Store (KS)

### KS-01 — Knowledge store schema + read/write
- **Release:** v0.2 · **Owner:** owner:deeksha (knowledge store design — core learning) · **Size:** L
- **Description:** The store for everything researched/taught: content, concept tags, source type (uploaded/web/model-generated), verification status (grounded/checked/unverified), date gathered, taught-to-this-learner flag.
- **Owns (arch):** Knowledge store service.
- **Acceptance criteria:** write/read entries with all fields; concept-tag and source-type queries; documented in `docs/data/guide.md`.
- **Dependencies:** PLAT-01.
- **Concepts:** knowledge store design, provenance, verification states.
- **Required eval:** n/a (schema); exercised by RES-05/RET evals.

### KS-02 — Trust rules (model-generated stays unverified until checked)
- **Release:** v0.2 · **Owner:** owner:deeksha (knowledge store design) · **Size:** M
- **Description:** Enforce that model-generated content never becomes trusted without being checked against real sources; manage status transitions unverified → checked → grounded.
- **Acceptance criteria:** model-generated entries start unverified; promotion requires a source check; untrusted content is excluded from grounded answers.
- **Dependencies:** KS-01.
- **Concepts:** verification workflow, trust boundaries.
- **Required eval:** no unverified model content appears in a grounded answer across the test set.

### KS-03 — Cross-course/user sharing + privacy
- **Release:** v0.2 · **Owner:** owner:deeksha (knowledge store design) · **Size:** M
- **Description:** Verified general knowledge is shareable across courses/users; learner notes, mistakes, and progress stay private to the learner.
- **Acceptance criteria:** a verified general fact is reusable by another course; learner-private data is never returned in a cross-course/user query.
- **Dependencies:** KS-01, KS-02. **Open question:** depends on the auth/user-identity decision (see Gaps).
- **Concepts:** data scoping, privacy boundaries, knowledge reuse.
- **Required eval:** privacy test — learner-private rows never leak across users.

### KS-04 — Cache behavior (store doubles as cache)
- **Release:** v0.2 · **Owner:** owner:deeksha (knowledge store design) · **Size:** S
- **Description:** Look up the KS before re-researching; dedupe equivalent content so the store doubles as a cache.
- **Acceptance criteria:** a repeated concept request is served from the KS without a new web search; dedupe prevents duplicate entries.
- **Dependencies:** KS-01, RES-05.
- **Concepts:** caching, deduplication, cache-as-store.
- **Required eval:** cache-hit rate measured on repeated concepts.

---

## E6 — Retrieval and Grounding (RET)

### RET-03 — Grounded answers with citations + source-type labels · **Issue [#14](https://github.com/deekshak012/ai-tutor/issues/14)**
- **Release:** v0.1 · **Owner:** owner:deeksha (grounding — core learning) · **Size:** M
- **Description:** Assemble grounded output where every claim links to its source and is labeled by source type (uploaded/web/model). In v0.1 grounding draws directly from Researcher output; vector retrieval arrives in v0.2.
- **Owns (arch):** grounding cross-cut for lessons + chat.
- **Acceptance criteria:** lesson/chat claims carry a citation + source-type label; unsupported claims are flagged or withheld.
- **Dependencies:** RES-01.
- **Concepts:** grounding, citations, source-type labeling.
- **Required eval:** claim-support rate (judge/fact-check) above a threshold on the test courses.

### RET-01 — Embeddings + vector index (pgvector)
- **Release:** v0.2 · **Owner:** owner:deeksha (retrieval — core learning) · **Size:** M
- **Description:** Embed knowledge-store/source content and index it in pgvector for semantic retrieval.
- **Acceptance criteria:** content is embedded on write; nearest-neighbor query returns relevant items; index documented in the data guide.
- **Dependencies:** KS-01, PLAT-01.
- **Concepts:** embeddings, vector search, pgvector.
- **Required eval:** retrieval relevance (hit@k) on a labeled query set above a threshold.

### RET-02 — Context packet assembler
- **Release:** v0.2 · **Owner:** owner:deeksha (retrieval & grounding — core learning) · **Size:** L
- **Description:** Build the compact per-lesson context packet (never full history): course goal + user context, module objective, lesson concepts + prerequisites, learner mastery for those concepts, rolling summary of what's been taught, and relevant KS/source items.
- **Owns (arch):** the context packet.
- **Acceptance criteria:** given a lesson, produces a packet with all sections within a token budget; omits unrelated history; deterministic given the same state.
- **Dependencies:** RET-01, KS-01, RET-04; reads mastery from LRN-01 when available.
- **Concepts:** context engineering, packet construction, token budgeting.
- **Required eval:** packet completeness + size checks; downstream lesson quality vs full-history baseline.

### RET-04 — Rolling lesson summary
- **Release:** v0.2 · **Owner:** owner:deeksha (grounding/continuity — core learning) · **Size:** S
- **Description:** Maintain a rolling summary of what's been taught, for continuity and for the context packet.
- **Acceptance criteria:** summary updates after each lesson; stays within a size bound; lessons reference earlier material via it.
- **Dependencies:** KS-01, LES-03.
- **Concepts:** rolling summarization, continuity.
- **Required eval:** summary faithfulness (judge) above a threshold.

### RET-05 — Hybrid search (keyword + vector)
- **Release:** v0.3 · **Owner:** owner:deeksha (retrieval — core learning) · **Size:** M
- **Description:** Combine keyword and vector retrieval over sources + KS once uploads exist.
- **Acceptance criteria:** hybrid retrieval beats vector-only on the labeled query set; citations preserved.
- **Dependencies:** RET-01, SRC-02.
- **Concepts:** hybrid/lexical+semantic retrieval, fusion ranking.
- **Required eval:** hit@k improvement over RET-01 baseline.

---

## E7 — Lessons (LES)

### LES-01 — Slide data schema + validation · **Issue [#15](https://github.com/deekshak012/ai-tutor/issues/15)**
- **Release:** v0.1 · **Owner:** owner:agent (scaffolding) · **Size:** S
- **Description:** The structured slide contract (title, images, text, speaker notes, slide type) + validation the Lesson Builder must satisfy.
- **Acceptance criteria:** schema defined; invalid slide data is rejected with clear errors; documented in the data guide.
- **Dependencies:** PLAT-01.
- **Concepts:** schema/contract design, validation.
- **Required eval:** n/a.

### LES-02 — Slide renderer (frontend) · **Issue [#16](https://github.com/deekshak012/ai-tutor/issues/16)**
- **Release:** v0.1 · **Owner:** owner:agent (frontend wiring) · **Size:** M
- **Description:** Render structured slide data into the slide view (per slide type), with the chat panel beside it.
- **Acceptance criteria:** renders each slide type; handles images + speaker notes; responsive.
- **Dependencies:** LES-01, DEV-01.
- **Concepts:** rendering structured content, slide layouts.
- **Required eval:** n/a.

### LES-03 — Lesson Builder workflow (context packet → validated slide data) · **Issue [#17](https://github.com/deekshak012/ai-tutor/issues/17)**
- **Release:** v0.1 · **Owner:** owner:agent (workflow; Deeksha pairs on the generation prompt, which touches grounding) · **Size:** L
- **Description:** Mid-tier workflow: context packet in, validated slide data out, prepared ahead of the learner. In v0.1 the packet is thin (goal + concept + Researcher output).
- **Owns (arch):** Lesson Builder workflow.
- **Acceptance criteria:** produces schema-valid slides for a concept with citations (via RET-03); defined input/output for eval; runs offline/ahead of time.
- **Dependencies:** LES-01, RES-01, RET-03, PLAT-02.
- **Concepts:** workflow with defined I/O, structured generation, grounding handoff.
- **Required eval:** slide accuracy vs test-course fact checks + citation-support rate above thresholds.

### LES-04 — Lesson pause/resume
- **Release:** v0.2 · **Owner:** owner:agent (state/scaffolding) · **Size:** S
- **Description:** Pause a lesson and resume later at the same slide/state.
- **Acceptance criteria:** pausing persists position + context; resuming restores it.
- **Dependencies:** LES-02, LES-03.
- **Concepts:** session state persistence.
- **Required eval:** n/a.

### LES-05 — Lesson images + teaching-diagram generation (no AI art)
- **Release:** v0.2 · **Owner:** owner:agent (workflow/rendering; enforces ADR 0004) · **Size:** L
- **Description:** Source images from course sources first, then web; when none fit, generate teaching diagrams **as code** (flowcharts, labeled illustrations, concept maps). Enforce the hard rule: generation only to teach, never AI art for end use (ADR 0004).
- **Acceptance criteria:** images preferred from sources→web; diagrams render from generated code; a guard prevents decorative/AI-art generation; source images carry provenance.
- **Dependencies:** LES-03, RET-01 (image/source lookup).
- **Concepts:** diagram-as-code, image provenance, the no-AI-art boundary.
- **Required eval:** on diagram-worthy concepts, a valid teaching diagram is produced; no end-use art generated (checked).

### LES-06 — Goal-alignment + accuracy Reviewer workflow
- **Release:** v0.2 · **Owner:** owner:agent (workflow; depends on grounding owned by RET) · **Size:** L
- **Description:** Strong-tier Reviewer that checks each module/lesson for accuracy against sources and alignment with the course goal, and sends failing lessons back for fixes.
- **Owns (arch):** Reviewer workflow.
- **Acceptance criteria:** flags off-goal or unsupported lessons with reasons; a flagged lesson re-enters the builder; defined input/output.
- **Dependencies:** LES-03, RET-02, RET-03, PLAN-01.
- **Concepts:** review/verification workflow, goal alignment, accuracy-vs-source checks.
- **Required eval:** reviewer catches seeded inaccuracies/off-goal lessons above a threshold (recall) with bounded false positives.

---

## E8 — Tutor and Chat (TUT)

### TUT-01 — Tutor agent loop (slide-aware; answer/retrieve) · **Issue [#18](https://github.com/deekshak012/ai-tutor/issues/18)**
- **Release:** v0.1 · **Owner:** owner:deeksha (agent loop — core learning) · **Size:** L
- **Description:** The fast-tier live agent for chat. Knows the current slide; decides when to answer directly vs retrieve. (Search / figure / exercise actions added in TUT-03.)
- **Owns (arch):** Tutor agent (the only live component).
- **Acceptance criteria:** answers slide-aware questions grounded in lesson/KS content with citations; decides answer-vs-retrieve; runs within a live latency budget.
- **Dependencies:** PLAT-02, RET-03; LES-03 for lesson context.
- **Concepts:** agent loop, tool/action selection, slide-aware context, grounding.
- **Required eval:** answer accuracy + citation-support on a slide-grounded Q&A set above thresholds.

### TUT-02 — Chat UI (slide-aware; tangents + return) · **Issue [#19](https://github.com/deekshak012/ai-tutor/issues/19)**
- **Release:** v0.1 · **Owner:** owner:agent (frontend wiring) · **Size:** M
- **Description:** Chat panel beside the slides that knows the current slide, supports tangents and returning to the lesson.
- **Acceptance criteria:** chat shows current-slide awareness; can branch into a tangent and return; history persists.
- **Dependencies:** TUT-01, LES-02, DEV-01.
- **Concepts:** conversational UI, context indicators.
- **Required eval:** n/a.

### TUT-03 — Tutor actions: retrieve/search/show figure/start exercise
- **Release:** v0.4 · **Owner:** owner:deeksha (agent loop — core learning) · **Size:** L
- **Description:** Extend the Tutor's decision loop to also live-search, show a figure, and start an exercise when appropriate.
- **Acceptance criteria:** the Tutor selects the right action on a labeled set (answer vs search vs figure vs exercise); exercise launches hand off to EX.
- **Dependencies:** TUT-01, RES-01, EX-02/EX-03.
- **Concepts:** action selection/routing, tool use.
- **Required eval:** action-selection accuracy on labeled scenarios above a threshold.

---

## E5 — Sources and Ingestion (SRC)

### SRC-01 — Upload intake + storage (all source types)
- **Release:** v0.3 · **Owner:** owner:agent (infrastructure) · **Size:** M
- **Description:** Upload + store every source type: books (PDF/EPUB), articles/web links, video/lecture transcripts, notes/class slides, syllabus, past exams/practice questions, admired-work examples, own-work samples, glossaries/reference sheets. No feature assumes a source exists (ADR 0002).
- **Acceptance criteria:** each type uploads + stores with metadata; a course runs unchanged with zero sources.
- **Dependencies:** PLAT-01.
- **Concepts:** file storage, source typing.
- **Required eval:** n/a.

### SRC-02 — Parsing per source type (background)
- **Release:** v0.3 · **Owner:** owner:agent (infrastructure; Deeksha pairs where parsing feeds grounding) · **Size:** L
- **Description:** Background processing to extract text/structure per type (PDF/EPUB text, transcript segments, slides, etc.).
- **Acceptance criteria:** each type yields normalized, chunked content ready for embedding; failures are isolated per source.
- **Dependencies:** SRC-01.
- **Concepts:** background processing, parsing/chunking.
- **Required eval:** extraction coverage on sample files above a threshold.

### SRC-03 — Subject profile detection
- **Release:** v0.3 · **Owner:** owner:agent (classification workflow; Deeksha pairs on the prompt) · **Size:** M
- **Description:** Classify each source's profile (text-heavy/visual/math/code/diagrams/mixed) to guide parsing, question types, and homework formats.
- **Acceptance criteria:** profiles assigned on a labeled sample above an accuracy threshold; profile drives downstream question/homework choices.
- **Dependencies:** SRC-02.
- **Concepts:** content classification, profile-driven behavior.
- **Required eval:** classification accuracy on labeled sources.

### SRC-04 — Relevance check (advisory, never blocks)
- **Release:** v0.3 · **Owner:** owner:agent (workflow; Deeksha pairs on prompt) · **Size:** M
- **Description:** Advise relevant / partly relevant (naming which chapters/sections fit) / not relevant, plus a level-mismatch warning. The user always decides.
- **Acceptance criteria:** verdicts produced with chapter/section detail for partial; level-mismatch warning shown; never blocks use.
- **Dependencies:** SRC-02.
- **Concepts:** relevance assessment, advisory UX.
- **Required eval:** relevance verdicts agree with labels above a threshold.

### SRC-05 — Conceptual ingestion (extract to knowledge store)
- **Release:** v0.3 · **Owner:** owner:deeksha (feeds knowledge store + grounding — core learning) · **Size:** L
- **Description:** From conceptual material, extract definitions, arguments, claims + evidence, examples, and how ideas connect; write to the KS with provenance.
- **Acceptance criteria:** extracted structures land in the KS tagged by concept with source provenance; verifiable against the source.
- **Dependencies:** SRC-02, KS-01, KS-02.
- **Concepts:** information extraction, claim/evidence modeling, provenance.
- **Required eval:** extraction precision/recall vs hand-labeled passages above thresholds.

### SRC-06 — Visual ingestion (images)
- **Release:** v0.3 · **Owner:** owner:agent (ingestion plumbing; vision) · **Size:** M
- **Description:** Optional image extraction/handling from sources for later "what do you see?" exercises and lesson images.
- **Acceptance criteria:** images extracted + stored with references; usable by LES-05 and EX-02.
- **Dependencies:** SRC-02.
- **Concepts:** image extraction, visual references.
- **Required eval:** n/a (exercised downstream).

### SRC-07 — Source-grounded retrieval priority (sources primary)
- **Release:** v0.3 · **Owner:** owner:deeksha (grounding — core learning) · **Size:** M
- **Description:** When sources exist, they are primary over web; answers label source type per claim; honor the per-course sources-only vs sources+web setting.
- **Acceptance criteria:** with sources present, grounded answers prefer sources and label types; sources-only mode never hits the web.
- **Dependencies:** RET-05, SRC-05, CRS-01.
- **Concepts:** grounding priority, source precedence.
- **Required eval:** source-precedence + labeling correctness on a mixed set above a threshold.

---

## E9 — Exercises and Assessment (EX)

### EX-01 — Placement quiz (baseline)
- **Release:** v0.4 · **Owner:** owner:agent (quiz generation + UI; baseline mapping lives in LRN-01) · **Size:** M
- **Description:** Generate + administer a short placement quiz that confirms the learner's level and seeds the baseline.
- **Acceptance criteria:** quiz generated for a course; results produce a level + per-concept baseline handed to LRN-01.
- **Dependencies:** PLAN-01, LRN-01.
- **Concepts:** adaptive placement, baseline estimation.
- **Required eval:** placement level correlates with a known-level simulated learner.

### EX-02 — "What do you see?" observation exercise (region highlighting)
- **Release:** v0.4 · **Owner:** owner:agent (Assessor workflow + UI, vision; Deeksha pairs on grading prompt) · **Size:** L
- **Description:** Learner interprets an image/chart/diagram/code; tutor confirms what's right, corrects misreadings, adds what was missed, highlighting the image regions discussed.
- **Acceptance criteria:** feedback distinguishes correct/misread/missed; highlighted regions map to the discussed content.
- **Dependencies:** SRC-06 (or lesson images), QA-03.
- **Concepts:** visual grounding, region referencing, observation assessment.
- **Required eval:** feedback correctness vs labeled image answers above a threshold.

### EX-03 — Explain-it-back exercise
- **Release:** v0.4 · **Owner:** owner:agent (Assessor workflow + UI; Deeksha pairs on grading) · **Size:** M
- **Description:** Learner explains a concept back; tutor assesses understanding and fills gaps.
- **Acceptance criteria:** identifies misconceptions + gaps; gives targeted feedback.
- **Dependencies:** QA-03.
- **Concepts:** self-explanation, misconception detection.
- **Required eval:** gap/misconception detection vs labels above a threshold.

### EX-04 — Question-type selection by subject profile
- **Release:** v0.4 · **Owner:** owner:agent (workflow logic) · **Size:** S
- **Description:** Choose exercise/question types that fit the source's subject profile (math vs code vs visual, etc.).
- **Acceptance criteria:** selected types match the profile on a labeled set.
- **Dependencies:** SRC-03, EX-02, EX-03.
- **Concepts:** profile-driven assessment design.
- **Required eval:** selection appropriateness on labeled profiles.

### EX-05 — Free-form answer grading vs sources
- **Release:** v0.4 · **Owner:** owner:deeksha (grading-vs-sources = grounding + judge — core learning) · **Size:** L
- **Description:** Grade free-form answers against sources/rubric with explanations.
- **Acceptance criteria:** grades + justifications produced; grounded in sources; feeds the learner model.
- **Dependencies:** RET-03, QA-03, LRN-01.
- **Concepts:** rubric grading, grounded assessment, judge calibration.
- **Required eval:** grade agreement with Deeksha's labels (via QA-03) above a threshold.

---

## E11 — Learner Model and Progress (LRN)

### LRN-01 — Statistics-based learner model (concept mastery)
- **Release:** v0.4 · **Owner:** owner:deeksha (learner model — core learning) · **Size:** L
- **Description:** Track concept-level mastery from placement + exercise results using statistics first (pre-ML).
- **Owns (arch):** Learner model service (stats phase).
- **Acceptance criteria:** mastery per concept updates from results; baseline set from placement; readable by planner + context packet.
- **Dependencies:** EX-01, EX-05.
- **Concepts:** mastery estimation, concept-level modeling.
- **Required eval:** mastery tracks ground truth on a simulated learner.

### LRN-02 — Confidence vs actual performance
- **Release:** v0.4 · **Owner:** owner:deeksha (learner model — core learning) · **Size:** M
- **Description:** Capture self-reported confidence and compare to actual performance (calibration of the learner).
- **Acceptance criteria:** confidence captured per item; calibration gap computed + surfaced.
- **Dependencies:** LRN-01.
- **Concepts:** metacognition, calibration.
- **Required eval:** calibration metric computed correctly on fixtures.

### LRN-03 — Retention checks + spaced repetition
- **Release:** v1.0 · **Owner:** owner:deeksha (learner model — core learning) · **Size:** L
- **Description:** Schedule retention checks days/weeks later and apply spaced repetition.
- **Acceptance criteria:** due concepts are scheduled + surfaced; retention results update mastery.
- **Dependencies:** LRN-01.
- **Concepts:** spaced repetition, retention, forgetting curves.
- **Required eval:** scheduling matches a spaced-repetition policy on simulated timelines.

### LRN-04 — Adaptive sequencing signals
- **Release:** v1.0 · **Owner:** owner:deeksha (learner model — core learning) · **Size:** M
- **Description:** Turn mastery/retention into next-concept recommendations that drive PLAN-03.
- **Acceptance criteria:** produces a prioritized next-concepts list the planner consumes.
- **Dependencies:** LRN-01, LRN-03.
- **Concepts:** mastery-driven sequencing.
- **Required eval:** recommendations improve simulated-learner outcomes vs fixed order.

### LRN-05 — Progress dashboard
- **Release:** v1.0 · **Owner:** owner:agent (frontend; data from Deeksha's model) · **Size:** M
- **Description:** Dashboard: concept mastery, homework/exercise scores over time, confidence vs actual, and progress toward the stated goal.
- **Acceptance criteria:** all measures render from real data; goal progress shown.
- **Dependencies:** LRN-01, LRN-02, LRN-03, DEV-01.
- **Concepts:** progress visualization.
- **Required eval:** n/a.

### LRN-06 — Trained knowledge-tracing model
- **Release:** v2.x · **Owner:** owner:deeksha (knowledge tracing — core learning) · **Size:** L
- **Description:** Replace/augment the statistics model with a trained knowledge-tracing model.
- **Acceptance criteria:** trained model beats the stats baseline on held-out mastery prediction.
- **Dependencies:** LRN-01 + accumulated data.
- **Concepts:** knowledge tracing (e.g. BKT/DKT), train/eval split.
- **Required eval:** predictive AUC/accuracy beats the stats baseline.

---

## E10 — Voice (VOI)

### VOI-01 — Core voice pipeline (STT + TTS + turn-taking, 1–2s)
- **Release:** v0.5 · **Owner:** owner:deeksha (core voice pipeline — core learning) · **Size:** L
- **Description:** The streaming pipeline: speech-to-text in, model, text-to-speech out, with turn-taking and replies starting in ~1–2s.
- **Owns (arch):** core voice pipeline.
- **Acceptance criteria:** spoken question → spoken answer with first audio in ~1–2s; barge-in boundary handled; runs through the gateway.
- **Dependencies:** TUT-01, PLAT-02.
- **Concepts:** streaming STT/TTS, latency budgeting, turn-taking.
- **Required eval:** first-response latency + transcription accuracy meet targets on a fixed set.

### VOI-03 — Narrated slides + spoken Q&A + voice answers to exercises
- **Release:** v0.5 · **Owner:** owner:deeksha (voice pipeline — core learning) · **Size:** M
- **Description:** Narrate slide speaker notes; accept spoken questions and give voice answers, including to exercises.
- **Acceptance criteria:** slides narrate on demand; spoken Q&A works in a lesson; exercise answers can be spoken + graded.
- **Dependencies:** VOI-01, LES-02, EX-03.
- **Concepts:** narration, voice-driven assessment.
- **Required eval:** spoken-answer grading parity with typed answers on a sample.

### VOI-04 — Interruptions + natural turn-taking
- **Release:** v0.5 · **Owner:** owner:deeksha (voice pipeline — core learning) · **Size:** M
- **Description:** Allow the learner to interrupt; handle natural turn-taking/barge-in gracefully.
- **Acceptance criteria:** interrupting stops playback + reroutes to the new input without losing context.
- **Dependencies:** VOI-01.
- **Concepts:** barge-in, endpointing, turn management.
- **Required eval:** interruption handled correctly across scripted scenarios.

### VOI-05 — Spoken rewrites of equations/code/tables
- **Release:** v0.5 · **Owner:** owner:agent (speech formatting; Deeksha pairs) · **Size:** M
- **Description:** Convert equations, code, and tables into natural spoken form.
- **Acceptance criteria:** sample equations/code/tables render to accurate, intelligible speech.
- **Dependencies:** VOI-01.
- **Concepts:** structured-content verbalization.
- **Required eval:** spoken-rewrite faithfulness (judge) above a threshold.

### VOI-06 — Voice UI (mic, streaming, barge-in controls)
- **Release:** v0.5 · **Owner:** owner:agent (frontend wiring) · **Size:** M
- **Description:** Mic capture, streaming playback, and controls that expose interruption/turn-taking.
- **Acceptance criteria:** usable mic + playback UI; barge-in control works; states are clear.
- **Dependencies:** VOI-01, DEV-01.
- **Concepts:** audio UI, streaming playback.
- **Required eval:** n/a.

---

## E12 — Homework (HW)

### HW-01 — Per-lesson assignment generation + rubric
- **Release:** v1.5 · **Owner:** owner:agent (generation workflow; Deeksha pairs on rubric design) · **Size:** M
- **Description:** Generate an assignment per lesson, each with a rubric.
- **Acceptance criteria:** assignment + rubric generated from a lesson's concepts; rubric is specific + gradeable.
- **Dependencies:** LES-03.
- **Concepts:** assignment design, rubric generation.
- **Required eval:** rubric covers the lesson's concepts (judge) above a threshold.

### HW-02 — Multi-format submission intake
- **Release:** v1.5 · **Owner:** owner:agent (infrastructure) · **Size:** M
- **Description:** Accept written answers, images, worked problems, code, and audio.
- **Acceptance criteria:** each format uploads + is routed to the grader; audio transcribed, images stored for annotation.
- **Dependencies:** HW-01, SRC-01 (storage), VOI-01 (audio).
- **Concepts:** multi-modal intake.
- **Required eval:** n/a.

### HW-03 — Grading vs rubric + feedback marked on images
- **Release:** v1.5 · **Owner:** owner:agent (Assessor workflow + image annotation, vision; grading judge in HW-04) · **Size:** L
- **Description:** Grade submissions against the rubric (vision when needed) and mark feedback directly on image submissions.
- **Acceptance criteria:** scores + rubric-aligned feedback produced; image feedback is positioned on the image.
- **Dependencies:** HW-01, HW-02, QA-03.
- **Concepts:** rubric grading, visual annotation.
- **Required eval:** grading accuracy vs labels (via HW-04) above a threshold.

### HW-04 — Grader calibration vs Deeksha's labels + feed learner model
- **Release:** v1.5 · **Owner:** owner:deeksha (judge calibration + learner model — core learning) · **Size:** M
- **Description:** Calibrate the homework grader against Deeksha's own labels and feed results into the learner model.
- **Acceptance criteria:** grader agreement with Deeksha's labels reported + above threshold; results update mastery.
- **Dependencies:** HW-03, QA-03, LRN-01.
- **Concepts:** judge calibration, score→mastery integration.
- **Required eval:** inter-rater agreement above a threshold.

---

## E14 — Optimization (OPT)

### OPT-01 — Model routing / tier optimization
- **Release:** v2.x · **Owner:** owner:deeksha (core model orchestration) · **Size:** M
- **Description:** Route each call to the cheapest tier that meets quality, measured by evals.
- **Acceptance criteria:** routing reduces cost at equal-or-better eval scores on the test set.
- **Dependencies:** PLAT-02, QA-01.
- **Concepts:** model routing, quality/cost tradeoff.
- **Required eval:** cost↓ with eval scores held on the test courses.

### OPT-02 — Cost optimization (caching/batching)
- **Release:** v2.x · **Owner:** owner:agent (infrastructure) · **Size:** M
- **Description:** Caching + batching + prompt-size reductions across workflows.
- **Acceptance criteria:** measurable cost/latency reduction with no eval regression.
- **Dependencies:** KS-04, QA-01.
- **Concepts:** caching, batching, prompt economy.
- **Required eval:** cost/latency delta with eval scores held.

### OPT-03 — Fuller multi-agent coordination
- **Release:** v2.x · **Owner:** owner:deeksha (agent architecture — core learning; revisits ADR 0003) · **Size:** L
- **Description:** Richer coordination among Planner/Researcher/Tutor/workflows; revisit whether a framework now helps (ADR 0003 revisit).
- **Acceptance criteria:** a documented coordination design with an eval showing improvement over the hand-rolled baseline; ADR updated.
- **Dependencies:** PLAN-01, RES-05, TUT-03.
- **Concepts:** multi-agent coordination, orchestration tradeoffs.
- **Required eval:** end-to-end quality improvement on the test courses.

### OPT-04 — Fine-tuning (judges / knowledge tracing)
- **Release:** v2.x · **Owner:** owner:deeksha (modeling — core learning) · **Size:** L
- **Description:** Fine-tune models for judging and/or knowledge tracing where it beats prompting.
- **Acceptance criteria:** fine-tuned model beats the prompt/stats baseline on held-out data.
- **Dependencies:** QA-03, LRN-06.
- **Concepts:** fine-tuning, dataset curation, eval.
- **Required eval:** held-out improvement over baseline.

---

## Suggestions (not in the spec — accept or reject)

These are my ideas, kept out of the numbered backlog per the rules until you approve:

- **AUTH — User accounts + auth.** The spec implies multiple users (KS-03 "shared across courses and users"; learner-private data) but no auth feature is specified. Likely a prerequisite for KS-03 and any real deployment. *(Would be an E0/PLAT feature, owner:agent.)*
- **Course export / shareable read-only outline.** Export a course plan or completed lesson set.
- **Accessibility pass** on the slide + voice UIs (captions for narration, keyboard nav).
- **Analytics on tutor quality** (thumbs-up/down on answers feeding evals).
- **Admired-work / own-work usage.** The spec lists "examples of work they admire" and "own work samples" as source types but never says how they're used (style targets? homework calibration?). I've stored them via SRC-01 but assigned them no behavior — flagging as a product decision, not a built feature.

## Gaps / open questions

1. **Users & auth.** Is there a multi-user model in the near term, or single-user (just Deeksha) for v0.x? KS-03's cross-user sharing + privacy and PLAT-04 deployment depend on this. *Recommend deciding before v0.2 (KS-03).*
2. **Model provider(s).** Default to Claude tiers (strong/mid/fast = Opus/Sonnet/Haiku) through the gateway? Confirm so PLAT-02 tier mapping is concrete. Also: embeddings provider for RET-01, STT/TTS provider for VOI.
3. **Placement quiz timing.** Confirmed interpretation: v0.1 uses self-reported level; the placement quiz (EX-01) confirms it in v0.4. OK?
4. **Image/diagram generation tooling.** What renders "diagrams as code" (Mermaid? matplotlib? a code-exec sandbox?) and where's the exact no-AI-art boundary enforced (LES-05)?
5. **Voice latency budget + providers.** "1–2s" first response — against which STT/TTS stack, and is streaming TTS required day one (VOI-01)?
6. **Use of admired-work / own-work samples** (see Suggestions) — what behavior should these drive?
7. **ID prefix for the Course Planner:** the backlog-writer skill defines `PLAN`; your example used `PLN`. I've used **PLAN** throughout for consistency with the skill — say if you'd rather switch the skill to `PLN`.
8. **Granularity.** This is 70 features; several (e.g. the VOI, SRC, LES sets) could be merged if you'd prefer a leaner board. Happy to consolidate.
