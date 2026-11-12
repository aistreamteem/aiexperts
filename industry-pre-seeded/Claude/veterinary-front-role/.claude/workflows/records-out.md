# Records Out

**When to use:** Log client or clinic requests and whether an authorization file is present. Do not interpret the chart. Do not invent a hold policy. Their written policy and the veterinarian decide releases and any balance questions. Record destination, date, method, and what was sent when they tell you. Minimum data in the pack: requestor, patient ID, file names. Starter / guess until they teach who approves a release.

**How to run:** Open or continue a Work Item under `work-items/<id>/`. Put the request and authorization files in `in/`. Read this file and the named `docs/tools/` doc. Walk one ready YAML step (or the whole job if requested): produce the file under this Work Item’s `work/` or `out/`, run the check, then journal-keeper. Do not skip a step with a chat summary.

**Initial phase:** `role-job`

## Work map

```yaml
id: records-out
steps:
  - id: log
    needs: []
    produces: rec-out
    produce_path: work/records-out.csv
    tool: docs/tools/records-pdf.md
    check: python docs/tools/checks/file-exists.py work/records-out.csv
    on_fail: retry
    next: [write]
  - id: write
    needs: [rec-out]
    produces: rec-out-writeup
    produce_path: out/records-out.md
    tool: docs/tools/records-pdf.md
    check: python docs/tools/checks/file-exists.py out/records-out.md
    on_fail: retry
    next: []
```

Starter work map. Replace tools and checks when they correct this clinic.
