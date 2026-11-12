# Supply Below Par

**When to use:** Compare on-hand to their par or min on the supply par sheet. Flag at or below their min. Do not invent a min, a brand, or a case count. Do not place an order. Chemical rows stay names from their sheet; mixes stay out. One SKU and closet per row. Write-up is the below-par list plus blank-min asks. They buy. You pack the flags the check can see.

**How to run:** Use **continue** with this workflow. Work inside `work-items/<id>/`. For each step: read the tool doc, produce the file, run the check (retry at most 3, then ask), then **journal-keeper**. Do not invent a min, brand, or case count. Do not place an order.

**Initial phase:** `pars`

## Work map

```yaml
id: supply-below-par
steps:
  - id: pars
    needs: []
    produces: pars
    produce_path: work/supply-par.csv
    tool: docs/tools/supply-par-sheet.md
    check: python docs/tools/checks/csv-has-columns.py work/supply-par.csv sku min
    on_fail: retry
    next: [pack]
  - id: pack
    needs: [pars]
    produces: below-par-pack
    produce_path: out/supply-below-par.md
    tool: docs/tools/spreadsheet.md
    check: python docs/tools/checks/file-exists.py out/supply-below-par.md
    on_fail: retry
    next: []
```

Starter map. Replace tools and checks when the operator corrects this shop (**remember**).
