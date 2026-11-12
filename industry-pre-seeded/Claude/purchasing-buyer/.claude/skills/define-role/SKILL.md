---
name: define-role
description: >-
  First session: ask what this Expert is for, write MyRole.txt and stub
  workflows. Use when MyRole.txt Role status is pending or they name a new job.
---

# Define role

## When

`MyRole.txt` **Role status** is `pending`. They name a job. New Expert folder.

## Ask (do not skip)

1. What should we **call** this Expert (their words)?
2. What **jobs** do you repeat (names + rough steps)? Typical buyer jobs: AVL check, RFQ, quote/lead/MOQ, open POs, backorder, blanket release, change order, receiving shorts, match.
3. What **tools** do you already use (spreadsheets, quote PDFs, receiving sheets, AVL export)? Notes only — no passwords.
4. What does **done** look like — what would a **command** see (a CSV with po, sku, and qty; a match pack in `out/`)?
5. What must we **never** do?
6. What is **not our job** (AP/payment, ERP implementation, customs law)?

## Write

- Fill `MyRole.txt` and set Role status to defined after they approve (`I approve the role`).
- Create `.claude/workflows/<name>.md` stubs: when to use, how to run (continue + this file + journal-keeper), and a work-map YAML (`needs`, `produces`, `tool`, `check`). See `.claude/workflows/README.md`. Register each job in `workflow-registry.json`.
- For each tool they named, a stub in `docs/tools/` until they confirm details.
- **journal-keeper**.

Do not pretend the files are complete. Thin is correct. Learning starts on the first real pack. Align new jobs with `docs/role/work-item-method.md` (requisition/AVL → RFQ/quote → PO draft → open-order → receiving → match) unless they described a different shop loop.
