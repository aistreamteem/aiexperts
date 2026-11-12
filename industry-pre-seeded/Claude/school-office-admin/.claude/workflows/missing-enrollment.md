# Missing Enrollment

**When to use:** Index the enrollment PDF folder against their required-page checklist. List present versus missing for each student on the SIS export if they provided one. Do not invent a required form. Do not mark enrolled. Do not copy SSNs. Custody and immunization pages are present or missing only. They collect signatures. You pack the missing-forms list and a write-up. If they have no checklist, ask before you invent pages. Mid-year enrollees use the same list unless they wrote a short form. They decide enrollment. You do not mark a seat filled.

**How to run:** Open or switch to a Work Item under `work-items/<id>/`. Walk this YAML one ready step (or the whole named job if requested): read the named `docs/tools/` file, write `produce_path` inside this Work Item, run `check` against those paths, then **journal-keeper**.

**Initial phase:** `role-job`

## Work map

```yaml
id: missing-enrollment
steps:
  - id: folder
    needs: []
    produces: packets
    produce_path: work/packet-index.csv
    tool: docs/tools/enrollment-pdf-folder.md
    check: python docs/tools/checks/file-exists.py work/packet-index.csv
    on_fail: retry
    next: [roster]
  - id: roster
    needs: [packets]
    produces: roster
    produce_path: work/sis-students.csv
    tool: docs/tools/sis-export.md
    check: python docs/tools/checks/csv-has-columns.py work/sis-students.csv student
    on_fail: retry
    next: [pack]
  - id: pack
    needs: [packets, roster]
    produces: missing-pack
    produce_path: out/missing-enrollment.md
    tool: docs/tools/spreadsheet.md
    check: python docs/tools/checks/file-exists.py out/missing-enrollment.md
    on_fail: retry
    next: []
```

Starter work map. Replace tools and checks when they correct this office (use **remember**).
