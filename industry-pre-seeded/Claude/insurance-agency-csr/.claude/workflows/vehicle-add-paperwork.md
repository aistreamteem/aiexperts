# Vehicle-Add Paperwork

**When to use:** From the endorsement sheet, list each vehicle add: VIN as they provided, requested effective date, and whether a title or registration PDF is present. Compare to the current dec schedule so duplicates show. Do not invent a VIN or value. Flag backdates. Do not say the unit is covered. ID cards wait for their issued or binder file. They submit the change. You pack missing docs only.

**How to run:** workflow-selector if this Work Item has no Workflow type yet. Follow the map below: read the named tool doc, write the produced file under `work-items/<id>/`, run the check from that folder, then journal-keeper. Paths `work/` and `out/` are relative to the Work Item. One ready step per continue (or the whole named job if requested).

**Initial phase:** `role-job`

## Work map

```yaml
id: vehicle-add-paperwork
steps:
  - id: end
    needs: []
    produces: endorsements
    produce_path: work/endorsements.csv
    tool: docs/tools/endorsement-sheet.md
    check: python docs/tools/checks/csv-has-columns.py work/endorsements.csv vin effective_date
    on_fail: retry
    next: [dec]
  - id: dec
    needs: [endorsements]
    produces: dec
    produce_path: work/dec-index.csv
    tool: docs/tools/dec-page-folder.md
    check: python docs/tools/checks/file-exists.py work/dec-index.csv
    on_fail: retry
    next: [pack]
  - id: pack
    needs: [endorsements, dec]
    produces: veh-pack
    produce_path: out/vehicle-add.md
    tool: docs/tools/endorsement-sheet.md
    check: python docs/tools/checks/file-exists.py out/vehicle-add.md
    on_fail: retry
    next: []
```

Starter work map. Replace tools and checks when they **remember** how *this* agency files.
