---
name: define-role
description: >-
  First session: ask what this Expert is for, write MyRole.txt and stub
  workflows. Use when `MyRole.txt` **Role status** is `pending` or they
  name a new job.
---

# Define role

Generic Experts start empty. Ask; then write files. This seed is already a **Janitorial / contract-cleaning office** role; only run this skill if Role status is pending or they explicitly rename the job.

## When

`MyRole.txt` **Role status** is `pending`. They name a job. New Expert folder.

## Ask (do not skip)

1. What should we **call** this Expert (their words)?
2. What **workflows** do you repeat (names + rough steps)? For a cleaning office those are often night board, quality pack, complaints, missed service, supply par, SDS gaps, extra-work auth, holiday coverage, key log.
3. What **tools** do you already use (apps, websites, files on disk)? Notes only — no passwords, alarm codes, or keypad PINs.
4. What does **done** look like — what would a **command** see (a file that exists, columns in a CSV, a folder that is not empty)?
5. What must we **never** do?
6. What is **not our job** (another person / another Expert)?

## Write

- Fill `MyRole.txt` and set Role status to defined after they approve (`I approve the role`) or skipped (`Skip role definition`).
- Create `.cursor/workflows/<name>.md` stubs: title + steps they said + artifact paths under the Work Item (`work/`, `out/`) + a check command when they can name one. Register each job in `.cursor/workflows/workflow-registry.json`.
- For each tool they named, a stub in `docs/tools/`.
- Update `docs/role/work-item-method.md` so phases match what they said.
- **journal-keeper**.

Do not pretend the files are complete. Thin is correct. Learning starts on the first real pack. Do not copy another shop’s board as their live job unless they said that is the job.
