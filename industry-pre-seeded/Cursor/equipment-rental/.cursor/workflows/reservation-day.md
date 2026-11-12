# Reservation Day

**When to use:** Build today’s reservation list from their reservation export and fleet statuses. Keep reserved distinct from available and on rent. Flag overlaps using their overbook rule; if there is no rule, ask and do not silently double-book. Do not invent a unit or a rate. Substitution stays a question when the reserved serial is in shop. After-hours flags copy from their file. Write the pack and the exception pack. They call renters and they dispatch.

**How to run:** Open or continue a Work Item under `work-items/<id>/`. Follow this file one ready step (or the whole named job if requested). Read the named tool under `docs/tools/`. Write artifacts under this Work Item (`work/` and `out/` mean `work-items/<id>/work/` and `work-items/<id>/out/`). Run the step check against those paths. After each step, run **journal-keeper**. If a required file or shop rule is missing, ask (**operator-qa** when the answer would change the pack). Do not invent rates, meters, serials, zones, deposits, or fees.

**Initial phase:** `role-job`

## Work map

```yaml
id: reservation-day
steps:
  - id: res
    needs: []
    produces: reservations
    produce_path: work/reservations.csv
    tool: docs/tools/reservation-csv.md
    check: python docs/tools/checks/csv-has-columns.py work/reservations.csv date
    on_fail: retry
    next: [fleet]
  - id: fleet
    needs: [reservations]
    produces: fleet
    produce_path: work/fleet.csv
    tool: docs/tools/fleet-csv.md
    check: python docs/tools/checks/csv-has-columns.py work/fleet.csv unit status
    on_fail: retry
    next: [pack]
  - id: pack
    needs: [reservations, fleet]
    produces: res-pack
    produce_path: out/reservation-day.md
    tool: docs/tools/spreadsheet.md
    check: python docs/tools/checks/file-exists.py out/reservation-day.md
    on_fail: retry
    next: []
```

Starter work map. Replace tools and checks when the operator confirms this yard's process (save with **remember**).
