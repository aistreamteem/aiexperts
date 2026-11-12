# Role Expert — Salon / spa front role

This folder is a role Expert. You do not need to be a programmer.

1. Open **this** folder (the one with `MyRole.txt` and `CLAUDE.md`).
2. Read `MyRole.txt` for the role. The work-item method is `docs/role/work-item-method.md`.
3. Follow `CLAUDE.md` and the always-apply role rule `.claude/rules/expert.md`.
4. Say **continue** or name a job (for example “today’s book”). The expert will open a Work Item under `work-items/<id>/` and walk the registered workflow.
5. Drop shop files (booking export, POS CSV, menu PDF, count sheet) into that Work Item’s `in/` folder.
6. Look for the finished list in that Work Item’s `out/` folder. Correct the expert in chat when a starter note is not how *this* shop works — it should save the correction.

Shop facts/rules live under `facts/` (operations memory). Work maps live under `.claude/workflows/`; tools live under `docs/tools/`.

## Typical jobs

- Today’s or tomorrow’s book (`days-book`)
- Reminder list, waitlist gaps, menu vs book, no-show list
- POS closeout, gift-card recon, retail count, booth split

## Do not

- Put passwords, bank logins, or card numbers in this folder.
- Ask it to send money or pay a bill.
- Ask it to send SMS, email, or CRM blasts (it can make a list; you send).
- Ask it for medical or aesthetic treatment advice, tax opinions, or worker-classification rulings.

Back up the **whole folder** on a regular schedule. Starter notes are guesses until you say how this shop works.
