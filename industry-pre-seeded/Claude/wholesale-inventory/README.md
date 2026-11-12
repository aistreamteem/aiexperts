# Role Expert — Wholesale / inventory role

This folder is a role role Expert. You do not need to be a programmer.

1. Open **this** folder (the one with `MyRole.txt` and `CLAUDE.md`).
2. Read `MyRole.txt` for scope and must-never.
3. Follow `CLAUDE.md` and `.claude/rules/expert.md`.
4. Shop facts/rules live in `facts/facts-shared.md` / `facts/rules-shared.md` and `facts/facts-operations.md` / `facts/rules-operations.md`. Workflows live under `.claude/workflows/`. Tools live under `docs/tools/`. Method: `docs/role/work-item-method.md`.

## Give it one small real job

1. In chat, name the job (this receipt, today’s cycle count, this reorder pull). It should use a Work Item under `work-items/<id>/` so this work does not mix with the last job.
2. Put a file you already use (stock CSV, count sheet, PO PDF) in that Work Item’s `in/` folder.
3. Ask for the work. Example: “Here is the open-PO export and the dock count. Match receiving. Do not invent a PO.”
4. When it finishes, look in **that Work Item’s** `out/` folder.

Starter notes already in `facts/` are typical for a US wholesale stockroom, **not** how *your* shop works until you say so.

## When it is wrong, tell it

Say **remember this** so it stores the correction.

## Do not

- Put passwords, bank logins, or card numbers in this folder.
- Ask it to send money, invent on-hand, or act as a customs broker.

## Back up this folder

Copy the **whole folder** to a safe place on a regular schedule.
