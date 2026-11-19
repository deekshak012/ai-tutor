# Concept: Fact-check design

## What it is

A fact check is a single, self-contained claim with a known verdict (true or false), tagged to one topic. An eval uses it to test whether generated content gets that point right. Fact-check design is about writing these claims so they are easy to score, hard to pass by accident, and clear about what went wrong when they fail.

## Why it matters here

Each QA-02 test course has at least five fact checks ([M18](../curriculum/18-test-courses-and-fact-checks.md)). The Lesson Builder's slide-accuracy eval (LES-03, [M11](../curriculum/11-lesson-builder-workflow.md)) uses them to catch slides that state something wrong. The grounding claim-support eval (RET-03, [M09](../curriculum/09-grounding-and-citations.md)) uses them to catch claims that are faithfully cited but still incorrect.

## How it works

Properties of a good fact check:

1. **Atomic**: one idea per claim. "A Type I error is a false positive and its rate is α" is really two checks.
2. **Unambiguous**: an expert would give the verdict without needing to hedge. Leave out claims that depend on convention or are disputed. If something has edge cases, state the condition in the claim (for example, "for independent samples with finite variance…").
3. **Include misconceptions**: write false claims that capture common errors ("a p-value is the probability the null is true"). A vague lesson can avoid contradicting true claims, but it can't pass a check that asks whether it stated a specific wrong idea.
4. **Topic-tagged**: each check is tied to one expected topic, so the scorer only applies it to slides about that topic and a failure points to a specific lesson.
5. **Scorable**: a judge model, given the slide and the claim, can answer "contradicts / states the false claim / consistent / not addressed". "Not addressed" counts as neutral for accuracy. Coverage is a separate metric.
6. **Explained**: a short note on why a false claim is false helps whoever reviews the failure.

Common pitfalls: claims that are only true under one textbook's definitions, claims that are too broad to falsify ("regression is useful"), and a set made up only of true claims.

## Further reading

- [Gold datasets](gold-datasets.md)
- [LLM-as-judge](llm-as-judge.md): how contradiction gets scored.
- Literature on factual-consistency evaluation and claim-level verification (for example, the FEVER fact-verification task).
