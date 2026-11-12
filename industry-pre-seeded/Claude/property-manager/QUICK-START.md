# Role Expert — Property manager write-ups

This folder is a role Expert. You do not need to be a programmer.

1. Open **this** folder (the one with `MyRole.txt` and `CLAUDE.md`).
2. Read `MyRole.txt` for scope and must-never.
3. Follow `CLAUDE.md` and `.claude/rules/expert.md`.
4. Shop facts/rules live under `facts/` (shared memory). Workflows live under `.claude/workflows/`. Tools live under `docs/tools/`. Method: `docs/role/work-item-method.md`.

## Give it one small real job

1. In chat, name the job (this week’s work-order export, this vacant unit’s make-ready, November’s owner pack). It should use a Work Item under `work-items/<id>/` so this work does not mix with the last job.
2. Put a file you already use (PMS export, PDF, spreadsheet) in that Work Item’s `in/` folder, or drop it here and say which property, unit, or period it belongs to.
3. Ask for the work. Example: “Here is this week’s work-order export. Make the open-ticket list. Do not invent a unit that is not in the file.”
4. When it finishes, look in **that Work Item’s** `out/` folder.

Starter notes already in `facts/` are typical for a US property-management office, **not** how *your* shop works until you say so.

## When it is wrong, tell it

- “We call that a ticket, not a work order.”
- “Never put full Social Security numbers in these lists.”
- “The late fee is in our policy file. Do not invent one.”

Say **remember this** so it stores the correction. A few real jobs plus a few corrections is enough to get going.

## Do not

- Put passwords, bank logins, or card numbers in this folder.
- Ask it to send money or pay a bill.
- Ask it to give eviction or fair-housing legal advice, certify a unit as up to code, or draft a lockout.

## Back up this folder

Copy the **whole folder** to a safe place on a regular schedule. The notes about how your shop works, plus each Work Item, are the memory.
