# Concept: Eval datasets

## What it is

An **eval dataset** is a versioned list of **items**. Each item has:

- `input`: exactly what the target component receives (for the Course Planner: goal, context, include/skip topics),
- `expected`: what you'll score against. This is rarely an exact output. More often it's a set of properties: expected topics, topics that must not appear (the skip topics), fact checks, a label,

(The general names are `input` / `expected` / `metadata`. QA-02's test courses spell these out concretely as `inputs`, `expected_topics` and `fact_checks`; see [M18](../curriculum/18-test-courses-and-fact-checks.md).)
- `metadata`: tags for slicing results (subject profile, difficulty, when added, held-out or not).

A dataset differs from test fixtures in that it's treated as a measuring instrument: changing it changes what the numbers mean.

## Why it matters here

- QA-02's three test courses ([M18](../curriculum/18-test-courses-and-fact-checks.md)) are the backbone dataset across releases: Intro Statistics, Reading Financial Statements, Music Theory. They span math, text/visual, and notation/visual subject profiles.
- Each "Required eval" in the backlog implies a dataset: injection payload pages (RES-02), hand-labeled sources (RES-03), labeled query sets (RET-01), seeded-error lessons (LES-06).
- The eval runner ([M17](../curriculum/17-eval-runner.md)) loads a dataset, pins its version, and refuses to compare runs across versions.

## How it works

**Versioning.** Scores are only comparable within one dataset version. Adding a harder item lowers the average without anything regressing. Editing an item's `expected` changes the definition of correct. Either change bumps the version (an explicit tag or a content hash) and needs a new baseline.

**Where it lives.** Usually as files in git (reviewable, diffable, tied to commits), synced into an eval platform such as Langfuse, whose datasets hold items with input / expected output / metadata and link each run's traces to items. Making the platform the source of truth is easier for adding items from production traces, but harder to review.

**Freezing the environment.** If the target depends on the outside world (the Researcher's web search), freeze those inputs into the item, so the dataset measures the component, not the internet on a given day.

**Held-out items.** Keep some items you never tune prompts against. Otherwise you overfit the prompt to the dataset and the scores stop predicting real quality.

**Size vs cost.** More items detect smaller regressions and generalize better, but cost grows linearly. A small, sharp dataset (three courses) is a good smoke signal. It isn't proof of quality.

Related: [gold datasets](gold-datasets.md) (hand-labeled ground truth) and [fact-check design](fact-check-design.md).

## Further reading

- [M17 — How the eval runner works](../curriculum/17-eval-runner.md)
- [M18 — Test courses & fact checks](../curriculum/18-test-courses-and-fact-checks.md)
- Langfuse documentation: datasets, dataset items, dataset runs
