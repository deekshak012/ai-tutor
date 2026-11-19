# Release overview: <version>

- Theme: <one line from the release plan>
- Milestone: <GitHub milestone link>
- Status: in progress | shipped on <date>

> A higher-altitude companion to the per-story feature docs in `docs/features/`. It stitches this version's stories into one picture so you can see how the pieces fit, without re-reading every feature doc. Links out rather than duplicating.

## What this release adds

A short narrative of what the learner/user can now do that they couldn't before.

| Story | What it adds | Feature doc |
|---|---|---|
| <ID> | one line | [link](../features/<ID>-<slug>.md) |

## End-to-end walkthrough

Walk one real flow from start to finish, naming the components it passes through (e.g. "create a course → Course Planner builds the outline → Lesson Builder renders a slide → Tutor answers a question"). This is the "how it all connects" story.

## How the pieces connect

```mermaid
flowchart LR
```

Diagram of the components added or changed this release and the data flowing between them. Reference the architecture overview for the full system.

## New concepts introduced

- [Concept](../concepts/<slug>.md) — one line on where it shows up this release.

## Data added this release

Tables/fields introduced or changed, linking to `docs/data/guide.md`.

## Decisions made

- [ADR NNNN](../decisions/<file>.md) — one line.

## Still stubbed / deferred

What was intentionally left thin and which later version deepens it.

## Check your understanding

- A release-level question that spans more than one story.
- A second question about how two components interact.
- A small end-to-end experiment to try.
