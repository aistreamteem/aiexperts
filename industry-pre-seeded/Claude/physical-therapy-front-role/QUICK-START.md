# Role Expert — Physical therapy front role

This folder is a role role Expert. You do not need to be a programmer.

1. Open **this** folder (the one with `MyRole.txt` and `CLAUDE.md`).
2. Read `MyRole.txt` for scope and must-never.
3. Follow `CLAUDE.md` and `.claude/rules/expert.md`.
4. Shop facts/rules live under `facts/` (shared + operations memory). Workflows live under `.claude/workflows/`. Tools live under `docs/tools/`. Method: `docs/role/work-item-method.md`.

## Give it one small real job

1. In chat, name the job (today’s day list, this remaining-visits pack, this referral folder). It should use a Work Item under `work-items/<id>/` so this work does not mix with the last job.
2. Put a file you already use (schedule export, auth tracker, screenshot, PDF) in that Work Item’s `in/` folder, or drop it here and say which clinic date or pack it belongs to.
3. Ask for the work. Example: “Here is this week’s schedule export. Make the day list. Do not invent remaining visits that are not in the file.”
4. When it finishes, look in **that Work Item’s** `out/` folder.

Starter notes already in `facts/` are typical for a US outpatient PT role, **not** how *your* clinic works until you say so.

## When it is wrong, tell it

- “We call that a follow-up, not a re-eval.”
- “Never put full Social Security numbers in these lists.”
- “The cancel fee is in our policy file. Do not invent one.”

Say **remember this** so it stores the correction. A few real jobs plus a few corrections is enough to get going.

## Do not

- Put passwords, bank logins, or card numbers in this folder.
- Ask it to send money or pay a bill.
- Ask it to treat, diagnose, invent remaining visits, or give a Medicare billing opinion.

## Back up this folder

Copy the **whole folder** to a safe place on a regular schedule. The notes about how your clinic works, plus each Work Item, are the memory.
