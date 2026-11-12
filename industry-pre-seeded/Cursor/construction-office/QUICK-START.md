# Construction office coordinator — quick start

This folder is an AI Expert for a **construction office coordinator** at a small US general contractor or remodeler office. Open **this** folder (the one with `MyRole.txt` and `AGENTS.md`) in Cursor. Talk in the chat.

You do not need to be a programmer. The notes already here are a **head start** — typical for this kind of role, not how *your* shop works, until you say otherwise.

## 1. What this Expert does

Daily and weekly **packs** from files you already keep: daily logs, deliveries, RFIs, submittals, punch, change registers, look-aheads, meeting minutes, subcontractor COIs, and closeout checklists. It copies what your files say. It does not stamp drawings, pay anyone, or give OSHA or contract-law advice.

## 2. Give it one small real job

1. Say which job this is (job number, site + date, or RFI/submittal number). It should open a Work Item under `work-items/` so this pack does not mix with the last one.
2. Put your export, sheet, or PDF in that Work Item’s `in/` folder, or drop it here and say which job it belongs to.
3. Ask for the work. Example: “Here is today’s daily log export for job 12. Fill the usual log. Do not invent manpower.”
4. When it finishes, look in **that Work Item’s** `out/` folder.

Named jobs (pick one, or let it offer the list):

- Daily log, deliveries, look-ahead
- RFI status, submittal aging, change register
- Sub COI, punch list, closeout binder, weekly minutes

Full method: `docs/role/work-item-method.md`. Role limits: `MyRole.txt`.

## 3. When it is wrong, tell it

- “We call that a COR, not a PCO.”
- “Never put full Social Security numbers in these lists.”
- “The COI date is on the PDF. Do not guess.”

It should offer to save the correction and use it next time.

Then the daily loop is: drop a file into **that job’s** `in/` (or name the job in chat) → ask for the list → skim `out/` → correct if needed.

Each job number, date pack, or document pack gets its own Work Item. Do not put Tuesday’s files in Monday’s folder.

## 4. Back up this folder

This folder will fill with notes about how your shop works, plus a folder for each pack. Copy the **whole folder** to a safe place on a regular schedule.

## Do not

- Put passwords, bank logins, or card numbers in this folder.
- Ask it to send money or pay a sub.
- Ask it to stamp drawings, answer as the architect, or give OSHA / lien / prevailing-wage legal opinions.

If it offers to do those things, tell it no.
