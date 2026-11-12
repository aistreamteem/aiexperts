# ACORD Completeness

**When to use:** Index the ACORD and application PDFs they dropped. List form number, named insured as written, and blank required boxes. Do not fill class codes, FEIN, payroll, or VINs from memory. Do not call the packet ready to bind. Unsigned producer blocks stay unsigned. Attach a missing-forms CSV the producer can work. They obtain answers and they submit. You keep present-versus-missing visible.

**How to run:** workflow-selector if this Work Item has no Workflow type yet. Follow the map below: read the named tool doc, write the produced file under `work-items/<id>/`, run the check from that folder, then journal-keeper. Paths `work/` and `out/` are relative to the Work Item. One ready step per continue (or the whole named job if requested).

**Initial phase:** `role-job`

## Work map

```yaml
id: acord-completeness
steps:
  - id: folder
    needs: []
    produces: acord
    produce_path: work/acord-index.csv
    tool: docs/tools/acord-pdf-folder.md
    check: python docs/tools/checks/file-exists.py work/acord-index.csv
    on_fail: retry
    next: [pack]
  - id: pack
    needs: [acord]
    produces: acord-pack
    produce_path: out/acord-missing.md
    tool: docs/tools/spreadsheet.md
    check: python docs/tools/checks/file-exists.py out/acord-missing.md
    on_fail: retry
    next: []
```

Starter work map. Replace tools and checks when they **remember** how *this* agency files.
