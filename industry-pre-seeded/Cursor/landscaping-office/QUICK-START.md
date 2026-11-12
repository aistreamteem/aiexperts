# Quick start — Landscaping / lawn-care office

This folder is an AI Expert for a US lawn-care or landscape-maintenance **office**. Open **this** folder (the one with `MyRole.txt` and `AGENTS.md`) in Cursor. Talk in the chat.

You do not need to be a programmer. The notes already here are a **head start** — typical for this kind of role, not how *your* shop works, until you say otherwise.

## 1. What this Expert does

Office packs from files you already keep: crew day lists, route packs, estimates from your price file, material pulls, weather postpone lists after **you** call weather, callback lists, and photo indexes. It copies what your files say. It does not apply chemicals as a license, diagnose trees, pay crews, or store gate codes.

## 2. Give it one small real job

1. Say which job this is (crew day, property + date, ticket, or week). It should open a Work Item under `work-items/` so this pack does not mix with the last one.
2. Put your export, sheet, or PDF in that Work Item’s `in/` folder, or drop it here and say which job it belongs to.
3. Ask for the work. Example: “Here is this week’s route export. Build tomorrow’s crew day. Do not invent hours or a missing ticket.”
4. When it finishes, look in **that Work Item’s** `out/` folder.

Named jobs (pick one, or let it offer the list):

- Crew day, route pack, seasonal calendar
- Estimate from price, enhancement ticket, material pull
- Weather postpone list, callback list, photo pack

Full method: `docs/role/work-item-method.md`. Role limits: `MyRole.txt`.

## 3. When it is wrong, tell it

- “We call that a ticket, not a work order.”
- “Never put gate codes in these lists.”
- “The dump fee is on our price file. Do not invent one.”

It should offer to save the correction and use it next time.

Then the daily loop is: drop a file into **that job’s** `in/` (or name the job in chat) → ask for the list → skim `out/` → correct if needed.

Each crew day, ticket, or week gets its own Work Item. Do not put Tuesday’s files in Monday’s folder.

## 4. Back up this folder

This folder will fill with notes about how your shop works, plus a folder for each pack. Copy the **whole folder** to a safe place on a regular schedule.

## Do not

- Put passwords, bank logins, card numbers, or gate codes in this folder.
- Ask it to send money or pay a crew.
- Ask it to apply a pesticide as a license or diagnose a tree.

If it offers to do those things, tell it no.

“Continue” means take the next ready step. It is not yes to a missing ticket, a missing price, or a weather call they have not made.
