# Records-release log

**When to use:** From the ROI folder and their release log, list request date, requester type as they coded, ROI present or missing, and send status as recorded. You do not release records and you do not copy the chart into docs/. Third-party rows still need their form. Fees come only from their records-fee sheet. Expired ROI dates stay questions. Prefer chart label. They ship. You pack the completeness list plus a write-up.

**How to run:** Open or reuse `work-items/<id>/`. Follow this file’s YAML one ready step (or the whole named job if requested). Then **journal-keeper**.

**Initial phase:** `role-job`

## Work map

```yaml
id: records-release-log
steps:
  - id: roi
    needs: []
    produces: roi
    produce_path: work/roi-index.csv
    tool: docs/tools/roi-form-folder.md
    check: python docs/tools/checks/file-exists.py work/roi-index.csv
    on_fail: retry
    next: [log]
  - id: log
    needs: [roi]
    produces: log
    produce_path: work/release-log.csv
    tool: docs/tools/spreadsheet.md
    check: python docs/tools/checks/csv-has-columns.py work/release-log.csv chart status
    on_fail: retry
    next: [write]
  - id: write
    needs: [roi, log]
    produces: roi-writeup
    produce_path: out/records-release.md
    tool: docs/tools/roi-form-folder.md
    check: python docs/tools/checks/file-exists.py out/records-release.md
    on_fail: retry
    next: []
```

Starter work map. Replace tools and checks when the operator confirms how *this* clinic works (**remember**).
