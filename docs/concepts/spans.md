# Concept: Spans

## What it is

A **span** is one timed step inside a [trace](observability-and-tracing.md). It has a name, a start time, an end time, optional input, output and metadata, and an optional parent span. Because spans nest, a trace forms a tree. For example, "plan course" can contain "call model", and "call model" can contain "retry".

Langfuse uses the general term **observation** for anything recorded under a trace. The core observation types are:

- **Span**: a generic timed step, such as "assemble context packet".
- **Generation**: a span specialized for one LLM call. It also carries model, model parameters, token usage, cost and an optional link to a managed prompt version.
- **Event**: a point-in-time marker with no duration, such as "retry after 429".

## Why it matters here

Each ai-tutor gateway call is recorded as a generation. When an agent loop makes several calls, those generations sit side by side under one trace, so you can see which step was slow or expensive.

- Used in: [M02 — How tracing & observability work](../curriculum/02-tracing-and-observability.md) (PLAT-03)
- Related: [token and cost accounting](token-and-cost-accounting.md), [model tiers](model-tiers.md)

## How it works

- **Timing:** latency is the span's end time minus its start time. A parent span's duration includes its children and any gaps between them.
- **Nesting:** every child stores the id of its parent. To nest correctly, the code creating a child must know the current parent. That's why a caller has to pass trace context down to the gateway.
- **Roll-ups:** tools add up child values to give trace-level totals, such as total cost and total tokens.
- **Status:** a span can be marked as an error with a message attached. That's how a failed provider call shows up.

## Further reading

- Langfuse documentation: observation types (spans, generations, events)
- OpenTelemetry documentation: spans and span context
