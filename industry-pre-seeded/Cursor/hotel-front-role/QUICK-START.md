# Hotel / inn front role Expert

You do not need to be a programmer. Open **this** folder (the one that contains `MyRole.txt` and `AGENTS.md`) and talk in the chat.

1. Read `MyRole.txt` for the role. Starter notes are typical inn practice, not how *your* property already works, until you say so.
2. Follow `AGENTS.md`, `.cursor/rules/expert.mdc`, and `docs/role/work-item-method.md`.
3. Use **continue** / **workflow-selector** for a named role job (arrivals, due-outs, house count, folio exceptions, and the other registered jobs). Saved knowledge lives in `facts/`. Corrections: tell the Expert; it should **remember**.
4. Shop facts/rules live under `facts/` (operations memory). Workflows live under `.cursor/workflows/` (listed in `workflow-registry.json`). Tools live under `docs/tools/`.
5. Each stay date, reservation, group, or pack is one Work Item under `work-items/<id>/`. Put source files in that item’s `in/` folder. Finished lists land in `out/`.

## One small real job

1. Save a file you already use (arrivals CSV, room-status sheet, folio PDF, night-audit PDF).
2. Tell the chat **which job and which date** — for example “today’s arrivals” or “folio exceptions for 15-Sep”. It should keep that work in one Work Item folder so it does not mix with the last job.
3. Put the file in that folder’s `in/` directory, or drop it here and say which date or reservation it belongs to.
4. Ask for the work. Example: “Here is today’s arrivals export. Make the usual list. Do not invent room numbers that are not in the file.”
5. When it finishes, look in **that Work Item’s** `out/` folder.

When it is wrong, tell it (for example: “Never put full card numbers in these lists.” “The no-show fee is in our policy file.”). A few real jobs plus a few corrections is enough to get going.

## Do not

- Put passwords, bank logins, or card numbers in this folder.
- Ask it to send money, run a card, take a deposit, or post a payment.
- Ask it for an ADA legal opinion or an invented rate or tax.

If it offers to do those things, tell it no.

## Back up this folder

This folder will fill with notes about how your role works, plus a folder for each Work Item. Copy the **whole folder** to a safe place on a regular schedule.
