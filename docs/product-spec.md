# Product Spec: AI Tutor

A generic, course-based AI tutor that teaches any subject interactively, with slides, chat, voice, exercises, and homework feedback, and adapts the course to how the learner performs.

## Courses

Courses are the central object:

- The user creates a course and defines what they want to learn and why, their current level (confirmed by a short placement quiz), their target outcome, time per week and any deadline, preferred learning style, and topics to include or skip.
- Sources are optional. A course can run with no uploads at all. Optional sources: books (PDF or EPUB), articles and web links, video or lecture transcripts, the user's own notes or class slides, a syllabus, past exams or practice questions, examples of work they admire, samples of their own current work, glossaries or reference sheets.
- Uploaded sources get a relevance check that advises but never blocks: relevant, partly relevant (naming which chapters or sections fit), or not relevant, plus a warning for level mismatches. The user decides.
- Source material can be conceptual or visual. Each source gets a subject profile (text-heavy, visual, math, code, diagrams, or mixed) that guides how it's parsed, which question types fit, and which homework formats make sense. Images are one optional part of ingestion. For conceptual material, extract definitions, arguments, claims and evidence, examples, and how ideas connect.

## Web research

- Web search supplements the course. Uploaded sources are primary when present, and answers label which source type each claim came from.
- Web sources are scored for quality, low-quality ones are filtered out, every claim links to its source, and content is summarized rather than copied.
- When sources conflict, show both views and explain the difference.
- Web content is treated strictly as data, never as instructions (prompt injection defense, with tests).
- Per-course setting: sources only, or sources plus web.

## Lessons

- Delivered as slides. The model generates structured slide data (title, images, text, speaker notes, slide type) and the frontend renders it.
- Images come from the course sources first, then the web. When no suitable image exists, teaching diagrams are generated as code (flowcharts, labeled illustrations, concept maps).
- A chat panel beside the slides knows the current slide, supports tangents and returning to the lesson, and lessons can be paused and resumed.

## Voice

- Spoken questions and answers, narrated slides, voice answers to exercises, interruptions and natural turn-taking, spoken rewrites of equations, code, and tables, and replies starting in about 1-2 seconds.

## Exercises

- "What do you see?" observation exercises on images, charts, diagrams, or code: the learner interprets, then the tutor confirms what's right, corrects misreadings, and adds what was missed, highlighting the image regions it's discussing.
- Explain-it-back exercises, question types chosen by subject profile, and free-form answer grading against sources.

## Homework

- Assignments generated per lesson, each with a rubric. Submissions can be written answers, images, worked problems, code, or audio. Feedback is marked directly on image submissions. The grader is calibrated against the user's own labels, and results feed the learner model.

## Tracking learning

- Baseline from the placement quiz, concept-level mastery, retention checks days or weeks later, homework scores over time, confidence versus actual performance, and progress toward the stated goal, shown on a progress dashboard.

## Knowledge store

- Everything researched or taught is stored with its content, concept tags, source type (uploaded source, web, or model-generated), verification status (grounded, checked, or unverified), date gathered, and whether it has been taught to this learner.
- Model-generated content never becomes trusted without being checked against real sources.
- Verified general knowledge can be shared across courses and users. Learner notes, mistakes, and progress stay private.
- Lessons reference earlier material for continuity.

## Course structure and context

- Hierarchy: course goal, course plan (skill map), modules, lessons, slides.
- Each lesson is generated from a compact context packet, never the full course history: course goal and user context, module objective, the lesson's concepts and prerequisites, learner mastery for those concepts, a rolling summary of what's been taught, and relevant items from the knowledge store and sources.
- A reviewer step checks each module and lesson against the stated goal. The user can view and edit the course outline at any time.

## Hard rule

No AI art generation for end use. Generation is allowed only to teach, such as diagrams or showing a correction. See [ADR 0004](decisions/0004-no-ai-art-generation-for-end-use.md).
