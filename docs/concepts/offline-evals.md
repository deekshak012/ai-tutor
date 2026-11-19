# Concept: Offline evals

## What it is

An **offline eval** measures a model-driven component by running it on a **fixed, curated dataset** ahead of time, scoring each output, and summarizing the scores. It's the opposite of **online evaluation**, which monitors real traffic after release (user ratings, live judge sampling, A/B tests).

Offline means: the inputs are known, the expected properties are written down, the run can be repeated, and nobody has to wait for real learners to hit a problem.

## Why it matters here

ai-tutor does almost all of its expensive work ahead of the learner: planning, research, lesson building, review. Only the Tutor runs live. So almost every component can, and should, be evaluated offline before it ships:

- The eval runner ([M17](../curriculum/17-eval-runner.md), QA-01) is the harness for every offline eval in the backlog.
- The three test courses ([M18](../curriculum/18-test-courses-and-fact-checks.md), QA-02) are the main offline dataset.
- Per-feature "Required eval" lines (PLAN-01 topic coverage, RES-01 claim support, RES-02 zero injections, LES-06 reviewer recall) are all offline evals.

Online signals (the "thumbs up/down feeding evals" suggestion in the backlog) would come later and *feed* offline datasets with real failure cases.

## How it works

1. **Dataset:** inputs + expected data, versioned ([eval datasets](eval-datasets.md)).
2. **Target:** a component with a defined [I/O contract](io-contracts.md).
3. **Run:** execute the target on every item, usually several times, because output is stochastic.
4. **Score:** deterministic scorers where possible, [LLM-as-judge](llm-as-judge.md) where necessary.
5. **Aggregate and gate:** compare to a floor and a baseline ([regression thresholds](regression-thresholds.md)).
6. **Inspect:** link each item's score to its trace so failures can be diagnosed.

Strengths: reproducible, comparable over time, cheap enough to run in CI, and able to isolate one component. Weaknesses: only as good as the dataset (it can't catch failure modes nobody wrote an item for), and prompts can be overfit to it, so keep held-out items.

## Further reading

- [M17 — How the eval runner works](../curriculum/17-eval-runner.md)
- [Evals vs unit tests](evals-vs-unit-tests.md)
- Langfuse documentation on datasets and experiments / dataset runs
- Hamel Husain, "Your AI product needs evals" (blog post), a practitioner's case for offline evals
