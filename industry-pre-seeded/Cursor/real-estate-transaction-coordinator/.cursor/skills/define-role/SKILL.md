---
name: define-role
description: >-
  First session: ask what this Expert is for, write MyRole.txt and stub
  workflows. Use when `MyRole.txt` **Role status** is `pending` or they
  name a new job.
---

# Define role

Generic Experts start empty. Ask; then write files. This folder is already a **Real estate transaction coordinator** starter — only rerun if they are renaming the role or Role status is pending.

## When

`MyRole.txt` **Role status** is `pending`. They name a job. New Expert folder.

## Ask (do not skip)

1. What should we **call** this Expert (their words)?
2. What **workflows** do you repeat (names + rough steps)? For a TC role, typical completeness jobs are dates calendar, missing docs, disclosure completeness, option period, inspection-to-repair log, amendment log, HOA packet, closing checklist, and their wire-fraud process rows.
3. What **tools** do you already use (contract PDFs, checklists, title/HOA folders, calendars)? Notes only — no passwords.
4. What does **done** look like — what file would exist (a dates calendar, a missing-docs list, a closing pack)?
5. What must we **never** do?
6. What is **not our job** (broker, escrow, underwriter, attorney)?

## Write

- Fill `MyRole.txt` and set Role status to `defined` after they approve.
- Create `.cursor/workflows/<name>.md` stubs: title + steps they said + a work-map YAML skeleton (`needs`, `produces`, `tool` if named, `check`). Register each job in `.cursor/workflows/workflow-registry.json`.
- For each tool they named, a stub in `docs/tools/`.
- Point the Work Item method at `docs/role/work-item-method.md` (create or update if the job changed).
- **journal-keeper**.

Do not pretend the files are complete. Thin is correct. Learning starts on the first real transaction file. Do not copy a software design-and-build pipeline onto this role unless they said this Expert writes code.
