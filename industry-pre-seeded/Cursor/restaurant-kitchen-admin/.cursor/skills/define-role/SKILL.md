---
name: define-role
description: >-
  First session: ask what this Expert is for, write MyRole.txt and stub
  workflows. Use when MyRole.txt Role status is pending or they name a new job.
---

# Define role

This seed is already a **Restaurant kitchen / BOH admin**. Run this skill only if `MyRole.txt` **Role status** is `pending`, or the operator wants to rename/narrow the role.

## When

`MyRole.txt` **Role status** is `pending`. They name a job. New Expert folder.

## Ask (do not skip)

1. What should we **call** this Expert (their words)?
2. What **jobs** do you repeat (prep list, walk-in count, order guide, receiving, invoice match, 86 board, par review, waste recap, catering pull, allergen quote)?
3. What **tools** do you already use (spreadsheets, vendor portal, POS export, PDF invoice folder)? Notes only — no passwords.
4. What does **done** look like — which file would exist (prep CSV columns, pack markdown in `out/`)?
5. What must we **never** do?
6. What is **not our job** (line cook, expo, paying the vendor, health inspector, FOH marketing)?

## Write

- Fill `MyRole.txt` and set Role status to defined after they approve.
- Create `.cursor/workflows/<name>.md` stubs only for jobs they named that are not already registered: title + steps + YAML skeleton (`needs`, `produces`, `tool` if named, `check` empty until they say how to check). Register them in `.cursor/workflows/workflow-registry.json`.
- For each new tool they named, a stub in `docs/tools/`.
- Point the work-item method at `docs/role/work-item-method.md` (update it if the jobs changed).
- **journal-keeper**.

Do not pretend the files are complete. Thin is correct. Do not copy a software-design pipeline onto this role.
