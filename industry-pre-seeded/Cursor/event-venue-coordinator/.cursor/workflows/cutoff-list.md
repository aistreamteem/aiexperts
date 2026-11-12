# Hold cutoff list

**When to use:** From the hold sheet, list tentative options with cutoff on or before the pack date, plus blank cutoff cells as asks. Do not invent a release date. Do not release space. Do not upgrade a hold to definite. Room-block cutoff is a different clock if a group-block file exists — label it separately only when that file is present. They call the planner. You deliver the due-to-release pack.

**How to run:** Open or continue a Work Item under `work-items/<id>/`. Put the hold sheet in `in/`. Read this file and `docs/tools/hold-sheet.md` / `docs/tools/spreadsheet.md`. Walk one ready YAML step (or the whole job if requested): produce the file under this Work Item’s `work/` or `out/`, run the check, then journal-keeper. Do not skip a step with a chat summary.

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

Starter work map. Replace tools and checks when the operator corrects this shop (remember / integrate-docs).
