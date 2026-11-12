---
name: define-role
description: >-
  First session: ask what this Expert is for, write MyRole.txt and stub
  workflows. Use when MyRole.txt Role status is pending or they name a new job.
---

# Define role

## When

`MyRole.txt` **Role status** is `pending`. They name a job. New Expert folder.

## Ask (do not skip)

1. What should we **call** this Expert (their words)?
2. What **jobs** do you repeat (names + rough steps)? Typical bookkeeping jobs: month-end, bank rec, card coding, vendor bills, AR questions.
3. What **tools** do you already use (QuickBooks, spreadsheets, bank CSV, receipt folder)? Notes only — no passwords.
4. What does **done** look like — what would a **command** see (a CSV with date, amount, and account; a rec pack in `out/`)?
5. What must we **never** do?
6. What is **not our job** (CPA, payroll filer, bill pay)?

## Write

- Fill `MyRole.txt` and set Role status to defined after they approve (`I approve the role`).
- Create `.claude/workflows/<name>.md` stubs: when to use, how to run (continue + this file + journal-keeper), and a work-map YAML (`needs`, `produces`, `tool`, `check`). See `.claude/workflows/README.md`. Register each job in `workflow-registry.json`.
- For each tool they named, a stub in `docs/tools/` until they confirm details.
- **journal-keeper**.

Do not pretend the files are complete. Thin is correct. Learning starts on the first real pack. Align new jobs with `docs/role/work-item-method.md` (intake → code → rec → close pack) unless they described a different shop loop.
