# ADR 0003: No agent frameworks at first — hand-build the agent loops

Status: Accepted

## Context

This project exists for the author to learn how agent loops, retrieval, and model orchestration actually work, not to learn a specific framework's abstractions.

## Decision

All model calls go through one internal gateway module, written directly against provider APIs. No agent-framework abstractions (e.g. LangChain, LlamaIndex, an agent SDK) for the Course Planner, Researcher, or Tutor loops in the initial releases.

## Alternatives considered

Using an existing agent framework from the start. Rejected for now: frameworks hide the exact mechanics (the tool-call loop, context assembly, retries) the author wants to understand first-hand. This is revisited in v2.x ("fuller multi-agent coordination") once the hand-built version is understood.

## Consequences

More code to write and maintain early on; slower initial velocity in exchange for deeper understanding. This decision can be revisited per-component later without an all-or-nothing switch.
