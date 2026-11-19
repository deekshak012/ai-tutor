# Concept: Gold datasets

## What it is

A gold dataset (also called a "golden set" or reference set) is a small, carefully curated collection of inputs paired with **trusted expected outputs**. The expected outputs are usually written or checked by a human. An eval scores a system's output against them. In other words, a gold dataset is a fixed answer key.

## Why it matters here

The three test courses in QA-02 are ai-tutor's gold dataset ([M18](../curriculum/18-test-courses-and-fact-checks.md)). Several later evals depend on them: Course Planner topic coverage (PLAN-01, [M06](../curriculum/06-course-planner-agent.md)), Lesson Builder slide accuracy (LES-03, [M11](../curriculum/11-lesson-builder-workflow.md)), and claim support for grounding (RET-03, [M09](../curriculum/09-grounding-and-citations.md)). The [eval runner](../curriculum/17-eval-runner.md) runs them. A gold dataset is one kind of [eval dataset](eval-datasets.md).

## How it works

- **Small and high-trust over large and noisy.** Ten items you have checked carefully are worth more than a thousand scraped ones, because a single wrong label teaches the eval the wrong thing.
- **Written independently of the system under test.** If a model writes the answer key, you end up measuring agreement between models, and errors they share pass unnoticed.
- **Stable and versioned.** You only learn something from scores across releases if the dataset stays the same, or if every change to it is recorded. Keeping it in git and linking each run to a dataset version handles this.
- **Scored with a metric plus a threshold.** For example, coverage ≥ 0.85, and the build fails below that line ([regression thresholds](regression-thresholds.md)).
- **Watch for overfitting.** If prompts are tuned against the same few items over and over, the system can learn the test rather than the skill. Keep a few items held out, or add items over time.

## Further reading

- [Offline evals](offline-evals.md)
- [LLM-as-judge](llm-as-judge.md): often used to compare outputs to gold answers when exact matching won't work.
- Langfuse documentation on datasets and dataset runs.
