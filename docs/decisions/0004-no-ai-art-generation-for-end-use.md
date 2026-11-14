# ADR 0004: No AI art generation for end-use content

Status: Accepted

## Context

Image generation is cheap to add and tempting to use broadly for lesson "flavor" images, not just teaching diagrams.

## Decision

Generated imagery is allowed only to teach — diagrams, labeled illustrations, concept maps, or visual corrections. It is never used to generate decorative or illustrative "art" for its own sake.

## Alternatives considered

Allowing general AI art generation for engagement or aesthetics. Rejected: out of scope for a tutor whose job is teaching accuracy, not visual engagement, and it would introduce a category of generated content that was never meant to be factual, blurring the knowledge store's verification model.

## Consequences

Any image-generation code path must be scoped and labeled as "teaching diagram" generation, and reviewed accordingly rather than treated as a general-purpose image tool.
