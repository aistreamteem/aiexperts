---
name: define-role
description: >-
  First session: ask what this Expert is for, write MyRole.txt and stub
  workflows. Use when `MyRole.txt` **Role status** is `pending` or they
  name a new job.
disable-model-invocation: false
---

# Define role

Generic Experts start empty. Ask; then write files. This seed is already **Auto shop service advisor**; only run when status is pending or they add a job.

## When

`MyRole.txt` **Role status** is `pending`. They name a job. New Expert folder.

## Ask (do not skip)

1. What should we **call** this Expert (their words)?
2. What **workflows** do you repeat (names + rough steps)? For a service counter, typical jobs are write-up, open board, MPI copy, estimate, auth gap, additional findings, parts status, comeback, pickup invoice.
3. What **tools** do you already use (shop software, labor guide, MPI form, files on disk)? Notes only — no passwords.
4. What does **done** look like — what file would exist (RO pack, CSV columns, folder that is not empty)?
5. What must we **never** do?
6. What is **not our job** (technician diagnosis, inspection stamp, sending money)?

## Write

- Fill `MyRole.txt`.
- Create `.claude/workflows/<name>.md` stubs: title + steps they said + a work-map YAML skeleton (`needs`, `produces`, `tool` if named, `check` empty until they approve a check). Register each job in `.claude/workflows/workflow-registry.json`. See `.claude/workflows/README.md`.
- For each tool they named, a stub in `docs/tools/` until **remember** fills it.
- Point `docs/role/work-item-method.md` at the live jobs.
- **journal-keeper**. Then wait for the first real RO pack.

Do not pretend the files are complete. Thin is correct. Learning starts on the first real ticket. Do not treat starter notes as *this* shop's rules until they say so.
