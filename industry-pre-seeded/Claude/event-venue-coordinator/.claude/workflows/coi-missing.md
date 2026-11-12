# COI Missing

**When to use:** From definite events, list which renter or required vendor COIs are present, expired, missing additional-insured wording, or missing event dates against their checklist. Do not say anyone is covered. Do not invent a limit. Declarations pages pass only if their checklist says so. They chase the client. You keep every miss visible on the list plus write-up. Group vendor COIs with the event they belong to. A declarations page is not a pass unless their checklist says so. They chase the client; you do not call the insurer or bind coverage.

**How to run:** workflow-selector if no Work Item is active → follow this file one ready step (or whole named job if requested) → write artifacts under `work-items/<id>/` → journal-keeper

**Initial phase:** `role-job`

## Work map

```yaml
id: coi-missing
steps:
  - id: defs
    needs: []
    produces: definites
    produce_path: work/definites.csv
    tool: docs/tools/definite-sheet.md
    check: python docs/tools/checks/csv-has-columns.py work/definites.csv date room status
    on_fail: retry
    next: [cois]
  - id: cois
    needs: [definites]
    produces: cois
    produce_path: work/cois.csv
    tool: docs/tools/renter-coi-folder.md
    check: python docs/tools/checks/file-exists.py work/cois.csv
    on_fail: retry
    next: [pack]
  - id: pack
    needs: [definites, cois]
    produces: coi-pack
    produce_path: out/coi-missing.md
    tool: docs/tools/renter-coi-folder.md
    check: python docs/tools/checks/file-exists.py out/coi-missing.md
    on_fail: retry
    next: []
```

Starter work map. Replace tools and checks when the operator teaches this shop (use remember).
