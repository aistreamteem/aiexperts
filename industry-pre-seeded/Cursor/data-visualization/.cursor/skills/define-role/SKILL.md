---
name: define-role
description: >-
  First session: ask what this Expert is for, write MyRole.txt and stub
  chart-pack workflows. Use when `MyRole.txt` **Role status** is `pending` or they
  name a new job.
---

# Define role

Generic Experts start empty. Ask; then write files. This seed is already **Data visualization from their files**; only run this when status is pending or they name a genuinely new job.

## When

`MyRole.txt` **Role status** is `pending`. They name a job. New Expert folder.

## Ask (do not skip)

1. What should we **call** this Expert (their words)?
2. What **chart packs** do you repeat (names + rough steps: question, file, picture, write-up)?
3. What **tools** do you already use (spreadsheets, Python, files on disk)? Notes only — no passwords.
4. What does **done** look like — what would a **command** see (a PNG that exists, columns in a CSV, a write-up file)?
5. What must we **never** do?
6. What is **not our job** (another person / another Expert)?

## Write

- Fill `MyRole.txt` (role, scope, out of scope, must never, registered workflows).
- Create `.cursor/workflows/<name>.md` stubs: title + When to use + self-contained How to run + Initial phase `question` + a work-map YAML skeleton (`needs`, `produces`, `tool` if named, `check` empty until they approve a check command). Register each job in `.cursor/workflows/workflow-registry.json`. See `.cursor/workflows/README.md`.
- Point `docs/role/work-item-method.md` at the new jobs.
- For each tool they named, a stub in `docs/tools/`.
- **journal-keeper** on `journals/expert/progress.md`.

Do not pretend the files are complete. Thin is correct. Learning starts on the first real pack.
