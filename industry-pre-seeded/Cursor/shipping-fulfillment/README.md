# Role Expert — Shipping / fulfillment role

This folder is a role role Expert. You do not need to be a programmer.

1. Open **this** folder (the one with `MyRole.txt` and `AGENTS.md`).
2. Read `MyRole.txt` for scope and must-never.
3. Follow `AGENTS.md` and `.cursor/rules/expert.mdc`.
4. Shop facts/rules live under `facts/` (shared + operations memory). Workflows live under `.cursor/workflows/`. Tools live under `docs/tools/`. Method: `docs/role/work-item-method.md`. Journals live under `journals/work-items/<id>/`.

## Give it one small real job

1. In chat, name the job (today’s pick wave, this BOL pack, this day’s manifest, this RMA sheet). It should use a Work Item under `work-items/<id>/` so this work does not mix with the last job.
2. Put a file you already use (WMS export, BOL PDF, scale export, label folder, RMA spreadsheet) in that Work Item’s `in/` folder, or drop it here and say which order, wave, truck, or day it belongs to.
3. Ask for the work. Example: “Here is this morning’s pick export. Make the pick list. Do not invent locations that are not in the file.”
4. When it finishes, look in **that Work Item’s** `out/` folder.

Starter notes already in `facts/` are typical for a US ship-from role, **not** how *your* shop works until you say so.

## When it is wrong, tell it

Say **remember this** so it stores the correction. A few real jobs plus a few corrections is enough to get going.

## Do not

- Put passwords, bank logins, or card numbers in this folder.
- Ask it to send money or pay a freight bill.
- Ask it to invent a scale weight, DIM, or NMFC class, stamp hazmat, file AES, or count inbound receipts.

## Back up this folder

Copy the **whole folder** to a safe place on a regular schedule. The notes about how your shop works, plus each Work Item, are the memory.
