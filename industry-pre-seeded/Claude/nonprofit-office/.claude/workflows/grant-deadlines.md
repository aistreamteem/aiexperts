# Grant Deadlines

**When to use:** From their grants sheet, list upcoming reports, draws, and closeouts, then check the award PDF for the attachments and due dates that sheet must match. Do not invent a due date or borrow another grantee’s calendar. If the sheet and the PDF disagree, quote both and ask. A no-cost extension counts only when a modification is on file. Output is the grants list, the award file in work/, and a pack note of what is due and what is missing. They submit. You do not click a portal. You do not say they are on time with the IRS.

**How to run:** Follow this file with **continue**. Paths `work/` and `out/` mean inside `work-items/<id>/`. Load `facts/MEMORY-INDEX.md` then shared facts/rules. If no Work Item exists, use **workflow-selector** for this job and copy `work-items/_TEMPLATE/`. Put operator files in `in/`. For each ready YAML step: read its tool doc; do not start if `needs` files are missing; write `produce_path`; run `check` against this Work Item’s paths (retry at most three times, then ask). Pass produced files to later steps. Missing shop knowledge → **operator-qa** or ask; do not invent. After the last check passes, the pack is `out/` plus `STATUS.md` (sources, artifacts, check results). They circulate, sign, send, submit, or talk to donors — you do not. **journal-keeper** after the step (or after the whole named job if they asked for the whole job).

**Initial phase:** `role-job`

## Steps

1. List grants and due dates from their sheet (docs/tools/spreadsheet.md) → `work/grants.csv`.
2. Check the award PDF (docs/tools/award-letter-pdf.md) → `work/award.pdf`.
3. Pack what is due and what is missing → `out/grants.md`. They submit. You do not click a portal.

## Work map

```yaml
id: grant-deadlines
steps:
  - id: pull
    needs: []
    produces: grants
    produce_path: work/grants.csv
    tool: docs/tools/spreadsheet.md
    check: python docs/tools/checks/csv-has-columns.py work/grants.csv funder due
    on_fail: retry
    next: [pdf]
  - id: pdf
    needs: [grants]
    produces: award
    produce_path: work/award.pdf
    tool: docs/tools/award-letter-pdf.md
    check: python docs/tools/checks/file-exists.py work/award.pdf
    on_fail: retry
    next: [pack]
  - id: pack
    needs: [grants, award]
    produces: grant-pack
    produce_path: out/grants.md
    tool: docs/tools/spreadsheet.md
    check: python docs/tools/checks/file-exists.py out/grants.md
    on_fail: retry
    next: []
```

Starter work map. Replace tools and checks when this shop corrects them.
