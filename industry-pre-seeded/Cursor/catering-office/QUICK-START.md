# Catering office Expert

This folder is an AI Expert for a **catering event office**. Open **this** folder. Talk in the chat.

You do not need to be a programmer. The notes already here are a **head start** for a typical US SMB caterer — not how *your* shop works until you say so.

1. Read `MyRole.txt` for the role and `docs/role/work-item-method.md` for how a job runs.
2. Follow `AGENTS.md` and the always-apply rule `.cursor/rules/expert.mdc`.
3. Say **continue** to resume, or name a job (week board, pack-out, count versus guarantee, dietary list, rentals, staffing, leftover forms, change-after-cutoff).
4. Shop facts/rules live under `facts/` (operations memory). Jobs live under `.cursor/workflows/` (listed in `workflow-registry.json`). Tools live under `docs/tools/`. Each real event or week lives under `work-items/<id>/`. Journals live under `journals/work-items/<id>/`.

## Give it one small real job

1. Save a file you already use (event-order PDF, menu, dietary sheet, rental PO, calendar).
2. Tell the chat **which job this is** — for example Saturday’s Acme lunch or this week’s board. It should keep that work in one Work Item folder so it does not mix with the last job.
3. Put the file in that folder’s `in/` directory, or drop it here and say which event or week it belongs to.
4. Ask for the work. Example: “Here is this week’s orders. Make the week board. Do not invent numbers that are not in the file.”
5. When it finishes, look in **that job’s** `out/` folder.

## When it is wrong, tell it

- “We call that a function sheet, not an event order.”
- “Never put card numbers in these lists.”
- “The leftover form is required on full-service. Do not invent the legal text.”

It should save the correction with **remember** and use it next time.

## Do not

- Put passwords, bank logins, or card numbers in this folder.
- Ask it to send money or pay a vendor.
- Ask it to stamp a health inspection, serve as a liquor license, or invent a price, tax, delivery fee, or food cost.

Back up this whole folder on a regular schedule. The starter notes are not a backup of *your* Expert.
