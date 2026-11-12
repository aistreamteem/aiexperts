---
name: define-role
description: >-
  First session: ask what this Expert is for, write MyRole.txt and stub
  workflows. Use when `MyRole.txt` **Role status** is `pending` or they
  name a new job.
---

# Define role

Generic Experts start empty. Ask; then write files. This seed is already a **Hotel / inn front role**; only run the interview if status is pending or they rename the job.

## When

`MyRole.txt` **Role status** is `pending`. They name a job. New Expert folder.

## Ask (do not skip)

1. What should we **call** this Expert (their words)?
2. What **jobs** do you repeat (names + rough steps)? For a hotel role, examples they may confirm: arrivals list, due-outs, house count, folio exceptions, group block vs pickup, no-shows, night-audit packet check.
3. What **tools** do you already use (PMS name, spreadsheets, PDFs on disk)? Notes only — no passwords, no card PAN.
4. What does **done** look like — what file would exist (arrivals CSV, exception list in `out/`)? If they only have words, still write them, then ask how a later check would know the step passed.
5. What must we **never** do?
6. What is **not our job** (night audit they run, card running, ADA legal, another Expert)?

Wait for explicit approval (“I approve the role”) before rewriting live files as defined. “Skip role definition” keeps the starter pack and sets status to skipped.

## Write

- Fill `MyRole.txt` (status `defined` after approval).
- Create `.cursor/workflows/<name>.md` stubs: title + When to use + How to run (self-contained steps for **continue**; no deleted process skills) + Initial phase + a step list (`needs`, `produces`, `tool` if named, `check`). Register each job in `.cursor/workflows/workflow-registry.json`. See `.cursor/workflows/README.md`.
- Align `docs/role/work-item-method.md` with the jobs they named.
- For each tool they named, a stub in `docs/tools/` until they fill it.
- **journal-keeper**.

Do not pretend the files are complete. Thin is correct. Learning starts on the first real task.
