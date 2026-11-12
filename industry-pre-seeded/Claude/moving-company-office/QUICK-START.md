# Moving company office Expert

This folder is an AI Expert for a US household-goods or local moving office. Open **this** folder (the one with `CLAUDE.md` and `MyRole.txt`) and talk in chat.

The notes already here are a **head start**. Facts and rules are typical for this kind of role, not how *your* shop works, until you say otherwise.

## Start a job

1. Read `MyRole.txt` for scope (no invented weight/cube, no tariff/DOT legal, no crew pay, no card PAN).
2. Follow `CLAUDE.md` and `.claude/rules/expert.md`.
3. Say which job this is — for example estimate 9021, Saturday’s loads, or claim 441. The Expert keeps it under `work-items/<id>/` so it does not mix with the last move.
4. Drop the files you already use into that job’s `in/` (rate sheet, inventory, calendar, scale tickets, claim photos).
5. Ask for the work. Example: “Here is this week’s inventory and rate file. Draft the estimate. Do not invent pounds or extras that are not in the file.”
6. Look in that job’s `out/` for the pack.

Registered jobs: estimate from rate file, inventory completeness, high-value list check, materials list, crew day, truck calendar, delivery windows, weigh-ticket pack, claims routing. See `docs/role/work-item-method.md`.

Shop facts/rules live under `facts/` (operations memory). Workflows live under `.claude/workflows/`. Tools live under `docs/tools/`.

## When it is wrong, tell it

- “We call that a first, not a guaranteed.”
- “Never put card numbers in these lists.”
- “Stairs extras are only on the extras sheet. Do not invent a flight count.”

It should save the correction (**remember**) and use it next time.

## Do not

- Put passwords, bank logins, or card numbers in this folder.
- Ask it to send money, pay a crew, or pay a bill.
- Ask it to be a tariff lawyer, DOT certifier, or a scale.

## Back up this folder

Copy the **whole folder** somewhere safe on a regular schedule. The starter download is not a backup of *your* Expert.
