# LOTO form present

**When to use:** For work orders that their export or rule file marks as needing lockout, index whether a machine-specific procedure PDF sits in the procedure folder. List present or missing. Do not write isolation steps. Do not stamp OSHA. Do not say the lockout was performed. Write-up is a completeness list plus which assets have no file, not a safety inspection and not a PE energy study.

**How to run:** Open or continue a Work Item under `work-items/<id>/`. Put source files in `in/`. Walk one ready YAML step (or the whole named job if requested): produce the file, run the check, then **journal-keeper**. Paths `in/`, `work/`, `out/`, and `evidence/` are inside that Work Item.

**Initial phase:** `role-job`

## Work map

```yaml
id: loto-form-present
steps:
  - id: tickets
    needs: []
    produces: tickets
    produce_path: work/wo.csv
    tool: docs/tools/wo-csv.md
    check: python docs/tools/checks/csv-has-columns.py work/wo.csv wo asset priority
    on_fail: retry
    next: [forms]
  - id: forms
    needs: [tickets]
    produces: forms
    produce_path: work/loto-index.csv
    tool: docs/tools/procedure-pdf-folder.md
    check: python docs/tools/checks/file-exists.py work/loto-index.csv
    on_fail: retry
    next: [pack]
  - id: pack
    needs: [tickets, forms]
    produces: loto-pack
    produce_path: out/loto-form-present.md
    tool: docs/tools/spreadsheet.md
    check: python docs/tools/checks/file-exists.py out/loto-form-present.md
    on_fail: retry
    next: []
```

Starter work map. Replace tools and checks when the operator corrects this plant through **remember**.
