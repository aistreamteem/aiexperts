# Role Expert — Gym / fitness front role

This folder is a role role Expert. You do not need to be a programmer.

1. Open **this** folder (the one with `MyRole.txt` and `CLAUDE.md`).
2. Read `MyRole.txt` for the role. The work-item method is `docs/role/work-item-method.md`.
3. Follow `CLAUDE.md` and the always-apply role rule `.claude/rules/expert.md`.
4. Say **continue** or name a job (for example “today’s check-in list”). The expert will open a Work Item under `work-items/<id>/` and walk the registered workflow.
5. Drop shop files (membership export, scan CSV, waiver PDFs, price/policy sheets) into that Work Item’s `in/` folder.
6. Look for the finished list in that Work Item’s `out/` folder. Correct the expert in chat when a starter note is not how *this* club works — it should save the correction.

Shop facts/rules live under `facts/` (`facts-shared` / `rules-shared`, then `facts-operations` / `rules-operations`). Work maps live under `.claude/workflows/`; tools live under `docs/tools/`.

## Typical jobs

- Today’s check-in list (`check-in-day`)
- Access-flag exceptions, guest-pass log, missing waivers
- Freeze and cancel list, failed-draft list (list only — they contact the member)
- Class roster, PT session counts, retail close

## Do not

- Put passwords, bank logins, or card numbers in this folder.
- Ask it to send money, run EFT, or pay a bill.
- Ask it for medical, diet, or trainer-on-the-floor advice.

Back up the **whole folder** on a regular schedule. Starter notes are guesses until you say how this club works.
