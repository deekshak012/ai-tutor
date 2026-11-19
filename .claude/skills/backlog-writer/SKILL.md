---
name: backlog-writer
description: Turns a curriculum topic into a GitHub issue for the ai-tutor repo (read-to-understand mode) — one explainer-doc module per issue, all owner:agent, using the module issue template and GitHub Project fields. Use when the user wants to add a module to the curriculum.
allowed-tools: Bash, Read, Grep, Glob
---

Turn the topic just discussed into a **curriculum module** issue for `deekshak012/ai-tutor`. This is a read-to-understand project: each issue's deliverable is an explainer doc at `docs/curriculum/NN-slug.md` authored by `doc-writer` — **no code is built, and every module is `owner:agent`.**

## Epic → ID prefix mapping

| Epic | Label | ID prefix |
|---|---|---|
| E0 Platform and Infrastructure | `epic:E0-platform` | `PLAT` |
| E1 Courses | `epic:E1-courses` | `CRS` |
| E2 Course Planner | `epic:E2-course-planner` | `PLAN` |
| E3 Research and Web | `epic:E3-research-web` | `RES` |
| E4 Knowledge Store | `epic:E4-knowledge-store` | `KS` |
| E5 Sources and Ingestion | `epic:E5-sources-ingestion` | `SRC` |
| E6 Retrieval and Grounding | `epic:E6-retrieval-grounding` | `RET` |
| E7 Lessons | `epic:E7-lessons` | `LES` |
| E8 Tutor and Chat | `epic:E8-tutor-chat` | `TUT` |
| E9 Exercises and Assessment | `epic:E9-exercises-assessment` | `EX` |
| E10 Voice | `epic:E10-voice` | `VOI` |
| E11 Learner Model and Progress | `epic:E11-learner-model-progress` | `LRN` |
| E12 Homework | `epic:E12-homework` | `HW` |
| E13 Quality and Evals | `epic:E13-quality-evals` | `QA` |
| E14 Optimization | `epic:E14-optimization` | `OPT` |
| E15 Dev Tooling and Docs | `epic:E15-dev-tooling-docs` | `DEV` |

## Steps

1. Identify the epic (topic area) for the module and its ID prefix from the table above.
2. Check for duplicates and find the next module number: `gh issue list --repo deekshak012/ai-tutor --search "<keywords>" --state all` and scan titles for the component ID and the next free `M<NN>` (modules are numbered in reading order; see `docs/curriculum/README.md`).
3. Draft the issue with every field, following `.github/ISSUE_TEMPLATE/feature.md`:
   - **Module** `M<NN>` and its **Part**, and the **Component** `<prefix>-<NN>` (e.g. `RET-02`)
   - **What you'll understand** (what the reader can explain afterward)
   - **The explainer must cover** (the standing checklist from the template)
   - **Depth**: deep dive (conceptually rich — agent loops, retrieval/grounding, knowledge store, lesson builder, evals, learner model, voice) or light (UI/plumbing)
   - **Epic label** (from the table)
   - **Milestone** (the topic's release grouping, from `docs/release-plan.md`) — used only as a grouping
   - **Reading order**: prereq modules and next module
   - **Deliverable**: `docs/curriculum/<NN>-<slug>.md`, authored by `doc-writer`
4. Show the full draft to the user and **wait for explicit approval**. Never create anything before approval.
5. Once approved, create the issue (always `owner:agent` — there is no `owner:deeksha`):
   `gh issue create --repo deekshak012/ai-tutor --title "M<NN> — How <component> works (<ID>)" --body "<filled template>" --label "type:feature" --label "<epic label>" --label "owner:agent" --milestone "<release>"`
6. Add the created issue to the `ai-tutor` GitHub Project and set its fields (Epic, Release, Owner = agent, Size, Status = Backlog):
   `gh project item-add <project-number> --owner deekshak012 --url <issue-url>`, then `gh project item-edit` for each field.
7. Report the issue URL back to the user.
