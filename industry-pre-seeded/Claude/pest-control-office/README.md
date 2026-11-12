# Pest control office Expert

This folder is an AI Expert for a **US structural pest-control office**. Open **this** folder. Talk in the chat.

You do not need to be a programmer. The notes already here are a **head start** for a typical pest office — not how *your* shop works until you say so.

1. Read `MyRole.txt` for the role and `docs/role/work-item-method.md` for how a job runs.
2. Follow `CLAUDE.md` and the always-apply rule `.claude/rules/expert.md`.
3. Say **continue** to resume, or name a job (route day, skip list, callback list, chemical-log pack, inventory vs log, bait-map index, device count, estimate from price file, WDO form completeness).
4. Shop facts/rules live under `facts/` (operations memory). Jobs live under `.claude/workflows/` (listed in `workflow-registry.json`). Tools live under `docs/tools/`. Each real route day, ticket pack, or named pack lives under `work-items/<id>/`.

## Give it one small real job

1. Save a file you already use (route CSV, ticket sheet, chemical log, bait-map PDF, price file, WDO form).
2. Tell the chat **which job this is** — for example Tuesday’s route, ticket 118, or this week’s callback board. It should keep that work in one Work Item folder so it does not mix with the last job.
3. Put the file in that folder’s `in/` directory, or drop it here and say which route day or ticket it belongs to.
4. Ask for the work. Example: “Here is this week’s route export. Make the day list. Do not invent a ticket or a mix that is not in the file.”
5. When it finishes, look in **that job’s** `out/` folder.

## When it is wrong, tell it

- “We call that a service ticket, not a work order.”
- “Never put gate codes in these lists.”
- “The EPA number is on our label file. Do not invent one.”

It should save the correction with **remember** and use it next time.

## Do not

- Put passwords, bank logins, card numbers, or gate codes in this folder.
- Ask it to send money or pay a tech or chemical vendor.
- Ask it to apply pesticide, invent a mix or EPA number, diagnose a structure, or give wildlife legal advice.

Back up this whole folder on a regular schedule. The starter notes are not a backup of *your* Expert.
