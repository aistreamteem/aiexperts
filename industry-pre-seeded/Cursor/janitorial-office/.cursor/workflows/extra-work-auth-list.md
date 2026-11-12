# Extra Work Auth List

**When to use:** Match add-on, extra-day, and project rows on the schedule to an auth PDF in the contract folder. Missing auth stays a hold. Do not invent a price. Do not treat a verbal as filed. Courtesy callbacks stay labeled if they coded them. Write-up is present versus missing auth plus which schedule rows wait. They collect signatures. You pack the list the check can see.

**How to run:** Use **continue** with this workflow. Work inside `work-items/<id>/`. For each step: read the tool doc, produce the file, run the check (retry at most 3, then ask), then **journal-keeper**. Missing auth stays a hold. Do not invent a price.

**Initial phase:** `schedule`

## Work map

```yaml
id: extra-work-auth-list
steps:
  - id: schedule
    needs: []
    produces: schedule
    produce_path: work/extra-schedule.csv
    tool: docs/tools/schedule-csv.md
    check: python docs/tools/checks/csv-has-columns.py work/extra-schedule.csv site date
    on_fail: retry
    next: [contracts]
  - id: contracts
    needs: [schedule]
    produces: auths
    produce_path: work/auth-index.csv
    tool: docs/tools/contract-pdf-folder.md
    check: python docs/tools/checks/file-exists.py work/auth-index.csv
    on_fail: retry
    next: [pack]
  - id: pack
    needs: [schedule, auths]
    produces: auth-pack
    produce_path: out/extra-work-auth.md
    tool: docs/tools/spreadsheet.md
    check: python docs/tools/checks/file-exists.py out/extra-work-auth.md
    on_fail: retry
    next: []
```

Starter map. Replace tools and checks when the operator corrects this shop (**remember**).
