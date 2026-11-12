# Waitlist

**When to use:** Copy their waitlist in the order they already wrote. Join grade openings only if they marked openings on the sheet. Do not reorder. Do not promise a seat. Sibling or parish flags stay as coded. Deposits appear only as they recorded them. They offer seats. You pack the list and a write-up. Do not sort by name. Declined offers stay if they keep a declined tab. You do not promise the next seat. They offer. You pack order and openings they marked.

**How to run:** Open or continue a Work Item under `work-items/<id>/`. Put source files in `in/`. Walk one ready YAML step (or the whole named job if requested): produce the file, run the check, then **journal-keeper**.

**Initial phase:** `role-job`

## Work map

```yaml
id: waitlist
steps:
  - id: list
    needs: []
    produces: wait
    produce_path: work/waitlist.csv
    tool: docs/tools/waitlist.md
    check: python docs/tools/checks/csv-has-columns.py work/waitlist.csv student
    on_fail: retry
    next: [pack]
  - id: pack
    needs: [wait]
    produces: wait-pack
    produce_path: out/waitlist.md
    tool: docs/tools/spreadsheet.md
    check: python docs/tools/checks/file-exists.py out/waitlist.md
    on_fail: retry
    next: []
```

Starter work map. Replace tools and checks when they correct this office (use **remember**).
