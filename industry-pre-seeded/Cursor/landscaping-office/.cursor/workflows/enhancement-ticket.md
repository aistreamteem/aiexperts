# Enhancement Ticket

**When to use:** Assemble one-time work from the enhancement ticket, price file, and sold proposal if present. Extra finds still need auth. Commercial PO missing when required stays a hold. Do not mix this onto the weekly mow row. Materials and hours come from their files only. Warranty language is copied, not a survival promise. They schedule the enhancement crew. You draft the pack and write-up.

**How to run:** Open or continue a Work Item under `work-items/<id>/`. Follow this file's steps in order. Read the cited tool doc, write artifacts under that Work Item's `work/` and `out/`, run the listed check against those same paths, then **journal-keeper**. Do not invent a missing ticket, price, or weather call — ask with **operator-qa**.

**Initial phase:** `role-job`

## Work map

```yaml
id: enhancement-ticket
steps:
  - id: tickets
    needs: []
    produces: tickets
    produce_path: work/enhancement-tickets.csv
    tool: docs/tools/job-ticket-sheet.md
    check: python docs/tools/checks/csv-has-columns.py work/enhancement-tickets.csv ticket property service
    on_fail: retry
    next: [price]
  - id: price
    needs: [tickets]
    produces: price
    produce_path: work/price-file.csv
    tool: docs/tools/price-file.md
    check: python docs/tools/checks/file-exists.py work/price-file.csv
    on_fail: retry
    next: [pack]
  - id: pack
    needs: [tickets, price]
    produces: enh-pack
    produce_path: out/enhancement.md
    tool: docs/tools/spreadsheet.md
    check: python docs/tools/checks/file-exists.py out/enhancement.md
    on_fail: retry
    next: []
```

Starter work map. Replace tools and checks when they correct shop practice (**remember** / **integrate-docs**).

