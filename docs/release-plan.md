# Release Plan

Evals and tracing run through every release.

- **v0.0 Foundations** — repo, gateway, tracing, eval runner, three test courses with hand-written expected topics and fact checks.
- **v0.1 End-to-end course** — create a course with goal and context, get an outline, take a slide lesson built from web research and the model with citations, ask questions in chat.
- **v0.2 Memory and context** — knowledge store, lesson summaries, context packets, goal-alignment reviewer.
- **v0.3 Optional sources** — uploads of all source types, relevance checks, conceptual and visual ingestion, retrieval with citations.
- **v0.4 Exercises and tracking** — placement quiz, observation and explain-back exercises, grading, mastery tracking.
- **v0.5 Voice** — spoken Q&A, narration, voice answers, turn-taking, low-latency replies.
- **v1.0 Adaptive and deployed** — spaced repetition, retention checks, adaptive sequencing, progress dashboard, production deployment.
- **v1.5 Homework** — generated assignments, rubrics, multi-format submissions, calibrated grading.
- **v2.x Hardening** — fuller multi-agent coordination, fine-tuning, model routing, cost optimization, learning outcome study.

## Epics

| Label | Epic |
|---|---|
| `epic:E0-platform` | Platform and Infrastructure |
| `epic:E1-courses` | Courses |
| `epic:E2-course-planner` | Course Planner |
| `epic:E3-research-web` | Research and Web |
| `epic:E4-knowledge-store` | Knowledge Store |
| `epic:E5-sources-ingestion` | Sources and Ingestion |
| `epic:E6-retrieval-grounding` | Retrieval and Grounding |
| `epic:E7-lessons` | Lessons (Lesson Builder, Reviewer, slide renderer) |
| `epic:E8-tutor-chat` | Tutor and Chat |
| `epic:E9-exercises-assessment` | Exercises and Assessment |
| `epic:E10-voice` | Voice |
| `epic:E11-learner-model-progress` | Learner Model and Progress |
| `epic:E12-homework` | Homework |
| `epic:E13-quality-evals` | Quality and Evals |
| `epic:E14-optimization` | Optimization |
| `epic:E15-dev-tooling-docs` | Dev Tooling and Docs |

Issue ID prefixes (used by the `backlog-writer` skill, e.g. `RET-02`) are defined in `.claude/skills/backlog-writer/SKILL.md`.
