---
name: define-role
description: >-
  First session: ask what this Expert is for, write MyRole.txt and stub
  workflows. Use when MyRole.txt Role status is pending or they name a new job.
---

# Define role

Ask; then write files. This seed is already a **Nonprofit office admin** role. Only run the interview when status is pending or they want to rename/extend the role.

## When

`MyRole.txt` **Role status** is `pending`. They name a job. New Expert folder.

## Ask (do not skip)

1. What should we **call** this Expert (their words)?
2. What **workflows** do you repeat (names + rough steps)? Offer the existing registry jobs as a starting list: board-pack, donor-list, funder-gap, gift-ack-draft, grant-deadlines, grant-report, in-kind-list, minutes-index, restricted-ask.
3. What **tools** do you already use (apps, websites, files on disk)? Notes only — no passwords.
4. What does **done** look like — what would a **command** see (a file that exists, columns in a CSV, a folder that is not empty)?
5. What must we **never** do?
6. What is **not our job** (another person / another Expert)?

## Write

- Fill `MyRole.txt` and set **Role status:** `defined`. Keep must-never aligned with this role: no money movement, no 990 certification, no deductibility/FMV opinions, no donor blast product, no silent spend of restricted funds.
- Create `.claude/workflows/<name>.md` stubs: title + When to use + How to run + Initial phase + a work-map YAML skeleton (`needs`, `produces`, `tool` if named, `check`). Register each job in `.claude/workflows/workflow-registry.json`. See `.claude/workflows/README.md` and `docs/role/work-item-method.md`.
- For each tool they named, a stub in `docs/tools/` until they fill it.
- **journal-keeper**.

Do not pretend the files are complete. Thin is correct. Learning starts on the first real task.

Wait for explicit approval: "I approve the role" or "Skip role definition". Continue is not approval.
