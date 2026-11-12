# Quick start — Data visualization from their files

This folder **is** an AI Expert for charts, tables, and write-ups from CSV/Excel exports you drop in. You do not need to be a programmer. Starter facts and rules are **typical for this kind of role**, not how *your* shop works, until you say otherwise.

## 1. Open *this* folder

In the editor use **File → Open Folder** and pick **this** folder (the one with `MyRole.txt` and `AGENTS.md`). One job, one folder.

## 2. Talk in the chat

You can paste:

> I run a [kind of business]. We use [spreadsheets or exports we already use]. Read the files in this folder, then ask what you need so this matches *our* shop. Do not treat the starter notes as our rules until I say so. We must never: [for example never invent a cause, never scrape, never put full SSNs on a chart].

Answer its questions. You do not have to edit files by hand.

## 3. Give it one small real pack

1. Save a CSV or Excel export you already use.
2. Say **which pack this is** — for example “sales by location, week of Nov 3.” It should open a folder under `work-items/<id>/` so this work does not mix with the last pack.
3. Put the file in that folder’s `in/` directory, or drop it here and say which pack it belongs to.
4. Ask for the work. Example: “Here is this week’s export. Bar chart of sales by location. Do not invent numbers that are not in the file.”
5. When it finishes, look in **that Work Item’s** `out/` folder. Work CSVs of plotted values live in `work/`.

Say **continue** to walk one ready step. Continue is not a yes to an open question.

## 4. When it is wrong, tell it

- “We call that location, not store.”
- “Never put full Social Security numbers on these charts.”
- “Week starts Sunday in this export.”

It should save the correction (**remember**) and use it next time.

Then the daily loop is: drop a file into **that pack’s** `in/` (or say the question and date in chat) → ask for the chart → skim `out/` → correct if needed.

Each question + source-file date gets its own folder under `work-items/`. Do not put Tuesday’s files in Monday’s folder.

## 5. Where things live

- Role and must-never: `MyRole.txt`
- How a pack runs: `docs/role/work-item-method.md`
- Agent instructions: `AGENTS.md`
- Shop memory: `facts/facts-operations.md`, `facts/rules-operations.md`
- Jobs: `.cursor/workflows/`
- Tools: `docs/tools/`

## Back up this folder

This folder will fill with notes about how your shop works, plus a folder for each pack. Copy the **whole folder** to a safe place on a regular schedule.

## Do not

- Put passwords, bank logins, API keys, or card numbers in this folder.
- Ask it to send money or pay a bill.
- Ask it to scrape live sites, stand up a BI website, or ship a forecast product.
- Treat a p-value or a correlation as a business decision.

If it offers to do those things, tell it no.
