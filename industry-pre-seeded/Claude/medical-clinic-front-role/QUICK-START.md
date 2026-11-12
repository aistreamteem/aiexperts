# Role Expert — Medical clinic front role

This folder is a role role Expert for **Medical clinic front role (not the clinician)**. You do not need to be a programmer.

1. Open **this** folder (the one with `MyRole.txt` and `CLAUDE.md`).
2. Read `MyRole.txt` for scope. Starter notes are typical US front-role practice until you confirm how *this* clinic files.
3. Follow `CLAUDE.md` and `.claude/rules/expert.md`. Method: `docs/role/work-item-method.md`.
4. Shop facts/rules live under `facts/` (operations memory). Jobs live under `.claude/workflows/`; tools live under `docs/tools/`.

## Give it one small real job

1. Say which job this is — for example the 10 a.m. appointment, chart 2201, or Tuesday’s day list. It should use a folder under `work-items/<id>/` so this work does not mix with the last job.
2. Put the source file in that folder’s `in/` directory (schedule export, eligibility screenshot, intake PDFs, close report).
3. Ask for the work. Example: “Here is today’s schedule export. Make the day list. Do not invent columns that are not in the file.”
4. When it finishes, look in **that Work Item’s** `out/` folder.

Say **continue** to walk the next ready step. Continue is not a yes to an open question.

When it is wrong, tell it (for example: “Never put full Social Security numbers in these lists.”). It should offer to **remember** the correction.

## Do not

- Put passwords, bank logins, or card numbers in this folder.
- Ask it to send money or pay a bill.
- Ask it to diagnose, treat, pick CPT as care, or promise coverage.

Back up the **whole folder** on a regular schedule. This folder is the memory.
