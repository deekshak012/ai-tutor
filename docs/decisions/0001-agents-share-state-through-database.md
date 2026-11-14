# ADR 0001: Agents share state through the database, not conversation-passing

Status: Accepted

## Context

The system has three agents (Course Planner, Researcher, Tutor) and three workflows (Lesson Builder, Reviewer, Assessor) that all contribute to a course over time, often at different points in time (research happens hours before a lesson is built; review happens after the lesson is drafted).

## Decision

No agent or workflow passes its conversation history or intermediate reasoning directly to another. All shared state — course plans, knowledge store entries, lesson drafts, review outcomes, learner model updates — is written to and read from Postgres. Each agent or workflow call receives a scoped context packet assembled from the database, never a transcript from another agent.

## Alternatives considered

Direct agent-to-agent message passing (e.g. Researcher hands its findings straight to the Lesson Builder in-context). Rejected: it makes each component's behavior depend on replaying the whole chain, defeats the goal of every workflow having a defined input/output it can be evaluated on independently, and prevents decoupling expensive work in time.

## Consequences

Every agent and workflow needs a well-defined database read/write contract. State is inspectable at any point, which helps debugging, but the knowledge store schema needs to be designed early and evolve carefully.
