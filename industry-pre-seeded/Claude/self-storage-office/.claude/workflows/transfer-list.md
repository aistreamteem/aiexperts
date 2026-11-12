# Transfer List

**When to use:** List open unit transfers from their spreadsheet or occupancy notes: old unit, new unit, date, and whether a new agreement PDF exists. Do not invent a prorate or the new rate. If the new unit is still occupied on the export, flag the clash. Gate access follows the new unit as process, never a code. Combo adds stay labeled if that is their reason. They approve the swap. You pack leftovers and missing agreements.

**How to run:** Open or continue a Work Item under `work-items/<id>/`. Put occupancy notes or the transfer spreadsheet in `in/`. Read this file and `docs/tools/occupancy-export.md` / `docs/tools/spreadsheet.md`. Walk one ready YAML step (or the whole job if requested): produce the file under this Work Item’s `work/` or `out/`, run the check, then journal-keeper. Do not skip a step with a chat summary.

**Initial phase:** `role-job`

## Work map

```yaml
id: transfer-list
steps:
  - id: occ
    needs: []
    produces: occ
    produce_path: work/occupancy.csv
    tool: docs/tools/occupancy-export.md
    check: python docs/tools/checks/csv-has-columns.py work/occupancy.csv unit status
    on_fail: retry
    next: [xfer]
  - id: xfer
    needs: [occ]
    produces: xfer
    produce_path: work/transfers.csv
    tool: docs/tools/spreadsheet.md
    check: python docs/tools/checks/file-exists.py work/transfers.csv
    on_fail: retry
    next: [pack]
  - id: pack
    needs: [occ, xfer]
    produces: xfer-pack
    produce_path: out/transfer-list.md
    tool: docs/tools/spreadsheet.md
    check: python docs/tools/checks/file-exists.py out/transfer-list.md
    on_fail: retry
    next: []
```

Starter work map. Replace tools and checks when the operator corrects this shop via **remember**.
