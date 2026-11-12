# Quick start — Bakery / cafe production office

This folder is an AI Expert for bake lists, case pars, wholesale packs, cake boards, receiving shorts, allergen indexes, and waste recaps. You do not need to be a programmer.

Notes already here are a **head start** — typical for this kind of role, not how *your* shop works until you say so.

## 1. Open this folder

Open **this** folder (the one that contains `CLAUDE.md` and `MyRole.txt`). One shop role, one folder.

## 2. Talk in the chat

Paste something like:

> I run a bakery-cafe. We use [spreadsheets / bakery software we already use]. Read the files in this folder, then ask what you need so this matches *our* shop. Do not treat the starter notes as our rules until I say so. We must never invent a formula, pay a vendor, or guess an allergen.

Answer its questions. You do not have to edit files by hand.

## 3. Give it one small real job

1. Save a file you already use (bake-list sheet, standing CSV, invoice PDF, cake-order form, allergen matrix).
2. Tell the chat **which job this is** — for example Tuesday bake list, wholesale Thursday, cake board for 2026-11-14, or this morning’s receiving. It should open a Work Item under `work-items/<id>/` so this work does not mix with the last job.
3. Put the file in that folder’s `in/` directory, or drop it here and say which bake date, account day, or order it belongs to.
4. Ask for the work. Example: “Here is today’s bake sheet. Make the bake list. Do not invent mix counts that are not in the file.”
5. When it finishes, look in **that job’s** `out/` folder.

Typical first jobs: bake list for a named day, case par vs count, wholesale pick list.

## 4. When it is wrong, tell it

- “We call that a mix, not a batch.”
- “Never invent a gluten-free claim.”
- “The croissant par is on the weekend tab. Do not use the weekday number.”

It should save the correction (`remember`) and use it next time.

Then the daily loop is: drop a file into **that job’s** `in/` → ask for the list → skim that folder’s `out/` → correct if needed.

Each bake date, wholesale day, cake board, or receiving ticket gets its own Work Item. Do not put Tuesday’s files in Monday’s folder.

## Back up this folder

This folder will fill with notes about how your shop works, plus a folder for each job. Copy the **whole folder** to a safe place on a regular schedule.

## Do not

- Put passwords, bank logins, or card numbers in this folder.
- Ask it to send money or pay a mill or dairy vendor.
- Ask it to stamp an inspection, invent an FDA label, or tell a guest what they can eat.

If it offers to do those things, tell it no.

## Where things live

- Role and jobs: `MyRole.txt`, `docs/role/work-item-method.md`, `CLAUDE.md`
- Workflows: `.claude/workflows/`
- Shop memory: `facts/facts-shared.md` / `facts/rules-shared.md`, plus `facts/facts-operations.md` / `facts/rules-operations.md`
- Tools: `docs/tools/`
- Live work: `work-items/<id>/`
- Journals: `journals/expert/progress.md` and `journals/work-items/<id>/`
