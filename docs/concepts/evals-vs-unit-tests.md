# Concept: Evals vs unit tests

## What it is

Two different tools for two different kinds of behavior:

| | Unit test | Eval |
|---|---|---|
| Checks | deterministic logic | stochastic, model-dependent behavior |
| Question | "is this exactly right?" | "over a dataset, is quality good enough and not worse?" |
| Result | pass/fail per assertion | scores → aggregates → thresholds |
| Runs | every change, milliseconds, free | tiered (PR/nightly), seconds to minutes, costs model spend |
| A failure means | a bug | a statistically meaningful drop (if thresholds are set right) |

In ServiceNow terms: ATF asserts that a record field equals a value after a flow runs. That suits deterministic flows. It doesn't suit an LLM skill whose wording changes every run.

## Why it matters here

The backlog draws the line explicitly: *"Model-dependent behavior stays with evals (QA-01), not unit tests."* In ai-tutor:

- **Unit tests (pytest):** schema validation, context-packet assembly given fixed state (RET-02 is "deterministic given the same state"), the eval runner's own aggregation and gate math, gateway retry logic with a mocked provider.
- **Evals (the runner, [M17](../curriculum/17-eval-runner.md)):** does the Planner cover the expected topics, are the Researcher's claims supported, does the Reviewer catch seeded errors.
- **E2E (Playwright, M19):** does the UI flow work.

M20 lays out the full three-way split.

## How it works

Why not unit-test model output?

- **Mocked responses** test only your parsing. They tell you nothing about the model, and they give false confidence.
- **Live calls with exact assertions** are flaky. People re-run until green, and the test stops meaning anything.
- **Live calls with loose assertions** ("output is non-empty") pass for bad outputs.

Why not evals for everything? They're slow and cost money, and their noise hides small logic bugs that a 2 ms unit test would catch exactly.

The boundary is one rule: **if the same input should always give the same output, unit-test it. If it shouldn't, eval it.** Many components contain both. The Planner's schema validation is unit-tested, and its planning quality is evaluated.

## Further reading

- [M17 — How the eval runner works](../curriculum/17-eval-runner.md)
- [M20 — Unit testing and the test split](../curriculum/20-unit-testing-and-the-test-split.md)
- [Offline evals](offline-evals.md)
