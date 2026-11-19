# ai-tutor curriculum — read to understand how it all works

This is a **read-to-understand** project. Instead of building the AI tutor, we produce a sequenced set of detailed explainer docs — one per module — so you can understand how a course-based AI tutor works end to end. Claude (`doc-writer`, `owner:agent`) writes each explainer; you read it and answer the check-your-understanding questions. **No application code is written.**

Each module maps to a GitHub issue (the deliverable is the doc, committed here as `NN-slug.md`). Read in order — later modules assume earlier ones. 🔵 = deep dive, ◻️ = light explainer.

## Part 1 — How the system is wired
- 🔵 **M01** — How the model gateway works ([#2](https://github.com/deekshak012/ai-tutor/issues/2)) → `01-model-gateway.md`
- ◻️ **M02** — How tracing & observability work ([#3](https://github.com/deekshak012/ai-tutor/issues/3)) → `02-tracing-and-observability.md`
- ◻️ **M03** — How the backend & data store are assembled ([#1](https://github.com/deekshak012/ai-tutor/issues/1)) → `03-backend-and-data-store.md`
- ◻️ **M04** — How the frontend shell is assembled ([#6](https://github.com/deekshak012/ai-tutor/issues/6)) → `04-frontend-shell.md`

## Part 2 — Courses & planning
- ◻️ **M05** — How a course is modeled ([#8](https://github.com/deekshak012/ai-tutor/issues/8)) → `05-course-model.md`
- 🔵 **M06** — How the Course Planner agent works ([#10](https://github.com/deekshak012/ai-tutor/issues/10)) → `06-course-planner-agent.md`

## Part 3 — Research, grounding & knowledge
- 🔵 **M07** — How the Researcher agent works ([#13](https://github.com/deekshak012/ai-tutor/issues/13)) → `07-researcher-agent.md`
- 🔵 **M08** — How prompt-injection defense (web-as-data) works ([#12](https://github.com/deekshak012/ai-tutor/issues/12)) → `08-prompt-injection-defense.md`
- 🔵 **M09** — How grounding & citations work ([#14](https://github.com/deekshak012/ai-tutor/issues/14)) → `09-grounding-and-citations.md`

## Part 4 — Lessons & the live tutor
- ◻️ **M10** — How the slide data contract works ([#15](https://github.com/deekshak012/ai-tutor/issues/15)) → `10-slide-data-contract.md`
- 🔵 **M11** — How the Lesson Builder workflow works ([#17](https://github.com/deekshak012/ai-tutor/issues/17)) → `11-lesson-builder-workflow.md`
- ◻️ **M12** — How the slide renderer works ([#16](https://github.com/deekshak012/ai-tutor/issues/16)) → `12-slide-renderer.md`
- 🔵 **M13** — How the live Tutor agent loop works ([#18](https://github.com/deekshak012/ai-tutor/issues/18)) → `13-tutor-agent-loop.md`

## Part 5 — How the learner interacts (UIs)
- ◻️ **M14** — How the course-creation flow works ([#9](https://github.com/deekshak012/ai-tutor/issues/9)) → `14-course-creation-flow.md`
- ◻️ **M15** — How the outline view/edit works ([#11](https://github.com/deekshak012/ai-tutor/issues/11)) → `15-outline-view-edit.md`
- ◻️ **M16** — How the slide + chat interface works ([#19](https://github.com/deekshak012/ai-tutor/issues/19)) → `16-slide-chat-interface.md`

## Part 6 — Quality: evaluating & testing
- 🔵 **M17** — How the eval runner works ([#4](https://github.com/deekshak012/ai-tutor/issues/4)) → `17-eval-runner.md`
- ◻️ **M18** — How the test courses & fact checks work ([#5](https://github.com/deekshak012/ai-tutor/issues/5)) → `18-test-courses-and-fact-checks.md`
- ◻️ **M19** — How E2E testing (Playwright) works ([#20](https://github.com/deekshak012/ai-tutor/issues/20)) → `19-e2e-testing-playwright.md`
- ◻️ **M20** — How unit testing fits (unit-vs-eval-vs-E2E) ([#7](https://github.com/deekshak012/ai-tutor/issues/7)) → `20-unit-testing-and-the-test-split.md`

---

Modules M01–M20 correspond to the (formerly v0.0 + v0.1) issues. Later topic areas — knowledge store, retrieval/context packets, optional sources & ingestion, exercises & assessment, the learner model & knowledge tracing, voice, homework, optimization — become further modules when you ask to add them (see `docs/backlog/backlog-draft.md`).

Each explainer follows `docs/templates/curriculum-module-template.md`.
