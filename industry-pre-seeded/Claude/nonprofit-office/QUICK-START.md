# Nonprofit office admin — quick start

This folder is a role role Expert for a small nonprofit office (grant files, restricted-fund questions, board packs, donor CSV lists, acknowledgment drafts). You do not need to be a programmer.

The notes already here are a **head start**. Facts and rules are typical for this kind of role, not how *your* shop works, until you say otherwise.

1. Read `MyRole.txt` for the role.
2. Follow `CLAUDE.md` and `.claude/rules/expert.md`.
3. Work-item method: `docs/role/work-item-method.md` (intake → pull shop files → gap check → draft pack → they review/send/submit → file/close).
4. Shop facts/rules live under `facts/` (shared memory). Work maps live under `.claude/workflows/` (listed in `workflow-registry.json`). Tools live under `docs/tools/`. Jobs live under `work-items/<id>/`.

## Talk in the chat

Open the chat / Agent panel. You can paste:

> We are a small nonprofit office. We use [spreadsheets / PDFs / folders we already use]. Read the files in this folder, then ask what you need so this matches *our* shop. Do not treat the starter notes as our rules until I say so. We must never send money, guess a deductibility opinion, or treat restricted cash as unrestricted.

Answer its questions. You do not have to edit files by hand.

## Give it one small real job

1. Save a file you already use (donor CSV, award PDF, board folder, minutes, restricted-fund sheet).
2. Name the job — for example the September board meeting, grant 2026-04, or this week’s gift batch. It should use one folder under `work-items/` so this work does not mix with the last job.
3. Put the file in that folder’s `in/` directory, or drop it here and say which meeting, grant, or batch it belongs to.
4. Ask for the work. Example: “Here is this week’s donor export. Make the usual list. Do not invent numbers that are not in the file.”
5. When it finishes, look in **that job’s** `out/` folder.

Typical jobs: board pack, donor list, gift acknowledgment draft, grant deadlines, grant report, funder gap, in-kind list, minutes index, restricted-fund questions for the bookkeeper.

## When it is wrong, tell it

- “We call that a board packet, not a board book.”
- “Never put full Social Security numbers in these lists.”
- “The fiscal year starts July 1. Do not assume calendar year.”

It should save the correction (**remember**) and use it next time.

Then the daily loop is: drop a file into **that job’s** folder → ask for the list or pack → skim that folder’s `out` → correct if needed.

Each meeting, grant, or gift batch gets its own folder under `work-items/`. Do not put Tuesday’s files in Monday’s folder.

## Back up this folder

This folder will fill with notes about how your shop works, plus a folder for each job. Copy the **whole folder** to a safe place on a regular schedule.

## Do not

- Put passwords, bank logins, or card numbers in this folder.
- Ask it to send money or pay a bill.
- Ask it to be a lawyer or CPA, to certify a Form 990, to appraise an in-kind gift, or to run a donor email/SMS/CRM blast. Paperwork and lists only. They communicate with donors.
