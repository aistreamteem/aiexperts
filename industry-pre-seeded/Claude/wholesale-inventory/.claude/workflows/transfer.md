# Site transfer list

**When to use:** From site, to site, SKU, quantity, and UOM from their transfer file, plus their transfer number. Do not mix the move into a single-site count. In-transit between buildings is not on-hand at either end until they said it landed. Do not invent a transfer number or move more than available at the from site. Lot and serial if required. Owner codes travel with the line. You do not run the truck. One list per their export.

**How to run:** Open or switch to a Work Item under `work-items/<id>/`. Follow this YAML one ready step (or the whole named job if requested). Then **journal-keeper**.

**Initial phase:** `role-job`

## Work map

```yaml
id: transfer
steps:
  - id: list
    needs: []
    produces: xfers
    produce_path: work/transfers.csv
    tool: docs/tools/spreadsheet.md
    check: python docs/tools/checks/csv-has-columns.py work/transfers.csv from_site to_site sku
    on_fail: retry
    next: [pack]
  - id: pack
    needs: [xfers]
    produces: xfer-pack
    produce_path: out/transfers.md
    tool: docs/tools/spreadsheet.md
    check: python docs/tools/checks/file-exists.py out/transfers.md
    on_fail: retry
    next: []
```

Starter work map. Replace tools and checks when the operator corrects this shop (**remember**).
