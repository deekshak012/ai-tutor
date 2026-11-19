# Concept: LLM-as-judge

## What it is

Using a model as a **scorer**: a judge prompt gets the target's input, output, and often a reference (source text, rubric, expected answer), and returns a structured verdict (`supported` / `unsupported`, a rubric score, or a pairwise preference) plus a rationale. It's used for properties code can't check: faithfulness, groundedness, goal alignment, answer correctness on free-form text.

## Why it matters here

- RES-01: "claims are supported by their cited source (judge or fact-check)."
- RET-03 / LES-03: claim-support rate. RET-04: summary faithfulness. LES-06: off-goal detection.
- Grading homework and exercises (EX-05, HW) is a judge with a rubric. QA-03 (v0.4) calibrates it against Deeksha's labels.
- In the eval runner ([M17](../curriculum/17-eval-runner.md)) a judge is just another scorer behind the same interface, but it's a model call, so it goes through the gateway on its own tier with a versioned prompt.

## How it works

**Shapes of judging:**

- *Reference-based:* "Given this source passage, is this claim supported?" This is the most reliable kind, because the judge checks instead of recalling.
- *Rubric-based:* "Score this answer 0–3 against this rubric." Use a small discrete scale with defined levels, not 1–10.
- *Pairwise:* "Which of A and B is better?" Good for comparing prompt versions. Prone to position bias, so swap the order and judge twice.

**Known failure modes:** leniency, verbosity bias (longer answers score higher), self-preference (favoring its own model family), position bias, sensitivity to small wording changes in the judge prompt, and non-determinism, which adds a second noise source on top of the target's.

**Mitigations:** prefer deterministic scorers where possible. Ask for a structured verdict *with evidence* (quote the supporting span). Use temperature 0. Use binary or small scales. Version the judge prompt and pin its model, so a judge change isn't mistaken for a target change. Watch the cost: judges often run once per claim and can cost more than the target.

**Calibration (QA-03).** A judge is an instrument, and you have to check its accuracy before trusting it. Label a set of examples yourself, run the judge on them, and measure agreement (accuracy, Cohen's kappa, precision/recall on the "fail" class). Tune on one part of the labels and report agreement on a **held-out** part. Until a judge is calibrated, treat its scores as directional and avoid using it as a hard CI gate.

## Further reading

- [M17 — How the eval runner works](../curriculum/17-eval-runner.md) (pointer forward to QA-03)
- Zheng et al., "Judging LLM-as-a-Judge with MT-Bench and Chatbot Arena" (2023), on judge biases
- Shankar et al., "Who Validates the Validators?" (2024), on aligning judges with human preferences
- [Fact-check design](fact-check-design.md): the deterministic/hand-written alternative for factual claims
