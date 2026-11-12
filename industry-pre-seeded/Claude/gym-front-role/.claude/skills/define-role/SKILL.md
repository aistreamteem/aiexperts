---
name: define-role
description: >-
  First session: ask what this Expert is for, write MyRole.txt and stub
  workflows with work-map shape. Use when `MyRole.txt` **Role status** is pending
  or they name a new job.
---

# Define role

Generic Experts start empty. Ask; then write files. This seed is already a **Gym / fitness front role** expert; run this skill only if status is pending or the operator wants a new job added.

## When

`MyRole.txt` **Role status** is `pending`. They name a job. New Expert folder.

## Ask (do not skip)

1. What should we **call** this Expert (their words)?
2. What **workflows** do you repeat (names + rough steps)? For a gym role, typical jobs are check-in day, access-flag exceptions, guest-pass log, missing waivers, freeze/cancel list, failed-draft list, class roster, PT session counts, retail close.
3. What **tools** do you already use (membership software exports, spreadsheets, waiver PDF folders)? Notes only — no passwords, no card PAN.
4. What does **done** look like — what would a **command** see (a file that exists, columns in a CSV, a folder that is not empty)? If they only have words, still write them, then propose a check command and get approval before the first real run.
5. What must we **never** do? (Default gym role: no medical/diet advice, no running EFT, no storing PAN, no inventing dues.)
6. What is **not our job** (trainer on the floor, clinician, collections attorney)?

## Write

- Fill `MyRole.txt`. Keep **Work-item method** pointing at `docs/role/work-item-method.md` or update that note if the role changed.
- Create `.claude/workflows/<name>.md` stubs: title + steps they said + a work-map YAML skeleton (`needs`, `produces`, `tool` if named, `check` empty until they approve a check). Register the job in `.claude/workflows/workflow-registry.json`. See `.claude/workflows/README.md`.
- For each tool they named, a stub in `docs/tools/` until they fill it.
- **journal-keeper**.

Do not pretend the files are complete. Thin is correct. Learning starts on the first real task. Do not treat starter notes as how *this* club already works.
