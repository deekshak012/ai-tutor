---
name: Curriculum module
about: A read-to-understand explainer module for ai-tutor (no code is written)
title: "M<NN> — How <component> works (<ID>)"
labels: type:feature, owner:agent
---

## Module
<!-- M<NN> · Part N -->

## Component
<!-- `<ID>` — <name> of the component being explained -->

## What you'll understand
<!-- One or two sentences on what the reader will be able to explain afterward -->

## The explainer must cover
- [ ] What it is & why it exists
- [ ] How it works, step by step — with a Mermaid data-flow or sequence diagram
- [ ] Where the data lives (tables/fields/stores, or "none")
- [ ] Key concepts (linked to `docs/concepts/`)
- [ ] Design decisions & rejected alternatives (linked ADRs)
- [ ] A worked example
- [ ] A "check your understanding" section (3–5 questions + a thought experiment)

## Depth
<!-- deep dive | light -->

## Deliverable
`docs/curriculum/<NN>-<slug>.md`, authored by `doc-writer` (**owner:agent**). No code.

## Reading order
<!-- Prereqs: M.. · Next: M.. -->

## Acceptance
- [ ] Explainer committed at `docs/curriculum/<NN>-<slug>.md` following `docs/templates/curriculum-module-template.md`
- [ ] Includes a Mermaid diagram and a worked example
- [ ] `reviewer` confirms it is accurate against the architecture/data references
- [ ] A reader can explain the component end to end **without seeing code**
