# Role Expert — Equipment rental role

This folder is an AI Expert for the **equipment rental role**. You do not need to be a programmer.

1. Open **this** folder (the one with `MyRole.txt` and `AGENTS.md`).
2. Read `MyRole.txt` for scope. Follow `AGENTS.md` and `.cursor/rules/expert.mdc`.
3. The Work Item method is `docs/role/work-item-method.md`.
4. Shop facts/rules live under `facts/` (`facts/facts-operations.md`, `facts/rules-operations.md`). Jobs live under `.cursor/workflows/`. Tools live under `docs/tools/`.
5. Notes already here are a **head start** — typical for this kind of role, not how *your* yard works until you say so.

## Talk in the chat

You can paste:

> I run an equipment rental yard. We use [software or spreadsheets we already use]. Read the files in this folder, then ask what you need so this matches *our* shop. Do not treat the starter notes as our rules until I say so. We must never: invent a rate, diagnose a repair, store card numbers, or send money.

## Give it one small real job

1. Save a file you already use (fleet export, rate file, contract PDF, inspection sheet, or photos).
2. Say **which job this is** — for example contract 331, today’s reservations, or this week’s returns. It should open a Work Item under `work-items/<id>/` so this work does not mix with the last job.
3. Put the file in that Work Item’s `in/` directory, or drop it here and say which contract, day, or pack it belongs to.
4. Ask for the work. Example: “Here is today’s reservation export. Make the usual list. Do not invent units that are not in the file.”
5. When it finishes, look in **that Work Item’s** `out/` folder.

Say **continue** to pick up the next ready step. That word is not approval and not an answer to a question.

## When it is wrong, tell it

- “We call that a contract, not a ticket.”
- “Never put card numbers in these lists.”
- “The day rate is in our rate file. Do not invent one.”

Ask it to **remember** the correction so the next job is closer.

## Do not

- Put passwords, bank logins, or card numbers in this folder.
- Ask it to send money or pay a vendor.
- Ask it to diagnose a machine, stamp an operator license, engineer indoor height, or collect a debt as a lawsuit.

## Back up this folder

This folder will fill with notes about how your shop works, plus a folder for each job. Copy the **whole folder** to a safe place on a regular schedule.
