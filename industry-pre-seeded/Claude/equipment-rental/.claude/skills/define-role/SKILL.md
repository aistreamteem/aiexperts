---
name: define-role
description: >-
  First session: ask what this Expert is for, write MyRole.txt and stub
  workflows with work-map shape. Use when `MyRole.txt` **Role status** is
  pending or they name a new job.
---

# Define role

Generic Experts start empty. Ask; then write files. This folder is already an **Equipment rental role** unless they are starting over.

## When

`MyRole.txt` **Role status** is `pending`. They name a job. New Expert folder.

## Ask (do not skip)

1. What should we **call** this Expert (their words)?
2. What **jobs** do you repeat (names + rough steps)? For a rental role, typical jobs are reservation day, contract completeness, COI missing, outgoing inspection, delivery tickets, meter exceptions, maintenance due, return damage, utilization — confirm which they actually run.
3. What **tools** do you already use (rental system, spreadsheets, PDF folders)? Notes only — no passwords.
4. What does **done** look like — what file would exist (a CSV, a missing-fields list, a folder that is not empty)?
5. What must we **never** do?
6. What is **not our job** (mechanic, collections, accounts payable, another Expert)?

## Write

- Fill `MyRole.txt` and set **Role status: defined**.
- Create `.claude/workflows/<name>.md` stubs: title + steps they said + a work-map YAML skeleton (`needs`, `produces`, `tool` if named, `check`). See `.claude/workflows/README.md`. Register each job in `.claude/workflows/workflow-registry.json`.
- For each tool they named, a stub in `docs/tools/`.
- Update `docs/role/work-item-method.md` so phases match the jobs they named.
- **journal-keeper**.

Do not pretend the files are complete. Thin is correct. Learning starts on the first real task. Do not treat starter notes as how *this* yard already works.
