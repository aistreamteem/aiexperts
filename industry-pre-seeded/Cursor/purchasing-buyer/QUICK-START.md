# Purchasing / buyer Expert

This folder is a **buyer role Expert** (not AP, not ERP). Open **this** folder in Cursor. Talk in the chat.

1. Read `MyRole.txt` for scope and must-nevers. The work-item method is `docs/role/work-item-method.md`.
2. Follow `AGENTS.md` and `.cursor/rules/expert.mdc`.
3. Shop facts and rules live in `facts/facts-shared.md`, `facts/rules-shared.md`, `facts/facts-operations.md`, and `facts/rules-operations.md`. Jobs live under `.cursor/workflows/`. Tools live under `docs/tools/`. Journals live under `journals/work-items/<id>/` (not under `work-items/<id>/journal/`).
4. Starter notes are **guesses** until you say how *this* shop works. Correct the Expert in chat (“we do not add vendors to the AVL from a one-time buy”). It should save the correction with **remember**.

## Give it one small real job

1. Say which job this is — for example PO 4412 AVL check, this week’s RFQ, or the match for invoice 8891. It should use one folder under `work-items/<id>/` so this work does not mix with the last job.
2. Put source files in that folder’s `in/` (requisition, AVL export, quote PDF, PO sheet, receiving file, invoice PDF).
3. Ask for the work. Example: “Here is this week’s requisition and AVL export. Check vendors. Do not add anyone to the list.”
4. When it finishes, look in that Work Item’s `out/` and `work/`. Shorts and open questions should stay labeled.

Typical jobs: AVL check, RFQ from files, quote/lead/MOQ extract, open-PO list, backorder list, blanket release, change-order pack, receiving shorts, three-way match.

## When it is wrong, tell it

- “We call that a blanket, not a standing PO.”
- “Never invent a unit price. Ask if the quote PDF is missing.”
- “Vendor Acme is approved only as Acme Fasteners LLC on our AVL.”

A few real jobs plus a few corrections is enough to get going.

Daily loop: drop files into **that job’s** `in/` → ask for the list or pack → skim `out/` → correct if needed.

Each PO, RFQ, match, or receiving event gets its own Work Item. Do not put Tuesday’s files in Monday’s folder.

## Back up this folder

This folder will fill with notes about how your shop works, plus a folder for each job. Copy the **whole folder** to a safe place on a regular schedule.

## Do not

- Put passwords, bank logins, or card numbers in this folder.
- Ask it to send money or pay a vendor.
- Ask it to send an unapproved PO as live, add a vendor to the AVL, or give a customs-law opinion.

If it offers to do those things, tell it no.
