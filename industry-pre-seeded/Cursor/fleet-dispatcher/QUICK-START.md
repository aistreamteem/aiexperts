# Fleet / delivery dispatcher Expert

This folder is a role role Expert for a small delivery or service fleet role.

You do not need to be a programmer. Open **this** folder (the one that contains `MyRole.txt` and `AGENTS.md`). Talk in the chat. The notes already here are a **head start** — typical for this kind of role, not how *your* shop works, until you say otherwise.

1. Read `MyRole.txt` for the role and `docs/role/work-item-method.md` for the day loop.
2. Follow `AGENTS.md` and the always-apply rule `.cursor/rules/expert.mdc`.
3. Say **continue** to resume, or name a job (assignment pack, today’s routes, DVIR gap, exceptions, breakdown, detention, POD check, HOS questions, fuel outliers).
4. Drop the files you already use (roster, route sheet, DVIR/POD folder, ELD/GPS/fuel export) into that Work Item’s `in/` directory, or drop them here and say which service date and unit they belong to.
5. Look in that Work Item’s `out/` for the pack. Facts/rules live under `facts/` (shared + operations memory). Work maps live under `.cursor/workflows/`. Tools live under `docs/tools/`.

## When it is wrong, tell it

- “We call that a unit, not a truck.”
- “Never put full fuel-card numbers in these lists.”
- “POD is required only when the stop flag says so.”

It should save the correction with **remember** and use it next time.

Each service date, unit pack, or named board gets its own folder under `work-items/<id>/`. Do not put Tuesday’s files in Monday’s folder.

## Do not

- Put passwords, bank logins, or card numbers in this folder.
- Ask it to send money or pay a bill.
- Ask it for HOS legal certification, an out-of-service ruling, invented GPS/ETA, or a forged POD.

If it offers to do those things, tell it no.

## Back up this folder

Copy the **whole folder** to a safe place on a regular schedule. The starter download is not a backup of *your* Expert.
