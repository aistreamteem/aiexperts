# Hold vs Definite

**When to use:** Build one list of tentative holds and definite bookings for the same date range. Keep status as they coded it. Flag same room-date conflicts and first-option versus second-option from their sheet. Do not upgrade a hold. Do not invent a cutoff or a room rate. Missing contract pointers on rows marked definite stay visible. They release or they sign. You hand a list plus write-up, not a live calendar change.

**How to run:** workflow-selector if no Work Item is active → follow this file one ready step (or whole named job if requested) → write artifacts under `work-items/<id>/` → journal-keeper

**Initial phase:** `role-job`

## Work map

```yaml
id: hold-vs-definite
steps:
  - id: holds
    needs: []
    produces: holds
    produce_path: work/holds.csv
    tool: docs/tools/hold-sheet.md
    check: python docs/tools/checks/csv-has-columns.py work/holds.csv date room status
    on_fail: retry
    next: [defs]
  - id: defs
    needs: [holds]
    produces: definites
    produce_path: work/definites.csv
    tool: docs/tools/definite-sheet.md
    check: python docs/tools/checks/csv-has-columns.py work/definites.csv date room status
    on_fail: retry
    next: [pack]
  - id: pack
    needs: [holds, definites]
    produces: hold-def-pack
    produce_path: out/hold-vs-definite.md
    tool: docs/tools/spreadsheet.md
    check: python docs/tools/checks/file-exists.py out/hold-vs-definite.md
    on_fail: retry
    next: []
```

Starter work map. Replace tools and checks when the operator teaches this shop (use remember).
