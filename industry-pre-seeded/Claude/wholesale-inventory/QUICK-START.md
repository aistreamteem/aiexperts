# Role Expert — Wholesale / inventory role

This folder is a role role Expert. You do not need to be a programmer.

1. Open **this** folder (the one with `MyRole.txt` and `CLAUDE.md`).
2. Read `MyRole.txt` for scope and must-never.
3. Follow `CLAUDE.md` and `.claude/rules/expert.md`.
4. Shop facts/rules live in `facts/facts-shared.md` / `facts/rules-shared.md` and `facts/facts-operations.md` / `facts/rules-operations.md`. Workflows live under `.claude/workflows/`. Tools live under `docs/tools/`. Method: `docs/role/work-item-method.md`.

## Give it one small real job

1. In chat, name the job (this receipt, today’s cycle count, this reorder pull). It should use a Work Item under `work-items/<id>/` so this work does not mix with the last job.
2. Put a file you already use (stock CSV, count sheet, PO PDF, packing slip) in that Work Item’s `in/` folder, or drop it here and say which receipt, count, or transfer it belongs to.
3. Ask for the work. Example: “Here is this week’s on-hand export and the count CSV. List the variances. Do not invent quantities that are not in the file.”
4. When it finishes, look in **that Work Item’s** `out/` folder.

Starter notes already in `facts/` are typical for a US wholesale stockroom, **not** how *your* shop works until you say so.

## When it is wrong, tell it

- “We call that a bin, not a slot.”
- “Never put WMS passwords in these lists.”
- “Blind counts hide book qty. Do not print expected on that sheet.”

Say **remember this** so it stores the correction. A few real jobs plus a few corrections is enough to get going.

## Do not

- Put passwords, bank logins, or card numbers in this folder.
- Ask it to send money or pay a bill.
- Ask it to invent on-hand, mark a shipment cleared through customs, act as a customs broker, or dump expired stock.

## Back up this folder

Copy the **whole folder** to a safe place on a regular schedule. The notes about how your shop works, plus each Work Item, are the memory.
