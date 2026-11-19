# Concept: Subject profiles

## What it is

A subject profile describes what kind of material a subject or source mostly consists of. The [product spec](../product-spec.md) lists six: **text-heavy, visual, math, code, diagrams, or mixed**. The profile determines how a source is parsed, which exercise question types fit, and which homework formats make sense. A proof-heavy math text, a set of annotated charts, and a Python tutorial each need different handling.

## Why it matters here

- **Ingestion (v0.3):** each uploaded source gets a profile that guides parsing (OCR and equations, image regions, code blocks).
- **Exercises and homework:** question types and submission formats follow the profile, for example "what do you see?" on visual material and worked problems on math.
- **Evals (now):** the QA-02 test courses ([M18](../curriculum/18-test-courses-and-fact-checks.md)) were chosen to span profiles. *Intro Statistics* is math + text, *Reading financial statements* is text + tables/visual, and *Music theory* is notation + visual. A system tuned and tested on one profile can fail quietly on the others, so the gold set covers several from the start, before profiling is built.

## How it works

- A profile can be a single label or a mix. Most real courses are mixed, so a set of labels with rough weights is more realistic than one label.
- The profile is assigned per source (and can be summarized per course). It is metadata that downstream steps read: the parser, the question-type selector, the homework generator.
- Coverage across profiles is an eval design choice. The test set should include at least one course where each important profile dominates, so that per-profile regressions show up. The current three courses do **not** cover a code-heavy subject. This is a known gap.

## Further reading

- [Product spec: Courses](../product-spec.md)
- [Gold datasets](gold-datasets.md)
