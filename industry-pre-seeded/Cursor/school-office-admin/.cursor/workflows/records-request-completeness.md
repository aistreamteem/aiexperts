# Records Request Completeness

**When to use:** Check each records or transcript request against their process checklist: form present, identity as they log it, hold flags from the SIS, and which documents they treat as in scope. Do not release files. Do not stamp FERPA-legal. Do not invent a fee. IEP contents stay out of the write-up. They authorize. You pack status and missing steps. Partial scopes stay partial. Court packets still go to their designated official. You do not send. FERPA is their process, not your stamp. They authorize the release.

**How to run:** Open or continue a Work Item under `work-items/<id>/`. Put source files in `in/`. Walk one ready YAML step (or the whole named job if requested): produce the file, run the check, then **journal-keeper**.

**Initial phase:** `role-job`

## Work map

```yaml
id: records-request-completeness
steps:
  - id: log
    needs: []
    produces: requests
    produce_path: work/records-requests.csv
    tool: docs/tools/transcript-request-log.md
    check: python docs/tools/checks/csv-has-columns.py work/records-requests.csv student date
    on_fail: retry
    next: [sis]
  - id: sis
    needs: [requests]
    produces: roster
    produce_path: work/sis-students.csv
    tool: docs/tools/sis-export.md
    check: python docs/tools/checks/file-exists.py work/sis-students.csv
    on_fail: retry
    next: [pack]
  - id: pack
    needs: [requests, roster]
    produces: rec-pack
    produce_path: out/records-request-completeness.md
    tool: docs/tools/spreadsheet.md
    check: python docs/tools/checks/file-exists.py out/records-request-completeness.md
    on_fail: retry
    next: []
```

Starter work map. Replace tools and checks when they correct this office (use **remember**).
