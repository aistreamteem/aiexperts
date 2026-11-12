# Weigh-ticket pack

**When to use:** Index scale slips they stored: tare, gross, net, unit, date. Never invent a pound. Say which slip is missing if only one side is present. If a survey weight disagrees, list both and keep the ticket as the weight field when their rule says ticket wins. They send the truck back to the scale if needed. You pack slips, the job row, and questions. No DOT weighing opinion.

**How to run:** Open or continue a Work Item under `work-items/<id>/`. Put source files in `in/`. Walk one ready YAML step (or the whole named job if requested): read the named tool, produce the file, run the check, then **journal-keeper**. Do not invent weight, cube, rates, crew names, or delivery hours.

**Initial phase:** `role-job`

## Work map

```yaml
id: weigh-ticket-pack
steps:
  - id: tickets
    needs: []
    produces: tickets
    produce_path: work/weigh-tickets.md
    tool: docs/tools/weigh-ticket-folder.md
    check: python docs/tools/checks/file-exists.py work/weigh-tickets.md
    on_fail: retry
    next: [jobs]
  - id: jobs
    needs: [tickets]
    produces: jobs
    produce_path: work/jobs.csv
    tool: docs/tools/spreadsheet.md
    check: python docs/tools/checks/csv-has-columns.py work/jobs.csv job date
    on_fail: retry
    next: [pack]
  - id: pack
    needs: [tickets, jobs]
    produces: weigh-pack
    produce_path: out/weigh-ticket-pack.md
    tool: docs/tools/spreadsheet.md
    check: python docs/tools/checks/file-exists.py out/weigh-ticket-pack.md
    on_fail: retry
    next: []
```

Starter work map. Replace tools and checks when the operator corrects this shop.
