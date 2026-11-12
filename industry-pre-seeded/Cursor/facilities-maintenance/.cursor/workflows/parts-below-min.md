# Parts below minimum

**When to use:** Compare crib on-hand to the min-qty they stored. List SKUs at or below min. Do not invent a min or a count. Do not place a PO. Do not hide a hole so the crib looks healthy. Kit and spare flags stay as they coded them. Write-up is a below-min pack plus which open work orders wait on those SKUs if the work-order file is in the folder.

**How to run:** Open or continue a Work Item under `work-items/<id>/`. Put source files in `in/`. Walk one ready YAML step (or the whole named job if requested): produce the file, run the check, then **journal-keeper**. Paths `in/`, `work/`, `out/`, and `evidence/` are inside that Work Item.

**Initial phase:** `role-job`

## Work map

```yaml
id: parts-below-min
steps:
  - id: crib
    needs: []
    produces: crib
    produce_path: work/parts-crib.csv
    tool: docs/tools/parts-crib-csv.md
    check: python docs/tools/checks/csv-has-columns.py work/parts-crib.csv sku on-hand min-qty
    on_fail: retry
    next: [pack]
  - id: pack
    needs: [crib]
    produces: below-min
    produce_path: out/parts-below-min.md
    tool: docs/tools/spreadsheet.md
    check: python docs/tools/checks/file-exists.py out/parts-below-min.md
    on_fail: retry
    next: []
```

Starter work map. Replace tools and checks when the operator corrects this plant through **remember**.
