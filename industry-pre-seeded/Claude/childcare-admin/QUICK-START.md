# Childcare center office Expert

This folder is an AI Expert for the **childcare center office** (not the teacher). Open **this** folder in Cursor. You do not need to be a programmer.

The notes already here are a **head start**: typical US center-office facts and rules, labeled as starter until you say how *your* shop files. They are not your handbook until you confirm them.

## 1. Open this folder

Use **File → Open Folder** and pick **this** folder (the one that contains `MyRole.txt` and `CLAUDE.md`). One job, one folder.

## 2. Talk in the chat

You can paste:

> I run a childcare center office. We use [Brightwheel / Procare / spreadsheets]. Read the files in this folder, then ask what you need so this matches *our* shop. Do not treat the starter notes as our rules until I say so. We must never: release a child, diagnose, interpret a court order, invent tuition, or copy extra medical notes into docs/.

Answer its questions. You do not have to edit files by hand.

## 3. Give it one small real job

1. Say which job this is — for example Room A attendance for today, a named child’s enrollment packet, or this month’s tuition list.
2. It should open a folder under `work-items/<id>/` so this work does not mix with the last job.
3. Put your export or PDFs in that folder’s `in/` directory, or drop them here and say which date/room/child they belong to.
4. Ask for the work. Example: “Here is today’s attendance export. Make the usual list. Do not mark anyone present to tidy ratio.”
5. When it finishes, look in **that job’s** `out/` folder.

Registered jobs: attendance day, pickup list check, missing enrollment forms, ratio from their posted chart, tuition from file, waitlist, licensing packet completeness, incident routing, holiday calendar pack. Details: `docs/role/work-item-method.md`.

## 4. When it is wrong, tell it

- “We call that extra-care, not drop-in.”
- “Never put full Social Security numbers in these lists.”
- “The late fee is in our handbook. Do not invent one.”

It should save the correction with **remember** and use it next time.

Then the daily loop is: drop a file into **that job’s** folder (or say the date, room, or child in chat) → ask for the list → skim that folder’s `out` → correct if needed.

Each attendance date, child packet, incident, or billing period gets its own folder under `work-items/`. Do not put Tuesday’s files in Monday’s folder.

## How the Expert works

1. Read `MyRole.txt` for the role.
2. Follow `CLAUDE.md` and `.claude/rules/expert.md`.
3. Use canonical expert skills: continue, workflow-selector, journal-keeper, operator-qa, remember.
4. Shop facts/rules live under `facts/` (shared + operations memory). Work maps live under `.claude/workflows/`; tools live under `docs/tools/`.

## Back up this folder

This folder will fill with notes about how your shop works, plus a folder for each job. Copy the **whole folder** to a safe place on a regular schedule.

## Do not

- Put passwords, bank logins, or card numbers in this folder.
- Ask it to send money or pay a bill.
- Ask it to teach a class, diagnose, release a child, interpret a court order, or stamp the license. Paperwork only.
