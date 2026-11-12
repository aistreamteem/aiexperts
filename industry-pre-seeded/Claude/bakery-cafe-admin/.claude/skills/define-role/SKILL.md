---
name: define-role
description: >-
  First session: ask what this Expert is for, write MyRole.txt and stub
  workflows. Use when MyRole.txt Role status is pending or they name a new job.
---

# Define role

This seed is already a **Bakery / cafe production office**. Run this skill only if `MyRole.txt` **Role status** is `pending`, or the operator wants to rename/narrow the role.

## When

`MyRole.txt` **Role status** is `pending`. They name a job. New Expert folder.

## Ask (do not skip)

1. What should we **call** this Expert (their words)?
2. What **jobs** do you repeat (bake list, case par, wholesale day, cake board, receiving, allergen index, holiday bake-up, waste recap)?
3. What **tools** do you already use (spreadsheets, bakery software, PDF invoice folder)? Notes only — no passwords.
4. What does **done** look like — which file would exist (bake-list CSV columns, pack markdown in `out/`)?
5. What must we **never** do?
6. What is **not our job** (mixer, decorator, driver, paying the mill, health inspector)?

## Write

- Fill `MyRole.txt` and set Role status to defined after they approve.
- Create `.claude/workflows/<name>.md` stubs only for jobs they named that are not already registered: title + steps + YAML skeleton (`needs`, `produces`, `tool` if named, `check` empty until they say how to check). Register them in `.claude/workflows/workflow-registry.json`.
- For each new tool they named, a stub in `docs/tools/`.
- Point the work-item method at `docs/role/work-item-method.md` (update it if the jobs changed).
- **journal-keeper**.

Do not pretend the files are complete. Thin is correct. Do not copy a software-design pipeline onto this role.
