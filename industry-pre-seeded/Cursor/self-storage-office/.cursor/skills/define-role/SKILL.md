---
name: define-role
description: >-
  First session: ask what this Expert is for, write MyRole.txt and stub
  workflows with work-map shape. Use when `MyRole.txt` **Role status** is
  pending or they name a new job.
---

# Define role

Generic Experts start empty. Ask; then write files. This seed is already **Self-storage office** with Role status defined — run this skill only if they ask to redefine the role or status is pending.

## When

`MyRole.txt` **Role status** is `pending`. They name a job. New Expert folder.

## Ask (do not skip)

1. What should we **call** this Expert (their words)?
2. What **workflows** do you repeat (names + rough steps)? For a storage office, typical jobs are occupancy, late list, move-in packet completeness, auction-file completeness, unit mix, waitlist.
3. What **tools** do you already use (SiteLink / storEDGE / SSM exports, spreadsheets, PDFs)? Notes only — no passwords.
4. What does **done** look like — what file would exist (a CSV with columns, a checklist in `out/`)?
5. What must we **never** do?
6. What is **not our job** (another person / another Expert)?

## Write

- Fill `MyRole.txt` and set **Role status:** defined.
- Create `.cursor/workflows/<name>.md` stubs: title + steps they said + a work-map YAML skeleton (`needs`, `produces`, `tool` if named, `check` empty until they approve a check). See `.cursor/workflows/README.md`.
- Register each job in `.cursor/workflows/workflow-registry.json`.
- For each tool they named, a stub in `docs/tools/`.
- Update `docs/role/work-item-method.md` if the phase list changed.
- **journal-keeper**.

Do not pretend the files are complete. Thin is correct. Learning starts on the first real task.
