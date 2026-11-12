---
name: define-role
description: >-
  First session: ask what this Expert is for, write MyRole.txt and stub
  workflows with work-map shape. Use when `MyRole.txt` **Role status** is `pending` or they
  name a new job.
---

# Define role

Generic Experts start empty. Ask; then write files. This seed is already an **Optometry front role (not the doctor)** role; only run this skill if Role status is pending or the operator names a new job.

## When

`MyRole.txt` **Role status** is `pending`. They name a job. New Expert folder.

## Ask (do not skip)

1. What should we **call** this Expert (their words)?
2. What **workflows** do you repeat (names + rough steps)? For an optometry front role, typical file jobs are day list, eligibility screenshot, wait list, frame/lens order completeness, missing Rx on order, pickup notify list, recall list, redo log, and day close.
3. What **tools** do you already use (EHR exports, spreadsheets, files on disk)? Notes only — no passwords.
4. What does **done** look like — what file would exist (CSV columns, a completeness list, an index)? If they only have words, write them, then propose a check command and wait for approval before the first real run.
5. What must we **never** do?
6. What is **not our job** (doctor, optician, owner, another Expert)?

## Write

- Fill `MyRole.txt` and set Role status to `defined` only after they approve the role text.
- Create `.cursor/workflows/<name>.md` stubs: title + steps they said + a work-map YAML skeleton (`needs`, `produces`, `tool` if named, `check` empty until they approve a check). Register each job in `.cursor/workflows/workflow-registry.json`. See `.cursor/workflows/README.md`.
- For each tool they named, a stub in `docs/tools/` until they describe how *this* office uses it.
- Update `docs/role/work-item-method.md` if the phase list changed.
- **journal-keeper**.

Do not pretend the files are complete. Thin is correct. Learning starts on the first real task.
