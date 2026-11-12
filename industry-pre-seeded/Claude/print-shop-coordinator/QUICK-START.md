# Role Expert — Print shop job coordinator

This folder is a role role Expert. You do not need to be a programmer.

1. Open **this** folder (the one with `MyRole.txt` and `CLAUDE.md`).
2. Read `MyRole.txt` for scope and must-never.
3. Follow `CLAUDE.md` and `.claude/rules/expert.md`.
4. Shop facts/rules live under `facts/` (shared memory). Workflows live under `.claude/workflows/`. Tools live under `docs/tools/`. Method: `docs/role/work-item-method.md`.

## Give it one small real job

1. In chat, name the job (today’s job board, this ticket’s preflight, this week’s stock vs jobs). It should use a Work Item under `work-items/<id>/` so this work does not mix with the last job.
2. Put a file you already use (ticket sheet, proof folder export, stock CSV, mill-order sheet, press calendar) in that Work Item’s `in/` folder, or drop it here and say which ticket, board day, or pack it belongs to.
3. Ask for the work. Example: “Here is this week’s ticket export. Make the job board. Do not invent dues that are not in the file.”
4. When it finishes, look in **that Work Item’s** `out/` folder.

Starter notes already in `facts/` are typical for a US print-shop coordinator role, **not** how *your* shop works until you say so.

## When it is wrong, tell it

- “We call that a jacket, not a job ticket.”
- “Never put full card numbers in these lists.”
- “Bleed is on our preflight checklist. Do not invent one.”

Say **remember this** so it stores the correction. A few real jobs plus a few corrections is enough to get going.

## Do not

- Put passwords, bank logins, or card numbers in this folder.
- Ask it to send money or pay a mill, vendor, or carrier.
- Ask it for a copyright legal opinion, a press-operator stamp, or an NCOA product.

## Back up this folder

Copy the **whole folder** to a safe place on a regular schedule. The notes about how your shop works, plus each Work Item, are the memory.
