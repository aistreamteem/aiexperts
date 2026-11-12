# Role Expert — Job coordinator in a trade shop

This folder is a role role Expert. You do not need to be a programmer.

1. Open **this** folder (the one with `MyRole.txt` and `AGENTS.md`).
2. Read `MyRole.txt` for scope and must-never.
3. Follow `AGENTS.md` and `.cursor/rules/expert.mdc`.
4. Shop facts/rules live under `facts/` (operations memory). Workflows live under `.cursor/workflows/`. Tools live under `docs/tools/`. Method: `docs/role/work-item-method.md`.

## Give it one small real job

1. In chat, name the job (today’s board, this ticket’s packing list, this permit pack). It should use a Work Item under `work-items/<id>/` so this work does not mix with the last job.
2. Put a file you already use (schedule export, sold PDF, spreadsheet) in that Work Item’s `in/` folder, or drop it here and say which ticket, day, or crew it belongs to.
3. Ask for the work. Example: “Here is today’s schedule export. Make the daily board. Do not invent ETAs or packing-list SKUs that are not in the file.”
4. When it finishes, look in **that Work Item’s** `out/` folder.

Starter notes already in `facts/` are typical for a US trade dispatch role, **not** how *your* shop works until you say so.

## When it is wrong, tell it

- “We call that a ticket, not a work order.”
- “Never put lockbox codes in these lists.”
- “The packing-list columns are in our sheet. Do not invent SKUs.”

Say **remember this** so it stores the correction. A few real jobs plus a few corrections is enough to get going.

## Do not

- Put passwords, bank logins, or card numbers in this folder.
- Ask it to send money or pay a bill.
- Ask it to claim a license, pass an inspection, diagnose over the phone, or store gate/alarm codes.

## Back up this folder

Copy the **whole folder** to a safe place on a regular schedule. The notes about how your shop works, plus each Work Item, are the memory.
