# Transcript Request Log

**When to use:** List open transcript requests from their log. Join student_id to the SIS export so holds and withdrawn status stay visible. Do not invent grades. Do not lift a hold. Do not send the transcript. Official versus unofficial stays as they labeled it. Completeness of the signed request is a column, not a legal FERPA stamp. They authorize and they send.

**How to run:** Open or switch to a Work Item under `work-items/<id>/`. Walk this YAML one ready step (or the whole named job if requested): read the named `docs/tools/` file, write `produce_path` inside this Work Item, run `check` against those paths, then **journal-keeper**.

**Initial phase:** `role-job`

## Work map

```yaml
id: transcript-request-log
steps:
  - id: log
    needs: []
    produces: requests
    produce_path: work/transcript-requests.csv
    tool: docs/tools/transcript-request-log.md
    check: python docs/tools/checks/csv-has-columns.py work/transcript-requests.csv student date
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
    produces: tr-pack
    produce_path: out/transcript-request-pack.md
    tool: docs/tools/spreadsheet.md
    check: python docs/tools/checks/file-exists.py out/transcript-request-pack.md
    on_fail: retry
    next: []
```

Starter work map. Replace tools and checks when they correct this office (use **remember**).
