# Concept: Model tiers

## What it is

A small, named set of capability and cost classes (in ai-tutor: `strong`, `mid`, `fast`) that callers request **instead of** a specific model ID. Configuration maps each tier to a concrete model plus an operating policy (timeout, retry budget, prices). Callers say what kind of job this is, and the gateway decides which model does it.

## Why it matters here

The architecture principle is "Model tiers match the job" ([overview](../architecture/overview.md)):

- `strong`: Course Planner, Reviewer (deep reasoning, accuracy checks against sources)
- `mid`: Researcher, Lesson Builder, Assessor (quality structured output at volume, vision for the Assessor)
- `fast`: Tutor (live chat and voice, replies starting in about 1–2 s per the [product spec](../product-spec.md))

The [model gateway](gateway-pattern.md) resolves tiers. See [M01](../curriculum/01-model-gateway.md), stage 1. Which concrete provider and model backs each tier is an **open choice** documented there.

## How it works

Models trade off three things that can't all be maximised: **quality** (reasoning, instruction-following, fewer factual errors), **latency** (time to first token and tokens per second), and **price** (per input or output token, often 10x or more between the largest and smallest models in a family).

A tier fixes a point on that trade-off for a class of work:

- **Indirection.** Upgrading "the fast model" is a single config change, and evals can compare before and after on the same prompts.
- **Policy travels with the tier.** A live tier gets tight [timeouts](timeouts.md) and a small retry budget. A background tier can wait minutes. The tier is a latency contract as well as a model choice.
- **Compensating architecture.** ai-tutor can put the Tutor on a small fast model because the expensive thinking (planning, research, lesson building, review) was already done ahead of time by stronger tiers and stored in the database. The small model mostly has to *use* good material, not produce it from scratch.
- **Routing is a later step.** Choosing the tier dynamically per request (e.g. escalating hard questions to `strong`) is "model routing", scheduled for v2.x in the [release plan](../release-plan.md). Static tiers come first.

Pitfall: tiers must be capability-complete for their callers. If the Assessor needs vision, the `mid` mapping must support image input, or a separate variant is needed.

## Further reading

- Anthropic, "Choosing a model": https://docs.anthropic.com/en/docs/about-claude/models/choosing-a-model
- FrugalGPT (Chen et al., 2023), on cascading cheap and expensive models: https://arxiv.org/abs/2305.05176
