# Immunization Present Missing

**When to use:** Compare their immunization log to packet PDFs. List complete, incomplete, exempt-as-filed, or stale as they coded it. Apply their deadline file if present; do not invent exclusion law. Do not read shots as a clinician. Clinic-day returns count only as they logged them. They notify families. You pack the present-missing list. Do not stamp compliant. New enrollees and grade-entry deadlines may differ if their file splits them. They notify. You do not exclude a child at the door.

**How to run:** Open or continue a Work Item under `work-items/<id>/`. Put source files in `in/`. Walk one ready YAML step (or the whole named job if requested): produce the file, run the check, then **journal-keeper**.

**Initial phase:** `role-job`

## Work map

```yaml
id: immunization-present-missing
steps:
  - id: log
    needs: []
    produces: imm
    produce_path: work/immunization.csv
    tool: docs/tools/immunization-log.md
    check: python docs/tools/checks/file-exists.py work/immunization.csv
    on_fail: retry
    next: [packets]
  - id: packets
    needs: [imm]
    produces: packets
    produce_path: work/packet-index.csv
    tool: docs/tools/enrollment-pdf-folder.md
    check: python docs/tools/checks/file-exists.py work/packet-index.csv
    on_fail: retry
    next: [pack]
  - id: pack
    needs: [imm, packets]
    produces: imm-pack
    produce_path: out/immunization-present-missing.md
    tool: docs/tools/spreadsheet.md
    check: python docs/tools/checks/file-exists.py out/immunization-present-missing.md
    on_fail: retry
    next: []
```

Starter work map. Replace tools and checks when they correct this office (use **remember**).
