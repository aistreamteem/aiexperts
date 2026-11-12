# Job coordinator in a trade shop — quick start

This folder is an AI Expert for a **job coordinator in a trade shop** (HVAC, plumbing, electrical, similar). Open **this** folder (the one with `MyRole.txt` and `CLAUDE.md`) in Claude Code. Talk in the chat.

You do not need to be a programmer. The notes already here are a **head start** — typical for this kind of role, not how *your* shop works, until you say otherwise.

## 1. What this Expert does

Dispatch boards, sold-job packs, packing lists, permit-number rows, closeout photo checklists, and callback flags from the schedule sheets, PDFs, and logs you already keep. It copies what your files say. It does not hold a trade license, pass an inspection, send money, or store gate or alarm codes.

## 2. Give it one small real job

1. Say which job this is (ticket, sold estimate, crew day, permit pack, or callback). It should open a Work Item under `work-items/` so this pack does not mix with the last one.
2. Put your schedule export, sold PDF, packing-list CSV, permit log, or photo folder in that Work Item’s `in/` folder, or drop it here and say which ticket it belongs to.
3. Ask for the work. Example: “Here is today’s schedule export. Make the daily board. Do not invent ETAs that are not in the file.”
4. When it finishes, look in **that Work Item’s** `out/` folder.

Named jobs (pick one, or let it offer the list):

- Callback triage, closeout photos, daily board, emergency queue
- Parts ready, permit file, quote to job
- Truck load, warranty parts, week schedule

Full method: `docs/role/work-item-method.md`. Role limits: `MyRole.txt`. Shared memory: `facts/facts-shared.md` and `facts/rules-shared.md`.

## 3. When it is wrong, tell it

- “We call that a ticket, not a work order.”
- “Never put gate codes in these lists.”
- “The permit number is in our permit log. Do not invent one.”

Say **remember this** so it stores the correction. A few real jobs plus a few corrections is enough to get going.

Then the daily loop is: drop a file into **that job’s** `in/` (or name the job in chat) → ask for the list → skim `out/` → correct if needed.

Each ticket, sold estimate, crew day, or callback gets its own Work Item. Do not put Tuesday’s files in Monday’s folder.

## 4. Back up this folder

This folder will fill with notes about how your shop works, plus a folder for each pack. Copy the **whole folder** to a safe place on a regular schedule.

## Do not

- Put passwords, bank logins, or card numbers in this folder.
- Ask it to send money or pay a bill.
- Ask it to claim a license, pass an inspection, diagnose over the phone, or store lockbox/alarm codes.

If it offers to do those things, tell it no.
