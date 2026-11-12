# Giving batch from export

**When to use:** List one batch they named from the giving export, then set it next to their signed count sheet. Flag amount or fund holes. Quote export versus sheet when they disagree. Do not invent a gift. Do not invent a deductible. Do not store account numbers. Dual-control signatures stay as written; you do not recount. Write-up is completeness, not a posting. They post and they deposit.

**How to run:** Open or continue the Work Item under `work-items/<id>/`. Walk one ready YAML step (or the whole named job if requested): produce the file, run the check, then journal-keeper.

**Initial phase:** `role-job`

## Work map

```yaml
id: giving-batch-from-export
steps:
  - id: export
    needs: []
    produces: gifts
    produce_path: work/giving-export.csv
    tool: docs/tools/giving-export.md
    check: python docs/tools/checks/csv-has-columns.py work/giving-export.csv amount fund
    on_fail: retry
    next: [count]
  - id: count
    needs: [gifts]
    produces: count
    produce_path: work/count-sheet.csv
    tool: docs/tools/count-sheet.md
    check: python docs/tools/checks/csv-has-columns.py work/count-sheet.csv batch amount
    on_fail: retry
    next: [pack]
  - id: pack
    needs: [gifts, count]
    produces: batch-pack
    produce_path: out/giving-batch.md
    tool: docs/tools/spreadsheet.md
    check: python docs/tools/checks/file-exists.py out/giving-batch.md
    on_fail: retry
    next: []
```

Starter work map. Replace tools and checks when they correct this shop (**remember**).
