---
name: define-role
description: >-
  First session: ask what this Expert is for, write MyRole.txt and stub
  workflows. Use when `MyRole.txt` **Role status** is `pending` or they
  name a new job.
---

# Define role

Generic Experts start empty. Ask; then write files. This seed is already **defined** as Childcare center office (not the teacher). Run this skill only if status is pending or they ask to redefine.

## When

`MyRole.txt` **Role status** is `pending`. They name a job. New Expert folder.

## Ask (do not skip)

1. What should we **call** this Expert (their words)?
2. What **workflows** do you repeat (names + rough steps)? For a childcare office, examples are attendance day, missing enrollment forms, pickup list check — only keep what they actually do.
3. What **tools** do you already use (childcare software exports, spreadsheets, PDF folders)? Notes only — no passwords.
4. What does **done** look like — what file would exist (attendance list, missing-forms grid, pickup check)?
5. What must we **never** do?
6. What is **not our job** (teacher, nurse, director, inspector, another Expert)?

## Write

- Fill `MyRole.txt` and set **Role status:** `defined`.
- Create `.cursor/workflows/<name>.md` stubs: title + steps they said + a work-map YAML skeleton (`needs`, `produces`, `tool` if named, `check` empty until they approve a check). See `.cursor/workflows/README.md`.
- Register each job in `.cursor/workflows/workflow-registry.json`.
- Update `docs/role/work-item-method.md` so phases match what they said.
- For each tool they named, a stub in `docs/tools/`.
- **journal-keeper**.

Do not pretend the files are complete. Thin is correct. Learning starts on the first real task. Do not copy a software developer pipeline onto this role.
