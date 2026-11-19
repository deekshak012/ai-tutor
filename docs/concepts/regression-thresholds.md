# Concept: Regression thresholds

## What it is

A **regression threshold** is the rule that turns eval scores into pass or fail. A good gate usually combines three kinds:

- **Absolute floor:** "good enough to ship at all", e.g. macro topic coverage ≥ 0.80.
- **Baseline-relative tolerance:** "no meaningfully worse than before", e.g. ≥ baseline − 0.05, where the baseline is the accepted score on `main` for the same dataset version.
- **Hard gate:** zero tolerance for safety and contract properties, e.g. 0 successful prompt injections, 100% schema-valid outputs.

## Why it matters here

QA-01's acceptance criterion is that the runner *"exits non-zero on regression below a threshold"*, and nearly every "Required eval" in the backlog ends with "above a threshold." The thresholds are what make an eval act as a CI gate instead of a dashboard. See the worked example in [M17](../curriculum/17-eval-runner.md).

## How it works

**Aggregation comes first.** The thresholded number depends on how per-item scores were combined:

- *macro* average (each item equal) vs *micro* (each unit, e.g. each topic, equal),
- *worst case* (min across items), which catches one broken subject that an average hides,
- *pass rate* (fraction of executions above a per-item bar),
- *any/count* for safety properties. Never average a safety property.

**Tolerance is about noise.** Model output varies run to run. If run-to-run sd of the aggregate is σ and you average k repeats, the standard error is about σ/√k. A tolerance well under ~2 standard errors makes CI fail at random. A tolerance far above it lets real regressions through. More repeats or items shrink the noise, and cost grows linearly.

**Why floor *and* baseline.** A floor alone misses a drop from 0.95 to 0.82. A baseline alone permits slow drift, where each change loses 0.03 within tolerance until quality has quietly halved.

**Updating baselines is deliberate.** When a change intentionally moves scores, or the dataset version changes, the baseline is updated in a reviewable step, never automatically on every green run.

**Paired comparison.** Comparing item by item against the baseline (did *each* course drop?) gives more signal than comparing two means.

## Further reading

- [M17 — How the eval runner works](../curriculum/17-eval-runner.md)
- [Offline evals](offline-evals.md), [Eval datasets](eval-datasets.md)
- Anthropic, "A statistical approach to model evaluations" (2024), on standard errors and paired differences in evals
