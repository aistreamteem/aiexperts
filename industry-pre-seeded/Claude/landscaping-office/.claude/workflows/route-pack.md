# Route Pack

**When to use:** Pull the route CSV and match each stop to a ticket. Keep their sequence. Flag skips, missing tickets, missing access, and time windows. Do not invent a better order or a ghost stop. Commercial PO flags stay visible if their file requires a PO. One property per row. They may reorder. You pack the file and write-up for the trucks they already named.

**How to run:** Open or continue a Work Item under `work-items/<id>/`. Follow this file's steps in order. Read the cited tool doc, write artifacts under that Work Item's `work/` and `out/`, run the listed check against those same paths, then **journal-keeper**. Do not invent a missing ticket, price, or weather call — ask with **operator-qa**.

**Initial phase:** `role-job`

## Work map

```yaml
id: route-pack
steps:
  - id: route
    needs: []
    produces: route
    produce_path: work/route.csv
    tool: docs/tools/route-csv.md
    check: python docs/tools/checks/csv-has-columns.py work/route.csv route property
    on_fail: retry
    next: [tickets]
  - id: tickets
    needs: [route]
    produces: tickets
    produce_path: work/route-tickets.csv
    tool: docs/tools/job-ticket-sheet.md
    check: python docs/tools/checks/file-exists.py work/route-tickets.csv
    on_fail: retry
    next: [pack]
  - id: pack
    needs: [route, tickets]
    produces: route-pack
    produce_path: out/route-pack.md
    tool: docs/tools/spreadsheet.md
    check: python docs/tools/checks/file-exists.py out/route-pack.md
    on_fail: retry
    next: []
```

Starter work map. Replace tools and checks when they correct shop practice (**remember** / **integrate-docs**).
