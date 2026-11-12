# Pledge versus received

**When to use:** Join their pledge sheet to gifts their process counts toward a pledge. Do not invent a pledge or a receipt. Do not send a reminder campaign. Do not call a household behind. Funds must match if they pledge by fund. Write-up is fulfillment plus holes, not pastoral pressure and not a tax opinion. They talk to households. You list the join.

**How to run:** Open `work-items/<id>/`. Read this file. For one ready step (or the whole job if they asked): follow the `tool` doc, write `produce_path` inside that Work Item, run `check` from there. Then journal-keeper. See `.claude/workflows/README.md`.

**Initial phase:** `intake`

## Work map

```yaml
id: pledge-vs-received
steps:
  - id: pledges
    needs: []
    produces: pledges
    produce_path: work/pledges.csv
    tool: docs/tools/pledge-sheet.md
    check: python docs/tools/checks/csv-has-columns.py work/pledges.csv pledge received
    on_fail: retry
    next: [export]
  - id: export
    needs: [pledges]
    produces: gifts
    produce_path: work/giving-export.csv
    tool: docs/tools/giving-export.md
    check: python docs/tools/checks/file-exists.py work/giving-export.csv
    on_fail: retry
    next: [pack]
  - id: pack
    needs: [pledges, gifts]
    produces: pledge-pack
    produce_path: out/pledge-vs-received.md
    tool: docs/tools/spreadsheet.md
    check: python docs/tools/checks/file-exists.py out/pledge-vs-received.md
    on_fail: retry
    next: []
```

Starter work map. Replace tools and checks when the operator corrects how this office works.
