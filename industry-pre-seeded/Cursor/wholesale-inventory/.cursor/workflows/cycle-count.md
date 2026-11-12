# Cycle count pack

**When to use:** From a count CSV, list variances versus the on-hand file if they provided both. No guessed quantity. No silent adjust. Keep SKU, UOM, book, counted, delta, location, counter, and date when those columns exist. Honor blind sheets and their recount threshold. One site unless they asked. Quote filenames and cutoff. Lost tags and unknown barcodes stay on an exception list. You do not post write-offs or invent on-hand to close a hole.

**How to run:** Open or switch to a Work Item under `work-items/<id>/`. Follow this YAML one ready step (or the whole named job if requested). Then **journal-keeper**.

**Initial phase:** `role-job`

## Work map

```yaml
id: cycle-count
steps:
  - id: count
    needs: []
    produces: count-raw
    produce_path: work/count-raw.csv
    tool: docs/tools/count-sheet.md
    check: python docs/tools/checks/csv-has-columns.py work/count-raw.csv sku qty
    on_fail: retry
    next: [compare]
  - id: compare
    needs: [count-raw]
    produces: variance
    produce_path: work/count-variance.csv
    tool: docs/tools/spreadsheet.md
    check: python docs/tools/checks/csv-has-columns.py work/count-variance.csv sku qty
    on_fail: retry
    next: [pack]
  - id: pack
    needs: [variance]
    produces: count-pack
    produce_path: out/count-pack.md
    tool: docs/tools/spreadsheet.md
    check: python docs/tools/checks/file-exists.py out/count-pack.md
    on_fail: retry
    next: []
```

Starter work map. Replace tools and checks when the operator corrects this shop (**remember**).
