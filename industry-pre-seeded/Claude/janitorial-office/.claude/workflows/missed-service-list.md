# Missed Service List

**When to use:** List schedule rows they coded as missed and any complaint rows that point at a miss. Keep misses visible. Do not invent a make-up night or a credit. Holiday skips already on the calendar are not misses. Write-up is the miss list plus missing-reason asks. They call the customer. You do not hide a lock-out to protect a score. Night-supervisor notes stay attached only if they already stored them.

**How to run:** Use **continue** with this workflow. Work inside `work-items/<id>/`. For each step: read the tool doc, produce the file, run the check (retry at most 3, then ask), then **journal-keeper**. Do not invent a make-up night or hide a miss.

**Initial phase:** `schedule`

## Work map

```yaml
id: missed-service-list
steps:
  - id: schedule
    needs: []
    produces: schedule
    produce_path: work/miss-schedule.csv
    tool: docs/tools/schedule-csv.md
    check: python docs/tools/checks/csv-has-columns.py work/miss-schedule.csv site date
    on_fail: retry
    next: [log]
  - id: log
    needs: [schedule]
    produces: log
    produce_path: work/miss-complaints.csv
    tool: docs/tools/complaint-log.md
    check: python docs/tools/checks/file-exists.py work/miss-complaints.csv
    on_fail: retry
    next: [pack]
  - id: pack
    needs: [schedule, log]
    produces: miss-pack
    produce_path: out/missed-service.md
    tool: docs/tools/spreadsheet.md
    check: python docs/tools/checks/file-exists.py out/missed-service.md
    on_fail: retry
    next: []
```

Starter map. Replace tools and checks when the operator corrects this shop (**remember**).
