# RMA / Returns Pack

**When to use:** List open RMAs from their sheet: number, sku, qty, reason, and restock path as written. Do not invent an RMA. Attach damage-photo filenames if they stored them. Restock qty stays their inspect columns, not hope. You do not pay return postage and you do not apply a customer credit. They approve returns and they receive if that is their split. You do not invent a restock quantity.

**How to run:** Open or switch to a Work Item under `work-items/<id>/`. Put source files in that item’s `in/`. Follow the YAML steps below — one ready step per **continue**, or the whole named job if requested. Read the named `docs/tools/` doc. Produce files under this Work Item. Run each step’s check. Then **journal-keeper**.

**Initial phase:** `role-job`

## Work map

```yaml
id: rma-returns
steps:
  - id: rma
    needs: []
    produces: rma
    produce_path: work/rma.csv
    tool: docs/tools/rma-sheet.md
    check: python docs/tools/checks/csv-has-columns.py work/rma.csv sku qty
    on_fail: retry
    next: [pack]
  - id: pack
    needs: [rma]
    produces: rma-pack
    produce_path: out/rma-returns.md
    tool: docs/tools/spreadsheet.md
    check: python docs/tools/checks/file-exists.py out/rma-returns.md
    on_fail: retry
    next: []
```

Starter work map. Replace tools and checks when they **remember** a shop correction.
