# Occupancy

**When to use:** Build the occupancy list from their rent-roll or occupancy export: unit, status, occupant label, and size if the file has it. Keep reserved, company, damaged, and auction-hold as they coded them. Do not invent vacant or occupied from a photo. Do not invent a rate. Python may write a summary CSV or a named chart only if they asked and the columns exist. They use the list. You write the pack and questions, not a same-store growth story.

**How to run:** Open or continue a Work Item under `work-items/<id>/`. Put the occupancy or rent-roll export in `in/`. Read this file and `docs/tools/occupancy-export.md`. Walk one ready YAML step (or the whole job if requested): produce the file under this Work Item’s `work/` or `out/`, run the check, then journal-keeper. Do not skip a step with a chat summary.

**Initial phase:** `role-job`

## Work map

```yaml
id: occupancy
steps:
  - id: pull
    needs: []
    produces: occ
    produce_path: work/occupancy.csv
    tool: docs/tools/occupancy-export.md
    check: python docs/tools/checks/csv-has-columns.py work/occupancy.csv unit status
    on_fail: retry
    next: [pack]
  - id: pack
    needs: [occ]
    produces: occ-pack
    produce_path: out/occupancy.md
    tool: docs/tools/occupancy-export.md
    check: python docs/tools/checks/file-exists.py out/occupancy.md
    on_fail: retry
    next: []
```

Starter work map. Replace tools and checks when the operator corrects this shop via **remember**.
