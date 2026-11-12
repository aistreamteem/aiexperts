# Hold versus definite list

**When to use:** Build one list of tentative holds and definite bookings for the same date range. Keep status as they coded it. Flag same room-date conflicts and first-option versus second-option from their sheet. Do not upgrade a hold. Do not invent a cutoff or a room rate. Missing contract pointers on rows marked definite stay visible. They release or they sign. You hand a list pack, not a live calendar change.

**How to run:** Open or continue a Work Item under `work-items/<id>/`. Put the hold sheet and definite sheet in `in/`. Read this file and `docs/tools/hold-sheet.md` / `docs/tools/definite-sheet.md`. Walk one ready YAML step (or the whole job if requested): produce the file under this Work Item’s `work/` or `out/`, run the check, then journal-keeper. Do not skip a step with a chat summary.

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

Starter work map. Replace tools and checks when the operator corrects this shop (remember / integrate-docs).
