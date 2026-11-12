# Quick start — Restaurant kitchen / BOH admin

This folder is an AI Expert for prep lists, walk-in counts, 86 boards, vendor order guides, receiving notes, invoice matches, catering pulls, allergen quotes, and waste recaps. You do not need to be a programmer.

Notes already here are a **head start** — typical for this kind of role, not how *your* kitchen works until you say so.

## 1. Open this folder

Open **this** folder (the one that contains `AGENTS.md` and `MyRole.txt`). One shop role, one folder.

## 2. Talk in the chat

Paste something like:

> I run a restaurant kitchen. We use [spreadsheets / vendor portal / POS we already use]. Read the files in this folder, then ask what you need so this matches *our* kitchen. Do not treat the starter notes as our rules until I say so. We must never invent an on-hand count, pay a vendor, or guess an allergen.

Answer its questions. You do not have to edit files by hand.

## 3. Give it one small real job

1. Save a file you already use (count sheet, prep list, invoice PDF, 86-board photo, allergen matrix, waste log).
2. Tell the chat **which job this is** — for example Saturday dinner prep, Sysco truck, walk-in count, or this week’s waste. It should open a Work Item under `work-items/<id>/` so this work does not mix with the last job.
3. Put the file in that folder’s `in/` directory, or drop it here and say which service date, vendor, or shift it belongs to.
4. Ask for the work. Example: “Here is tonight’s count sheet. Make the prep list. Do not invent on-hand that is not in the file.”
5. When it finishes, look in **that job’s** `out/` folder.

Typical first jobs: prep list for a named shift, walk-in count, order guide for one vendor.

## 4. When it is wrong, tell it

- “We call that a hotel pan, not a batch.”
- “Never invent a gluten-free claim.”
- “The PM par is on the weekend tab. Do not use the weekday number.”

It should save the correction (`remember`) and use it next time.

Then the daily loop is: drop a file into **that job’s** `in/` → ask for the list → skim that folder’s `out/` → correct if needed.

Each service date, vendor truck, shift, or invoice gets its own Work Item. Do not put Tuesday’s files in Monday’s folder.

## Back up this folder

This folder will fill with notes about how your kitchen works, plus a folder for each job. Copy the **whole folder** to a safe place on a regular schedule.

## Do not

- Put passwords, bank logins, or card numbers in this folder.
- Ask it to send money or pay a vendor.
- Ask it to stamp an inspection, invent a holding time as law, or tell a guest what they can eat.

If it offers to do those things, tell it no.

## Where things live

- Role and jobs: `MyRole.txt`, `docs/role/work-item-method.md`, `AGENTS.md`
- Workflows: `.cursor/workflows/`
- Shop memory: `facts/facts-operations.md`, `facts/rules-operations.md`
- Tools: `docs/tools/`
- Live work: `work-items/<id>/` (`in/`, `work/`, `out/`, `evidence/`)
- Journals: `journals/expert/progress.md` and `journals/work-items/<id>/` (flat journal, `state.json`, `nodes/`)
- Active Work Item: `.cursor/active-context.txt` (`work-item:<id>`)
