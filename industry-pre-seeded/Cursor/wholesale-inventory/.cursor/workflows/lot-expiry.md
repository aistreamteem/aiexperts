# Lot and expiry watch

**When to use:** Only if their file has lot or expiry columns. Do not invent lots or dates. Flag blanks on lot-controlled SKUs and mixed lots in one bin. FEFO or FIFO only when they said which. Expired or near-expired: flag; do not dump product or declare a recall. Keep location and quantity in their UOM. FDA pages are orientation, not a compliance stamp. If they do not use lots, say the folder had no lot file and stop.

**How to run:** Open or switch to a Work Item under `work-items/<id>/`. Follow this YAML one ready step (or the whole named job if requested). Then **journal-keeper**.

**Initial phase:** `role-job`

## Work map

```yaml
id: lot-expiry
steps:
  - id: pull
    needs: []
    produces: lots
    produce_path: work/lots.csv
    tool: docs/tools/lot-sheet.md
    check: python docs/tools/checks/csv-has-columns.py work/lots.csv sku lot
    on_fail: retry
    next: [pack]
  - id: pack
    needs: [lots]
    produces: lot-pack
    produce_path: out/lots.md
    tool: docs/tools/lot-sheet.md
    check: python docs/tools/checks/file-exists.py out/lots.md
    on_fail: retry
    next: []
```

Starter work map. Replace tools and checks when the operator corrects this shop (**remember**).
