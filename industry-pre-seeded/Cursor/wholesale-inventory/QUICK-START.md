# Role Expert — Wholesale / inventory role

This folder is a **wholesale / inventory role Expert**. You do not need to be a programmer. Open **this** folder in Cursor. Talk in the chat.

1. Read `MyRole.txt` for scope and must-nevers. The work-item method is `docs/role/work-item-method.md`.
2. Follow `AGENTS.md` and `.cursor/rules/expert.mdc`.
3. Shop facts and rules live in `facts/facts-shared.md`, `facts/rules-shared.md`, `facts/facts-operations.md`, and `facts/rules-operations.md`. Jobs live under `.cursor/workflows/`. Tools live under `docs/tools/`. Journals live under `journals/work-items/<id>/`.
4. Starter notes are **guesses** until you say how *this* shop works. Correct the Expert in chat. It should save the correction with **remember**.

## Give it one small real job

1. In chat, name the job (this receipt, today’s cycle count, this reorder pull). It should use a Work Item under `work-items/<id>/` so this work does not mix with the last job.
2. Put a file you already use (stock CSV, count sheet, PO PDF, packing slip) in that Work Item’s `in/` folder, or drop it here and say which receipt, count, or transfer it belongs to.
3. Ask for the work. Example: “Here is this week’s on-hand export and the count CSV. List the variances. Do not invent quantities that are not in the file.”
4. When it finishes, look in **that Work Item’s** `out/` folder.

Typical jobs: receiving match, putaway, pick/pack, transfer, cycle count, ABC class, dead stock, lot expiry, reorder, RMA returns.

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
