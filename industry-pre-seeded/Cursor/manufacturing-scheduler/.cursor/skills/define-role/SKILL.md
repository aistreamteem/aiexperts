---
name: define-role
description: >-
  First session: ask what this Expert is for, write MyRole.txt and stub
  workflows. Use when `MyRole.txt` **Role status** is `pending` or they
  name a new job.
---

# Define role

Generic Experts start empty. Ask; then write files. This seed is already a **small-plant production scheduler** unless they change it.

## When

`MyRole.txt` **Role status** is `pending`. They name a job. New Expert folder.

## Ask (do not skip)

1. What should we **call** this Expert (their words)?
2. What **packs** do you repeat (dispatch, kit/shortage, traveler check, WIP, due-date, outside process, machine-down, pending ECO — plus any this shop adds)?
3. What **tools** do you already use (ERP export, spreadsheets, traveler PDFs, calendar file)? Notes only — no passwords.
4. What does **done** look like — what file would exist (dispatch markdown, shortage sheet, traveler exception list)?
5. What must we **never** do?
6. What is **not our job** (engineering stamp, quality auditor, paying vendors)?

## Write

- Fill `MyRole.txt` and set Role status to `defined` only after they approve.
- Create `.cursor/workflows/<name>.md` stubs: title + steps they said + a work-map YAML skeleton (`needs`, `produces`, `tool` if named, `check`). Register them in `.cursor/workflows/workflow-registry.json`. See `.cursor/workflows/README.md` and `docs/role/work-item-method.md`.
- For each tool they named, a stub in `docs/tools/`.
- **journal-keeper**.

Do not pretend the files are complete. Thin is correct. Learning starts on the first real pack. Do not copy another shop’s live job unless they said that is the job.
