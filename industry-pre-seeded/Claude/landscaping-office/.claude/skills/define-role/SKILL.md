---
name: define-role
description: >-
  First session: ask what this Expert is for, write MyRole.txt and stub
  workflows. Use when MyRole.txt Role status is pending or they name a new job.
---

# Define role

Generic Experts start empty. This seed is already a **Landscaping / lawn-care office**. Ask only what is still open; then write files.

## When

`MyRole.txt` **Role status** is `pending`. They name a job. New Expert folder.

## Ask (do not skip)

1. What should we **call** this Expert (their words)?
2. Which **role jobs** do you repeat (crew day, estimates, material pulls, callbacks, weather postpones, …)?
3. What **files or apps** do you already use (route CSV, price file, Jobber/LMN/Aspire export — notes only, no passwords)?
4. What does **done** look like (a crew day list that exists, columns in a CSV)?
5. What must we **never** do?
6. What is **not our job** (field crew, licensed spray, paying people)?

## Write

- Fill `MyRole.txt` (Role status: defined). Keep must-never aligned with this shop.
- Create `.claude/workflows/<name>.md` stubs only for jobs they named that are not already registered. Register them in `workflow-registry.json`. Point the method note `docs/role/work-item-method.md` at the new file.
- For each tool they named, a stub in `docs/tools/` until they drop a real example (**integrate-docs** / **remember**).
- **journal-keeper**.

Do not pretend the files are complete. Do not add a software-build design pipeline.
