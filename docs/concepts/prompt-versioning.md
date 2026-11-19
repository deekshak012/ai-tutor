# Concept: Prompt versioning

## What it is

**Prompt versioning** treats each prompt as a named artifact with immutable, numbered versions, much like code. Each model call records exactly which prompt version it used. When output quality, cost or latency changes, you can then tell whether the prompt changed or something else did.

In Langfuse prompt management, a prompt has a **name**, numbered **versions**, and movable **labels** (for example `production`). A label points at one version. Code asks for "the `production` version of `course_planner.draft_outline`", and you promote a new version by moving the label. When a generation is linked to the prompt version it used, the trace shows that version, and metrics can be compared across versions.

## Why it matters here

Every prompt-driven component (Course Planner, Researcher, Lesson Builder, Reviewer, Assessor, Tutor) will have prompts that keep getting revised. PLAT-03 requires that every gateway call records its prompt version. Without that, eval regressions (QA-01) and quality drops can't be traced back to a specific change.

- Used in: [M02 — How tracing & observability work](../curriculum/02-tracing-and-observability.md) (PLAT-03)
- Related: [offline evals](offline-evals.md) (comparing scores across prompt versions), and QA-03 (the judge's calibration prompt is version-tracked)

## How it works

1. **Name** each prompt by component and purpose, for example `lesson_builder.generate_slides`.
2. **Version immutably.** An edit creates version N+1. Version N stays exactly as it was.
3. **Resolve at call time.** The caller (or a small prompt helper beside it) fetches the prompt by label or by pinned version, usually with a local cache, and fills in its variables. The model gateway only ever receives the rendered messages plus a `prompt_ref` label such as `name@version` ([M01](../curriculum/01-model-gateway.md)).
4. **Record the link** on the generation (prompt name and version), so every trace shows which version ran. The gateway does this from the `prompt_ref` it was given.
5. **Compare and promote.** You run evals on the new version and compare scores, cost and latency with the current one. If it wins, you move the `production` label to it.

There is an open design question here. Prompts can be kept in Langfuse, which allows editing without a deploy, or in git, which keeps them reviewable in PRs and means recording a version or hash on the trace. Either way, every call records the version that produced it.

## Further reading

- Langfuse documentation: prompt management (versions, labels, linking prompts to traces)
