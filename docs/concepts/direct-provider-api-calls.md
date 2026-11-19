# Concept: Direct provider API calls

## What it is

Calling a model provider's API yourself, either over raw HTTP or through the provider's own thin official SDK, with no orchestration framework in between. You build the request (model, system prompt, messages, tool definitions, `max_tokens`), send it, and read the response (content blocks, tool calls, stop reason, token usage) as the provider returns it.

"Direct" is about **what sits between your code and the wire**, not about avoiding SDKs. A vendor SDK that only types requests and responses still counts as direct. A framework that owns prompt templates, chains, memory, or a tool-execution loop does not, because it decides what actually gets sent and when.

## Why it matters here

[ADR 0003](../decisions/0003-no-agent-frameworks-at-first.md) requires every model call in ai-tutor to be written directly against provider APIs, inside the single [model gateway](gateway-pattern.md). The goal is to learn the mechanics frameworks hide. See [M01 — How the model gateway works](../curriculum/01-model-gateway.md), stage 2 ("Build the provider request"). The agent loops built on top of it (Tutor, Course Planner, Researcher) are hand-written for the same reason.

## How it works

A chat-style model call is a stateless HTTP POST. Each request carries the **entire** conversation the model should see. The provider keeps no session for you, which is why context assembly (the context packet in [ADR 0001](../decisions/0001-agents-share-state-through-database.md)) is the caller's job.

- **Request:** model ID, `max_tokens`, optional system prompt, a list of role-tagged messages, optional tool schemas (JSON Schema describing functions the model may *ask* to call), and sampling options.
- **Response:** one or more content blocks (text, or tool-use requests with arguments), a stop reason (`end_turn`, `max_tokens`, `tool_use`, ...), and usage counts (input, output, and sometimes cached tokens).
- **Tool calling is just data.** The model never runs anything. It returns "please call `search(query=...)`", and your code decides whether to run it, then sends the result back in a *new* request. The loop is yours. With direct calls that's visible, and in a framework it's hidden.
- **Errors are HTTP statuses** with a provider-specific body: 400 malformed, 401/403 auth, 404 unknown model, 429 rate limited, 5xx or "overloaded" server-side. Mapping these to your own types is part of the work ([retries and backoff](retries-and-backoff.md)).
- **SDK defaults matter.** Official SDKs commonly add their own retries and long default [timeouts](timeouts.md). If you wrap one, decide explicitly who owns retry policy.

Provider formats differ in the details: where the system prompt goes, how tool calls and tool results are shaped, and the error body format. Supporting more than one provider means writing an adapter per provider behind one internal type.

## Further reading

- Anthropic Messages API reference: https://docs.anthropic.com/en/api/messages
- Anthropic API errors: https://docs.anthropic.com/en/api/errors
- OpenAI API reference: https://platform.openai.com/docs/api-reference
- Anthropic, "Building effective agents" (argues for starting with direct API calls): https://www.anthropic.com/engineering/building-effective-agents
