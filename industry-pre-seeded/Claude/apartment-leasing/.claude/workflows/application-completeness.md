# Application Completeness

**When to use:** Index the application PDFs, mark each required form present or missing on a CSV, and write the pack. Do not decide income or credit. Do not approve or deny. Do not copy SSNs into the missing-forms sheet. Unreadable scans are missing-quality. Guarantor and roommate packets get their own rows if their checklist says so. They chase the applicant. Completeness is not a screening verdict.

**How to run:** Open or continue a Work Item under `work-items/<id>/`. Put application PDFs in `in/`. Read this file and `docs/tools/application-pdf-folder.md` / `docs/tools/spreadsheet.md`. Walk one ready YAML step (or the whole job if requested): produce the file under this Work Item’s `work/` or `out/`, run the check, then journal-keeper. Do not skip a step with a chat summary.

**Initial phase:** `role-job`

## Work map

```yaml
id: application-completeness
steps:
  - id: pdfs
    needs: []
    produces: pdfs
    produce_path: work/application-index.csv
    tool: docs/tools/application-pdf-folder.md
    check: python docs/tools/checks/file-exists.py work/application-index.csv
    on_fail: retry
    next: [missing]
  - id: missing
    needs: [pdfs]
    produces: missing
    produce_path: work/missing-forms.csv
    tool: docs/tools/spreadsheet.md
    check: python docs/tools/checks/csv-has-columns.py work/missing-forms.csv applicant form
    on_fail: retry
    next: [pack]
  - id: pack
    needs: [pdfs, missing]
    produces: app-pack
    produce_path: out/application-completeness.md
    tool: docs/tools/spreadsheet.md
    check: python docs/tools/checks/file-exists.py out/application-completeness.md
    on_fail: retry
    next: []
```

Starter work map. Replace tools and checks when the operator corrects this shop (remember / integrate-docs).
