---
name: define-role
description: >-
  First session: ask what this Expert is for, write MyRole.txt and stub
  workflows. Use when MyRole.txt Role status is pending or they name a new job.
---

# Define role

Ask; then write files. This folder is already seeded as **Landscaping / lawn-care office** until they change it.

## When

`MyRole.txt` **Role status** is `pending`. They name a job. New Expert folder.

## Ask (do not skip)

1. What should we **call** this Expert (their words)?
2. What **jobs** do you repeat (crew day, routes, estimates from a price file, material pulls, weather postpone, callbacks, …)?
3. What **tools** do you already use (Jobber, spreadsheets, shared drive folders)? Notes only — no passwords.
4. What does **done** look like — a pack file the office can open, columns in a CSV, a folder that is not empty?
5. What must we **never** do?
6. What is **not our job** (field crew, licensed applicator, arborist, payroll, another Expert)?

## Write

- Fill `MyRole.txt` and set Role status to `defined` only after they approve the wording (or they skip).
- Create `.cursor/workflows/<name>.md` stubs: title + When to use + How to run pointing at `docs/role/work-item-method.md` + Initial phase `role-job` + a step list (`needs`, `produces`, `tool` if named, `check`). Register each job in `.cursor/workflows/workflow-registry.json`.
- For each tool they named, a stub in `docs/tools/`.
- **journal-keeper**.

Do not pretend the files are complete. Thin is correct. Learning starts on the first real pack. Do not invent how this shop already works.
