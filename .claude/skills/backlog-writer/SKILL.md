---
name: backlog-writer
description: Turns an idea or feature description into a GitHub issue for the ai-tutor repo using the feature issue template, with ID, acceptance criteria, labels, milestone, and GitHub Project fields. Use when the user wants to turn a decision or idea discussed in chat into a tracked issue.
allowed-tools: Bash, Read, Grep, Glob
---

Turn the idea or feature description just discussed into a GitHub issue for `deekshak012/ai-tutor`.

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

1. Identify the epic for the idea and its ID prefix from the table above.
2. Check for duplicates and find the next free number for that prefix: `gh issue list --repo deekshak012/ai-tutor --search "<keywords>" --state all` and scan titles for the prefix (e.g. `RET-01`, `RET-02`, ...).
3. Draft the issue with every field:
   - **ID**: `<prefix>-<NN>`, e.g. `RET-02`
   - **Description**
   - **Testable acceptance criteria** (checklist)
   - **Dependencies** (other issue IDs, or none)
   - **Epic label** (from the table)
   - **Release milestone** (one of v0.0, v0.1, v0.2, v0.3, v0.4, v0.5, v1.0, v1.5, v2.x — from `docs/release-plan.md`)
   - **Owner label**: `owner:deeksha` or `owner:agent`, with a one-line reason (learning-mode items from CLAUDE.md — agent loops, retrieval, knowledge store, learner model, evals, voice pipeline — default to `owner:deeksha`; scaffolding/infra/tests/frontend wiring default to `owner:agent`)
   - **Concepts learned**
   - **Required eval**
   - **Size**: S, M, or L
4. Show the full draft to the user and **wait for explicit approval**. Never create anything before approval.
5. Once approved, create the issue using `.github/ISSUE_TEMPLATE/feature.md` as the body structure:
   `gh issue create --repo deekshak012/ai-tutor --title "<ID> <short title>" --body "<filled template>" --label "type:feature" --label "<epic label>" --label "<owner label>" --milestone "<release>"`
6. Add the created issue to the `ai-tutor` GitHub Project and set its fields (Epic, Release, Owner, Priority, Size, Status = Backlog):
   `gh project item-add <project-number> --owner deekshak012 --url <issue-url>`, then `gh project item-edit` for each field.
7. Report the issue URL back to the user.
