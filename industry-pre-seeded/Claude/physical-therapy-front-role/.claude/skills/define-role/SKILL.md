---
name: define-role
description: >-
  First session: ask what this Expert is for, write MyRole.txt and stub
  workflows with work-map shape. Use when `MyRole.txt` **Role status** is `pending` or they
  name a new job.
---

# Define role

Generic Experts start empty. Ask; then write files.

## When

`MyRole.txt` **Role status** is `pending`. They name a job. New Expert folder.

## Ask (do not skip)

1. What should we **call** this Expert (their words)?
2. What **workflows** do you repeat (names + rough steps)?
3. What **tools** do you already use (apps, websites, files on disk)? Notes only — no passwords.
4. What does **done** look like — what would a **command** see (a file that exists, columns in a CSV, a folder that is not empty)? If they only have words, still write them, then propose a check command and wait for approval before the first real run.
5. What must we **never** do?
6. What is **not our job** (another person / another Expert)?

## Write

- Fill `MyRole.txt`.
- Create `.claude/workflows/<name>.md` stubs: title + steps they said + a work-map YAML skeleton (`needs`, `produces`, `tool` if named, `check` empty until they approve a check). See `.claude/workflows/README.md` and `docs/role/work-item-method.md`.
- Register each new job in `.claude/workflows/workflow-registry.json`.
- For each tool they named, a stub in `docs/tools/`.
- **journal-keeper**.

Do not pretend the files are complete. Thin is correct. Learning starts on the first real task.
