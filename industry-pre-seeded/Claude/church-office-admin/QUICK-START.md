# Role Expert — Church / house-of-worship office

This folder is a role role Expert. You do not need to be a programmer.

1. Open **this** folder (the one with `MyRole.txt` and `CLAUDE.md`).
2. Read `MyRole.txt` for scope and must-never.
3. Follow `CLAUDE.md` and `.claude/rules/expert.md`.
4. Shop facts/rules live under `facts/` (shared memory). Workflows live under `.claude/workflows/`. Tools live under `docs/tools/`. Method: `docs/role/work-item-method.md`.

## Give it one small real job

1. In chat, name the job (this Sunday’s batch, this week’s rooms, this volunteer roster, this board meeting). It should use a Work Item under `work-items/<id>/` so this work does not mix with the last job.
2. Put a file you already use (giving export, count sheet, calendar, roster, PDF) in that Work Item’s `in/` folder, or drop it here and say which Sunday, batch, or meeting it belongs to.
3. Ask for the work. Example: “Here is this week’s giving export and the signed count sheet. Make the batch completeness list. Do not invent gifts or fund codes that are not in the file.”
4. When it finishes, look in **that Work Item’s** `out/` folder.

Starter notes already in `facts/` are typical for a US church office, **not** how *your* shop works until you say so.

## When it is wrong, tell it

- “We call that a batch, not a deposit.”
- “Never put full account numbers in these lists.”
- “The statement process is in our process file. Do not invent one.”

Say **remember this** so it stores the correction. A few real jobs plus a few corrections is enough to get going.

## Do not

- Put passwords, bank logins, or card numbers in this folder.
- Ask it to send money or pay a bill.
- Ask it to give a tax opinion, pastoral counseling, a safeguarding legal opinion, or a background-clearance verdict.

## Back up this folder

Copy the **whole folder** to a safe place on a regular schedule. The notes about how your shop works, plus each Work Item, are the memory.
