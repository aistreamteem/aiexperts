# End-of-Day Manifest

**When to use:** Compare live label PDFs to the carrier manifest export. Voided labels must not appear as tendered. Holds and will-calls stay off the street manifest. Do not invent a pickup confirmation or a close timestamp. Missing manifest file: say missing, do not mark the day closed. They click close. You do not pay daily pickup fees. Will-call and hold-for-pickup must not appear as street tenders. Unmanifested live labels are exceptions. They click close in the tool. You do not invent a driver pickup name.

**How to run:** Open or switch to a Work Item under `work-items/<id>/`. Put source files in that item's `in/`. Follow the YAML steps below — one ready step per **continue**, or the whole named job if requested. Read the named `docs/tools/` doc. Produce files under this Work Item. Run each step's check. Then **journal-keeper**.

**Initial phase:** `role-job`

## Work map

```yaml
id: end-of-day-manifest
steps:
  - id: labels
    needs: []
    produces: labels
    produce_path: work/labels-index.csv
    tool: docs/tools/label-pdf-folder.md
    check: python docs/tools/checks/file-exists.py work/labels-index.csv
    on_fail: retry
    next: [carrier]
  - id: carrier
    needs: [labels]
    produces: manifest
    produce_path: work/manifest.csv
    tool: docs/tools/carrier-export.md
    check: python docs/tools/checks/file-exists.py work/manifest.csv
    on_fail: retry
    next: [pack]
  - id: pack
    needs: [labels, manifest]
    produces: eod-pack
    produce_path: out/end-of-day-manifest.md
    tool: docs/tools/spreadsheet.md
    check: python docs/tools/checks/file-exists.py out/end-of-day-manifest.md
    on_fail: retry
    next: []
```

Starter work map. Replace tools and checks when they correct this shop.
