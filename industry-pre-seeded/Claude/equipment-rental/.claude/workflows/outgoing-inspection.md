# Outgoing Inspection

**When to use:** For units leaving today, check outgoing inspection sheets against the fleet row: meter, fuel, kit, manual present, photos if required. Do not invent hours or fuel. Do not diagnose. Missing required serial or blank meter is an ask. Licensed-operator ask completeness follows their form only — no license stamp. Pack the incompletes and the pack. They hold the gate. Indoor-height asks stay questions, not engineering. Card PAN does not belong on the sheet.

**How to run:** Open or continue a Work Item under `work-items/<id>/`. Follow this file one ready step (or the whole named job if requested). Read the named tool under `docs/tools/`. Write artifacts under this Work Item (`work/` and `out/` mean `work-items/<id>/work/` and `work-items/<id>/out/`). Run the step check against those paths. After each step, run **journal-keeper**. If a required file or shop rule is missing, ask (**operator-qa** when the answer would change the pack). Do not invent rates, meters, serials, zones, deposits, or fees.

**Initial phase:** `role-job`

## Work map

```yaml
id: outgoing-inspection
steps:
  - id: insp
    needs: []
    produces: outgoing
    produce_path: work/outgoing-inspections.csv
    tool: docs/tools/inspection-sheet.md
    check: python docs/tools/checks/csv-has-columns.py work/outgoing-inspections.csv unit
    on_fail: retry
    next: [fleet]
  - id: fleet
    needs: [outgoing]
    produces: fleet
    produce_path: work/fleet.csv
    tool: docs/tools/fleet-csv.md
    check: python docs/tools/checks/file-exists.py work/fleet.csv
    on_fail: retry
    next: [photos]
  - id: photos
    needs: [fleet]
    produces: photos
    produce_path: work/outgoing-photos.csv
    tool: docs/tools/photo-folder.md
    check: python docs/tools/checks/file-exists.py work/outgoing-photos.csv
    on_fail: retry
    next: [pack]
  - id: pack
    needs: [outgoing, fleet, photos]
    produces: out-insp-pack
    produce_path: out/outgoing-inspection.md
    tool: docs/tools/spreadsheet.md
    check: python docs/tools/checks/file-exists.py out/outgoing-inspection.md
    on_fail: retry
    next: []
```

Starter work map. Replace tools and checks when the operator confirms this yard's process (save with **remember**).
