# Bookkeeping / bills — quick start

This folder is a **bookkeeper role Expert** (not a CPA). Open **this** folder in Cursor. Talk in the chat.

1. Read `MyRole.txt` for scope and must-nevers. The work-item method is `docs/role/work-item-method.md`.
2. Follow `AGENTS.md` and `.cursor/rules/expert.mdc`.
3. Shop facts and rules live in `facts/facts-shared.md` / `facts/rules-shared.md` and `facts/facts-operations.md` / `facts/rules-operations.md`. Jobs live under `.cursor/workflows/`. Tools live under `docs/tools/`.
4. Starter notes are **guesses** until you say how *this* shop works. Correct the Expert in chat (“we expense supplies, we do not keep inventory”). It should save the correction with **remember**.

## Give it one small real job

1. Say which job this is — for example August operating bank rec, September cards, or October month-end. It should use one folder under `work-items/<id>/` so this work does not mix with the last job.
2. Put source files in that folder’s `in/` (bank CSV, statement PDF, bills, receipts).
3. Ask for the work. Example: “Here is this month’s operating CSV. Review unclear lines. Do not invent payees.”
4. When it finishes, look in that Work Item’s `out/` and `work/`. Open questions should stay labeled.

Typical jobs: month-end close pack, bank review, bank rec, credit-card coding, vendor bills, receipt match, AR aging questions, sales-tax questions, contractor 1099 list, light job cost.

## When it is wrong, tell it

- “We call that a draw, not COGS.”
- “Never put full account numbers in these lists — last four only.”
- “Rent is account 6100. Do not guess a new name.”

A few real jobs plus a few corrections is enough to get going.

Daily loop: drop files into **that job’s** `in/` → ask for the list or rec → skim `out/` → correct if needed.

Each period, account rec, or pack gets its own Work Item. Do not put September’s files in August’s folder.

## Back up this folder

This folder will fill with notes about how your shop works, plus a folder for each job. Copy the **whole folder** to a safe place on a regular schedule.

## Do not

- Put passwords, bank logins, or card numbers in this folder.
- Ask it to send money or pay a bill.
- Ask it to file a return, 1099, or sales-tax return, or to give a tax opinion.

If it offers to do those things, tell it no.
