---
name: Feature
about: A feature issue for the ai-tutor backlog (fields match the backlog-writer skill)
title: "[ID] Short title"
labels: type:feature
---

## ID
<!-- Epic prefix + number, e.g. RET-02 -->

## Description

## Acceptance criteria

- [ ]
- [ ]

## Dependencies

## Epic

## Release milestone

## Owner
<!-- owner:deeksha or owner:agent, with a one-line reason -->

## Concepts learned

## Required eval

## Size
<!-- S / M / L -->

## Definition of Done (every story)
<!-- Standing checklist — the same for every feature; do not delete. -->

- [ ] **Learning doc** written by `doc-writer` at `docs/features/<ID>-<slug>.md` so Deeksha can understand what was built: what & why, how it works (with file/function refs), a Mermaid data-flow diagram, data stored, concepts used (linked to concept docs), design decisions, how to run & test, and a **"check your understanding"** section
- [ ] `docs/data/guide.md` and/or `docs/architecture/overview.md` updated if data or architecture changed
- [ ] Tests added/updated and passing; evals run where relevant
- [ ] `reviewer` subagent run (checks acceptance criteria, tests, and that the doc matches the code)
