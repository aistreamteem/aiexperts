# ACORD Completeness

**When to use:** Index the ACORD and application PDFs they dropped. List form number, named insured as written, and blank required boxes. Do not fill class codes, FEIN, payroll, or VINs from memory. Do not call the packet ready to bind. Unsigned producer blocks stay unsigned. Attach a missing-forms CSV the producer can work. They obtain answers and they submit. You keep present-versus-missing visible.

**How to run:** Open or continue a Work Item under `work-items/<id>/`. Put AMS exports and PDFs in `in/`. Read this file and the named `docs/tools/` doc. Walk one ready YAML step (or the whole job if requested): produce the file under this Work Item’s `work/` or `out/`, run the check, then journal-keeper. Do not skip a step with a chat summary.

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

Starter work map. Replace tools and checks when the operator corrects this shop (remember / integrate-docs).
