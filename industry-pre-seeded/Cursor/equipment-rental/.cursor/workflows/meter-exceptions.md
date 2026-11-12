# Meter Exceptions

**When to use:** Compare meter or telematics export to fleet and inspection hours. Flag blanks, return below outgoing, and GPS-versus-gauge disagreements. Do not invent a reading and do not diagnose a rolled meter. Overage math waits for their allowance file and both real readings. Portal passwords stay out. Produce the exception list and pack. They re-read the unit or they accept a photo as the record if that is their rule.

**How to run:** Open or continue a Work Item under `work-items/<id>/`. Follow this file one ready step (or the whole named job if requested). Read the named tool under `docs/tools/`. Write artifacts under this Work Item (`work/` and `out/` mean `work-items/<id>/work/` and `work-items/<id>/out/`). Run the step check against those paths. After each step, run **journal-keeper**. If a required file or shop rule is missing, ask (**operator-qa** when the answer would change the pack). Do not invent rates, meters, serials, zones, deposits, or fees.

**Initial phase:** `role-job`

## Work map

```yaml
id: meter-exceptions
steps:
  - id: meter
    needs: []
    produces: meters
    produce_path: work/meters.csv
    tool: docs/tools/meter-export.md
    check: python docs/tools/checks/csv-has-columns.py work/meters.csv unit
    on_fail: retry
    next: [fleet]
  - id: fleet
    needs: [meters]
    produces: fleet
    produce_path: work/fleet.csv
    tool: docs/tools/fleet-csv.md
    check: python docs/tools/checks/file-exists.py work/fleet.csv
    on_fail: retry
    next: [pack]
  - id: pack
    needs: [meters, fleet]
    produces: meter-pack
    produce_path: out/meter-exceptions.md
    tool: docs/tools/spreadsheet.md
    check: python docs/tools/checks/file-exists.py out/meter-exceptions.md
    on_fail: retry
    next: []
```

Starter work map. Replace tools and checks when the operator confirms this yard's process (save with **remember**).
