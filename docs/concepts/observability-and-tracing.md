# Concept: Observability and tracing

## What it is

**Observability** is the ability to answer questions about what a running system did, using only what the system emits. You shouldn't need to add new code each time a new question comes up. There are three classic signals:

- **Logs** are individual timestamped messages.
- **Metrics** are numbers aggregated over time, such as calls per minute or p95 latency.
- **Traces** are the record of one unit of work, shown as a tree of timed steps.

For LLM applications, traces are the most useful of the three. A single model call has a lot of context that only matters together: the prompt, the model, the parameters, the input, the output, token counts, cost and latency. A trace keeps all of that in one place.

## Why it matters here

Most of ai-tutor's model work runs in the background, before the learner arrives (Course Planner, Researcher, Lesson Builder, Reviewer). Postgres only stores the results. Traces show how each result was produced, which makes them the main debugging tool. They are also what the eval runner and the cost work build on.

- Used in: [M02 — How tracing & observability work](../curriculum/02-tracing-and-observability.md) (PLAT-03)
- Builds on: [M01 — How the model gateway works](../curriculum/01-model-gateway.md) and the [gateway pattern](gateway-pattern.md)
- Feeds: [offline evals](offline-evals.md) (QA-01, [M17](../curriculum/17-eval-runner.md)), and the OPT-01/02 cost and routing work

## How it works

1. **Instrument a chokepoint.** You add recording code at a point every request passes through. In ai-tutor that point is the model gateway.
2. **Open a trace** for each unit of work, such as "plan this course" or "answer this chat turn". Attach identifiers like the session, the user and tags.
3. **Record nested [spans](spans.md)** for the steps inside the trace, each with a start and end time. LLM calls are recorded as *generations*, which also carry model, usage, cost and a [prompt version](prompt-versioning.md).
4. **Ship the data asynchronously** to a backend (Langfuse here). If the backend is unavailable, the application keeps working. This is called failing open.
5. **Query and inspect.** You filter traces, drill into a slow or expensive one, compare prompt versions, and attach eval scores.

The ServiceNow comparison is a flow's execution details. Each step is listed with its timing and its inputs and outputs. LLM tracing adds tokens, cost and prompt version to each step.

## Further reading

- Langfuse documentation: the tracing data model (traces, observations, sessions)
- OpenTelemetry documentation: the concepts of traces and spans (the general industry model that LLM tracing tools borrow from)
