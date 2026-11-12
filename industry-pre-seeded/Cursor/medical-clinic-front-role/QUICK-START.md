# Role Expert — Medical clinic front role (not the clinician)

You do not need to be a programmer. This folder is an AI Expert for medical clinic front-role paperwork (scheduling files, eligibility as dated screenshots, intake-form completeness, referral paperwork, day lists). It is **not** the clinician.

The notes already here are a **head start**. They are typical for this kind of role, not how *your* shop works, until you say otherwise.

1. Open **this** folder in Cursor (the one that contains `MyRole.txt` and `AGENTS.md`). Do not open a parent folder that contains many Experts.
2. Read `MyRole.txt` for scope and must-nevers. Method: `docs/role/work-item-method.md`. Default job: tomorrow’s **day list**.
3. Drop one real export or PDF, name the job (for example tomorrow’s day list), and ask for the usual list. The Expert should keep that work under `work-items/<id>/` so it does not mix with the last job.
4. Put source files in that Work Item’s `in/` folder. Look for results in `out/`.
5. When it is wrong, tell it in ordinary words. Ask it to **remember** the correction if it should apply next time.
6. Shop facts/rules live under `facts/` (shared memory). Work maps live under `.cursor/workflows/`; tools live under `docs/tools/`. Method: `docs/role/work-item-method.md`.

## Daily loop

Drop a file into **that job’s** folder (or say the clinic day, chart, or pack in chat) → ask for the list → skim `out/` → correct if needed.

Each appointment, clinic day, or pack gets its own Work Item. Do not put Tuesday’s files in Monday’s folder.

## Back up this folder

Copy the **whole folder** to a safe place on a regular schedule. If you only keep it on one computer and that copy is lost, those notes are gone.

## Do not

- Put passwords, bank logins, or card numbers in this folder.
- Ask it to send money or pay a bill.
- Ask it to diagnose, treat, choose CPT as care, interpret labs, or promise coverage.
