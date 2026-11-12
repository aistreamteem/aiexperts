# Cutoff List

**When to use:** From the hold sheet, list tentative options with cutoff on or before the pack date, plus blank cutoff cells as asks. Do not invent a release date. Do not release space. Do not upgrade a hold to definite. Room-block cutoff is a different clock if a group-block file exists — label it separately only when that file is present. They call the planner. You deliver the due-to-release list plus write-up.

**How to run:** workflow-selector if no Work Item is active → follow this file one ready step (or whole named job if requested) → write artifacts under `work-items/<id>/` → journal-keeper

**Initial phase:** `role-job`

## Work map

```yaml
id: cutoff-list
steps:
  - id: holds
    needs: []
    produces: holds
    produce_path: work/holds.csv
    tool: docs/tools/hold-sheet.md
    check: python docs/tools/checks/csv-has-columns.py work/holds.csv date room status
    on_fail: retry
    next: [pack]
  - id: pack
    needs: [holds]
    produces: cutoff-pack
    produce_path: out/cutoff-list.md
    tool: docs/tools/spreadsheet.md
    check: python docs/tools/checks/file-exists.py out/cutoff-list.md
    on_fail: retry
    next: []
```

Starter work map. Replace tools and checks when the operator teaches this shop (use remember).
