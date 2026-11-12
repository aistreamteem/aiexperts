# Role Expert — Self-storage office

This folder is a role role Expert. You do not need to be a programmer.

1. Open **this** folder (the one with `MyRole.txt` and `AGENTS.md`).
2. Read `MyRole.txt` for scope and must-never.
3. Follow `AGENTS.md` and `.cursor/rules/expert.mdc`.
4. Shop facts/rules live under `facts/` (shared memory). Workflows live under `.cursor/workflows/`. Tools live under `docs/tools/`. Method: `docs/role/work-item-method.md`.

## Give it one small real job

1. In chat, name the job (today’s occupancy list, this unit’s move-in packet, this week’s late list, this auction file). It should use a Work Item under `work-items/<id>/` so this work does not mix with the last job.
2. Put a file you already use (SiteLink / storEDGE / SSM export, PDF, spreadsheet) in that Work Item’s `in/` folder, or drop it here and say which unit, date, or pack it belongs to.
3. Ask for the work. Example: “Here is this week’s occupancy export. Make the occupancy list. Do not invent vacant or occupied that are not in the file.”
4. When it finishes, look in **that Work Item’s** `out/` folder.

Starter notes already in `facts/` are typical for a US self-storage office, **not** how *your* shop works until you say so.

## When it is wrong, tell it

- “We call that an occupant, not a tenant.”
- “Never put gate codes or full card numbers in these lists.”
- “The late fee is in our fee file. Do not invent one.”

Say **remember this** so it stores the correction. A few real jobs plus a few corrections is enough to get going.

## Do not

- Put passwords, bank logins, or card numbers in this folder.
- Ask it to send money or pay a bill.
- Ask it to give lien or auction legal advice, invent a rate, store a keypad PIN, or hang an overlock.

## Back up this folder

Copy the **whole folder** to a safe place on a regular schedule. The notes about how your shop works, plus each Work Item, are the memory.
