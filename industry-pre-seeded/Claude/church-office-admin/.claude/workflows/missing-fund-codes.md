# Missing fund codes

**When to use:** From the giving export they dropped, list rows with a blank fund or a code not on their chart if they also stored a chart. Do not default a blank to general. Do not invent a fund from a pew note. Quote note versus dropdown when both exist. Write-up is a missing-code list, not a recode and not a tax opinion. They recode. You flag holes.

**How to run:** Open `work-items/<id>/`. Read this file. For one ready step (or the whole job if they asked): follow the `tool` doc, write `produce_path` inside that Work Item, run `check` from there. Then journal-keeper. See `.claude/workflows/README.md`.

**Initial phase:** `intake`

## Work map

```yaml
id: missing-fund-codes
steps:
  - id: export
    needs: []
    produces: gifts
    produce_path: work/giving-export.csv
    tool: docs/tools/giving-export.md
    check: python docs/tools/checks/csv-has-columns.py work/giving-export.csv amount fund
    on_fail: retry
    next: [pack]
  - id: pack
    needs: [gifts]
    produces: fund-pack
    produce_path: out/missing-fund-codes.md
    tool: docs/tools/spreadsheet.md
    check: python docs/tools/checks/file-exists.py out/missing-fund-codes.md
    on_fail: retry
    next: []
```

Starter work map. Replace tools and checks when the operator corrects how this office works.
