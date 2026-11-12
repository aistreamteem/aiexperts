# Mortgage processor (file completeness) — quick start

This folder is a **processor role Expert** (completeness only — not an underwriter). Open **this** folder in Cursor. Talk in the chat.

1. Read `MyRole.txt` for scope and must-nevers. The work-item method is `docs/role/work-item-method.md`.
2. Follow `CLAUDE.md` and `.claude/rules/expert.md`.
3. Shop facts and rules live in `facts/facts-shared.md` and `facts/rules-shared.md`. Jobs live under `.claude/workflows/`. Tools live under `docs/tools/`.
4. Starter notes are **guesses** until you say how *this* shop works. Correct the Expert in chat (“we export PTD as PriorToDocs”). It should save the correction with **remember**.

## Give it one small real job

1. Say which loan this is — for example loan 4412 conditions checklist, or today’s missing-docs chase. It should use one folder under `work-items/<id>/` so this work does not mix with the last loan.
2. Put source files in that folder’s `in/` (LOS export, conditions sheet, PDFs).
3. Ask for the work. Example: “Here is this loan’s conditions export. Build the checklist. Do not invent conditions.”
4. When it finishes, look in that Work Item’s `out/` and `work/`. Open questions should stay labeled. Dates should quote stamps on files you stored.

Typical jobs: conditions checklist, loan-file index, missing docs, date stamps, appraisal-in-file (not a value), title routing, insurance binder present, CD/LE present, suspense as their codes, their wire-fraud checklist rows.

## When it is wrong, tell it

- “We call that PriorToDocs, not PTD.”
- “Never put full Social Security numbers in these lists.”
- “Do not declare CTC. Only copy the LOS flag.”

A few real jobs plus a few corrections is enough to get going.

Daily loop: drop files into **that loan’s** `in/` → ask for the list or checklist → skim `out/` → correct if needed.

Each loan or pack gets its own Work Item. Do not put Tuesday’s files in Monday’s folder.

## Back up this folder

This folder will fill with notes about how your shop works, plus a folder for each loan. Copy the **whole folder** to a safe place on a regular schedule.

## Do not

- Put passwords, bank logins, or card numbers in this folder.
- Ask it to send money, pay a bill, or send a wire.
- Ask it to underwrite, lock a rate, invent DTI/LTV, or give a TRID or fair-lending legal opinion.
- Ask it to copy a credit score or a full SSN into docs.

If it offers to do those things, tell it no.
