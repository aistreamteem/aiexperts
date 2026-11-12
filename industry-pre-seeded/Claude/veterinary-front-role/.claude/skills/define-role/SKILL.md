---
name: define-role
description: >-
  First session: ask what this Expert is for, write MyRole.txt and stub
  workflows. Use when `MyRole.txt` **Role status** is `pending` or they
  name a new job.
---

# Define role

Ask; then write files. This seed is already a veterinary front role; use this skill only if Role status is pending or the operator is renaming the job.

## When

`MyRole.txt` **Role status** is `pending`. They name a job. New Expert folder.

## Ask (do not skip)

1. What should we **call** this Expert (their words)?
2. What **workflows** do you repeat (names + rough steps)? Offer the current clinic-role jobs as a starting list: day appointments, emergency flag, new-client forms, records in, records out, reminder list, estimate from prices, checkout list, board dropoff.
3. What **tools** do you already use (PIMS export, PDF folders, spreadsheets)? Notes only — no passwords.
4. What does **done** look like — which files exist in a Work Item `out/` folder?
5. What must we **never** do?
6. What is **not our job** (veterinarian, biller, another Expert)?

## Write

- Fill `MyRole.txt` and set **Role status:** defined.
- Create `.claude/workflows/<name>.md` stubs: title + steps they said + `needs` / `produces` / `tool` / `check` when known. Register each job in `.claude/workflows/workflow-registry.json`. See `.claude/workflows/README.md` and `docs/role/work-item-method.md`.
- For each tool they named, a stub in `docs/tools/` until they fill it.
- **journal-keeper**.

Do not pretend the files are complete. Thin is correct. Learning starts on the first real task. Do not invent this clinic’s fees, durations, or coverage.
