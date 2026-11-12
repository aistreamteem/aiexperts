# Role Expert — Facilities / plant maintenance planner

This folder is a role role Expert. You do not need to be a programmer.

1. Open **this** folder (the one with `MyRole.txt` and `CLAUDE.md`).
2. Read `MyRole.txt` for scope and must-never.
3. Follow `CLAUDE.md` and `.claude/rules/expert.md`.
4. Shop facts/rules live under `facts/` (operations memory). Workflows live under `.claude/workflows/`. Tools live under `docs/tools/`. Method: `docs/role/work-item-method.md`.

## Give it one small real job

1. In chat, name the job (today’s dispatch list, this week’s PM due, this crib pull). It should use a Work Item under `work-items/<id>/` so this work does not mix with the last job.
2. Put a file you already use (CMMS export, crib CSV, procedure PDF) in that Work Item’s `in/` folder, or drop it here and say which work order, asset, or week it belongs to.
3. Ask for the work. Example: “Here is this week’s work-order export. Make the dispatch list. Do not invent a craft that is not in the file.”
4. When it finishes, look in **that Work Item’s** `out/` folder.

Starter notes already in `facts/` are typical for a US in-house maintenance role, **not** how *your* plant works until you say so.

## When it is wrong, tell it

- “We call that a ticket, not a work order.”
- “Never put lockbox codes or badge secrets in these lists.”
- “The PM interval is in our calendar file. Do not invent one.”

Say **remember this** so it stores the correction. A few real jobs plus a few corrections is enough to get going.

## Do not

- Put passwords, bank logins, card numbers, alarm codes, or badge secrets in this folder.
- Ask it to send money or pay a vendor.
- Ask it to stamp OSHA, stamp PE drawings, diagnose as the technician, or sell a CMMS.

## Back up this folder

Copy the **whole folder** to a safe place on a regular schedule. The notes about how your plant works, plus each Work Item, are the memory.
