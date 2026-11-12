# Utilization

**When to use:** Compute or copy utilization from their fleet and contract or reservation exports using only the formula they wrote. Keep idle and shop visible. Do not invent a percent and do not invent rates for a dollar view. Serials must match the fleet file. Weekend and holiday treatment follows their sheet. Hand them the list plus pack. They decide transfers, sales, or rate-file changes. You do not hide a dead unit to make the board look busy.

**How to run:** Open or continue a Work Item under `work-items/<id>/`. Follow this file one ready step (or the whole named job if requested). Read the named tool under `docs/tools/`. Write artifacts under this Work Item (`work/` and `out/` mean `work-items/<id>/work/` and `work-items/<id>/out/`). Run the step check against those paths. After each step, run **journal-keeper**. If a required file or shop rule is missing, ask (**operator-qa** when the answer would change the pack). Do not invent rates, meters, serials, zones, deposits, or fees.

**Initial phase:** `role-job`

## Work map

```yaml
id: utilization
steps:
  - id: fleet
    needs: []
    produces: fleet
    produce_path: work/fleet.csv
    tool: docs/tools/fleet-csv.md
    check: python docs/tools/checks/csv-has-columns.py work/fleet.csv unit status
    on_fail: retry
    next: [onrent]
  - id: onrent
    needs: [fleet]
    produces: onrent
    produce_path: work/on-rent.csv
    tool: docs/tools/reservation-csv.md
    check: python docs/tools/checks/file-exists.py work/on-rent.csv
    on_fail: retry
    next: [pack]
  - id: pack
    needs: [fleet, onrent]
    produces: util-pack
    produce_path: out/utilization.md
    tool: docs/tools/spreadsheet.md
    check: python docs/tools/checks/file-exists.py out/utilization.md
    on_fail: retry
    next: []
```

Starter work map. Replace tools and checks when the operator confirms this yard's process (save with **remember**).
