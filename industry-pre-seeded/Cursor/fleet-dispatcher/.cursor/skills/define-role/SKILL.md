---
name: define-role
description: >-
  First session: ask what this Expert is for, write MyRole.txt and stub
  workflows with work-map shape. Use when `MyRole.txt` **Role status** is `pending` or they
  name a new job.
---

# Define role

Generic Experts start empty. Ask; then write files. This seed is already a **Fleet / delivery dispatcher** role; only run this when status is pending or they rename the job.

## When

`MyRole.txt` **Role status** is `pending`. They name a job. New Expert folder.

## Ask (do not skip)

1. What should we **call** this Expert (their words)?
2. What **workflows** do you repeat (names + rough steps)? For a fleet role, typical jobs are assignment pack, today’s routes, DVIR gap, exceptions, breakdown, detention, POD check, HOS questions, fuel outliers — confirm or replace.
3. What **tools** do you already use (TMS, ELD, GPS, spreadsheets, files on disk)? Notes only — no passwords.
4. What does **done** look like — what would a **command** see (a file that exists, columns in a CSV, a folder that is not empty)?
5. What must we **never** do?
6. What is **not our job** (another person / another Expert)?

## Write

- Fill `MyRole.txt` and set **Role status:** defined (only after they approve the draft, or they say skip).
- Create `.cursor/workflows/<name>.md` stubs: title + steps they said + a work-map YAML skeleton (`needs`, `produces`, `tool` if named, `check`). Register them in `.cursor/workflows/workflow-registry.json`. See `.cursor/workflows/README.md`.
- Update `docs/role/work-item-method.md` so phases match the jobs they named.
- For each tool they named, a stub in `docs/tools/` until they fill it via **remember** / **integrate-docs**.
- **journal-keeper**.

Do not pretend the files are complete. Thin is correct. Learning starts on the first real pack.
