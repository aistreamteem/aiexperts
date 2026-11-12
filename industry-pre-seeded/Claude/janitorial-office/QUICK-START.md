# Janitorial / contract-cleaning office Expert

This folder is an AI Expert for a US contract-cleaning or building-service **office role**. It helps with night boards, supply pars, quality checklist packs, complaint callbacks, extra-work auth lists, holiday coverage, key-log completeness, missed-service lists, and SDS-index gaps.

The notes already here are a **head start** — typical for this kind of role, not how *your* shop works, until you say otherwise.

1. Open **this** folder (the one with `MyRole.txt` and `CLAUDE.md`).
2. Read `MyRole.txt` for the role. Follow `CLAUDE.md` and `.claude/rules/expert.md`.
3. Method: `docs/role/work-item-method.md`. Shop facts/rules live under `facts/` (operations memory). Workflows live under `.claude/workflows/`. Tools live under `docs/tools/`.
4. Say **continue** or name a job (for example “tonight’s night board”). Each real site-night, ticket, or pack gets its own folder under `work-items/<id>/` so jobs do not mix.
5. Drop source files into that Work Item’s `in/` folder (site list, schedule CSV, par sheet, SDS index, quality form, complaint log, key log, contract PDFs). Ask for the list. Do not expect invented hours, mixes, scores, or missing sites.
6. Look in that Work Item’s `out/` folder when it finishes. If it is wrong, tell it in plain language (“we call that a callback, not a complaint”). It should **remember** the correction.

## Daily loop

Drop a file into **that job’s** folder → ask for the matching role job → skim `out/` → correct if needed.

## Do not

- Put passwords, bank logins, card numbers, alarm codes, or keypad PINs in this folder.
- Ask it to send money, pay a crew, stamp OSHA, or invent a chemical mix.

Back up this whole folder on a regular schedule. The starter download is not a backup of *your* Expert.
