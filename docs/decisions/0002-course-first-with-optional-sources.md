# ADR 0002: Courses are the central object; sources are optional

Status: Accepted

## Context

The tutor needs to work for any subject, including ones where the learner has no material to upload yet, while also supporting learners who want to study from their own books, notes, or syllabi.

## Decision

A course is fully definable and runnable with zero uploaded sources — goal, level, target outcome, time budget, and style are enough to start, backed by web research and model knowledge. Sources (books, articles, transcripts, notes, syllabi, past exams, examples, glossaries) are an optional enrichment layer that gets an advisory (never blocking) relevance check and a subject profile.

## Alternatives considered

A source-required model, where a course can't start until material is uploaded. Rejected: adds friction for subjects where the learner has no material, and conflicts with the goal of a generic tutor that works for any subject from day one.

## Consequences

The pipeline must support "sources only," "web only," and "sources + web" per course, and ingestion/relevance-check logic must degrade gracefully to a no-op when there's nothing to ingest.
