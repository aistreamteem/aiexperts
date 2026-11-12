# Work-order dispatch list

**When to use:** Build today's or this week's dispatch list from their work-order CSV: wo, asset, location, priority, craft, status. Flag missing assets and emergency rows. Do not invent a diagnosis or a craft reassignment. Do not treat requested drafts as assigned. This is an in-house board, not a field-trade customer dispatch and not a construction daily log. The pack names which columns came from the export versus a guess you labeled.

**How to run:** Open or continue a Work Item under `work-items/<id>/`. Put source files in `in/`. Walk one ready YAML step (or the whole named job if requested): produce the file, run the check, then **journal-keeper**. Paths `in/`, `work/`, `out/`, and `evidence/` are inside that Work Item.

**Initial phase:** `role-job`

## Work map

```yaml
id: dispatch-list
steps:
  - id: tickets
    needs: []
    produces: tickets
    produce_path: work/wo.csv
    tool: docs/tools/wo-csv.md
    check: python docs/tools/checks/csv-has-columns.py work/wo.csv wo asset priority
    on_fail: retry
    next: [board]
  - id: board
    needs: [tickets]
    produces: dispatch-list
    produce_path: out/dispatch-list.md
    tool: docs/tools/spreadsheet.md
    check: python docs/tools/checks/file-exists.py out/dispatch-list.md
    on_fail: retry
    next: []
```

Starter work map. Replace tools and checks when the operator corrects this plant through **remember**.
