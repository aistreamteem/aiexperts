# Role Expert — Veterinary front role (not the vet)

This folder is a role Expert for **Veterinary front role (not the vet)**. You do not need to be a programmer.

1. Open **this** folder (the one with `MyRole.txt` and `CLAUDE.md`).
2. Read `MyRole.txt` for scope and must-never. Starter notes are typical US veterinary-front-role practice until you confirm how *this* clinic files.
3. Follow `CLAUDE.md` and `.claude/rules/expert.md`. Method: `docs/role/work-item-method.md`.
4. Shop facts/rules live under `facts/` (shared, then operations memory). Jobs live under `.claude/workflows/`; tools live under `docs/tools/`.

## Give it one small real job

1. Say which job this is — for example today’s book, this records request, this estimate, or this boarding drop-off. It should use a folder under `work-items/<id>/` so this work does not mix with the last job.
2. Put the source file in that folder’s `in/` directory (PIMS export, PDF, spreadsheet).
3. Ask for the work. Example: “Here is today’s appointment export. Make the day list. Flag emergency wording at the top. Do not invent reasons that are not in the file.”
4. When it finishes, look in **that Work Item’s** `out/` folder.

Say **continue** to walk the next ready step. Continue is not a yes to an open question.

When it is wrong, tell it (for example: “Never put card numbers in these lists.”). It should offer to **remember** the correction.

## Do not

- Put passwords, bank logins, or card numbers in this folder.
- Ask it to send money or pay a bill.
- Ask it to diagnose, recommend treatment or drugs, read a lab, or triage as a veterinarian.

Back up the **whole folder** on a regular schedule. This folder is the memory.
