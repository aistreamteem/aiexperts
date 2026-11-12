# Vehicle-Add Paperwork

**When to use:** From the endorsement sheet, list each vehicle add: VIN as they provided, requested effective date, and whether a title or registration PDF is present. Compare to the current dec schedule so duplicates show. Do not invent a VIN or value. Flag backdates. Do not say the unit is covered. ID cards wait for their issued or binder file. They submit the change. You pack missing docs only.

**How to run:** Open or continue a Work Item under `work-items/<id>/`. Put AMS exports and PDFs in `in/`. Read this file and the named `docs/tools/` doc. Walk one ready YAML step (or the whole job if requested): produce the file under this Work Item’s `work/` or `out/`, run the check, then journal-keeper. Do not skip a step with a chat summary.

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

Starter work map. Replace tools and checks when the operator corrects this shop (remember / integrate-docs).
