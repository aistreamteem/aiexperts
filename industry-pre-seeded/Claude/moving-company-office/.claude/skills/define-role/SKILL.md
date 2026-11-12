---
name: define-role
description: >-
  First session: ask what this Expert is for, write MyRole.txt and stub
  workflows with work-map shape. Use when `MyRole.txt` **Role status** is
  pending or they name a new job.
---

# Define role

Ask; then write files. This seed is already a **Moving company office** role. Re-run only if Role status is pending or they want a different job.

## When

`MyRole.txt` **Role status** is `pending`. They name a job. New Expert folder.

## Ask (do not skip)

1. What should we **call** this Expert (their words)?
2. What **workflows** do you repeat (names + rough steps)? For a moving office, typical jobs are estimate from rate file, inventory completeness, crew day, truck calendar, materials, delivery windows, weigh tickets, claims routing — confirm or replace.
3. What **tools** do you already use (jobber, spreadsheet, scale tickets, rate book)? Notes only — no passwords.
4. What does **done** look like — what would a **command** see (a file that exists, columns in a CSV, a folder that is not empty)?
5. What must we **never** do?
6. What is **not our job** (tariff lawyer, scale, payroll, DOT certifier, another Expert)?

## Write

- Fill `MyRole.txt` (Role status: defined). Keep must-never aligned with this shop.
- Create `.claude/workflows/<name>.md` stubs: title + steps they said + a work-map YAML skeleton (`needs`, `produces`, `tool` if named, `check` when they can name a file). Register each job in `.claude/workflows/workflow-registry.json`.
- For each tool they named, a stub in `docs/tools/`.
- Update `docs/role/work-item-method.md` if the phase list changed.
- **journal-keeper**.

Do not pretend the files are complete. Thin is correct. Learning starts on the first real task. Do not copy a software HLD/DD pipeline onto this role unless they are actually a developer.
