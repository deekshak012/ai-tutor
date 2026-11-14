---
name: explain
description: Deep walkthrough of a file, function, or concept in the ai-tutor codebase — how it works, how data flows, where data is stored, the concepts involved, and questions to check understanding. Read-only, never modifies code. Use for /explain requests.
allowed-tools: Read, Grep, Glob
disallowed-tools: Edit, Write, Bash, NotebookEdit
arguments: [target]
---

Explain `$target` (a file path, function name, or concept) to Deeksha, who is learning how this system works.

Produce:

1. **How it works** — plain walkthrough, referencing real `file.py:function_name` locations.
2. **Data flow** — what data comes in, what's stored or produced, and where (name the actual tables/files; a small Mermaid diagram if it helps).
3. **Concepts involved** — name each concept used (e.g. embeddings, knowledge tracing, context packets) and link to `docs/concepts/<slug>.md` if that doc exists.
4. **Check your understanding** — 2-4 questions, and optionally one small experiment to try, to confirm the explanation landed.

Never edit, write, or run anything that changes repo state — this is read-only, even if asked to "fix" or "clean up" something while explaining it. If asked to make a change, say so and suggest the user ask for that separately.
