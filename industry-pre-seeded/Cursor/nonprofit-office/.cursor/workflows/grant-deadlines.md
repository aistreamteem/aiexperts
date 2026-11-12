# Grant deadlines

**When to use:** From their grants sheet, list upcoming reports, draws, and closeouts, then check the award PDF for the attachments and due dates that sheet must match. Do not invent a due date or borrow another grantee’s calendar. If the sheet and the PDF disagree, quote both and ask. A no-cost extension counts only when a modification is on file. Output is the grants list, the award file in work/, and a pack of what is due and what is missing. They submit. You do not click a portal. You do not say they are on time with the IRS.

**How to run:** Open or continue the Work Item under `work-items/<id>/`. Walk one ready YAML step (or the whole named job if requested): produce the file, run the check, then journal-keeper.

**Initial phase:** `role-job`

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

Starter work map. Replace tools and checks when they correct how this shop works (**remember**).
