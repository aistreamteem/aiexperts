# Night Board

**When to use:** Build a night list from their site list, schedule CSV, and crew roster: site, shift, crew, area-split if they have one, and miss flags. Apply holiday skips only from their calendar if it is already in the folder; otherwise leave holiday as a question. Do not invent hours, wages, or a missing site. Never put alarm codes on the board. One site or area per row. They dispatch. You write the list and a short write-up the check can see.

**How to run:** Use **continue** with this workflow. Work inside `work-items/<id>/`. For each step: read the tool doc, produce the file, run the check (retry at most 3, then ask), then **journal-keeper**. Do not invent hours, wages, sites, or alarm codes.

**Initial phase:** `sites`

## Work map

```yaml
id: night-board
steps:
  - id: sites
    needs: []
    produces: sites
    produce_path: work/site-list.csv
    tool: docs/tools/site-list.md
    check: python docs/tools/checks/csv-has-columns.py work/site-list.csv site shift
    on_fail: retry
    next: [schedule]
  - id: schedule
    needs: [sites]
    produces: schedule
    produce_path: work/schedule.csv
    tool: docs/tools/schedule-csv.md
    check: python docs/tools/checks/csv-has-columns.py work/schedule.csv site date
    on_fail: retry
    next: [roster]
  - id: roster
    needs: [schedule]
    produces: roster
    produce_path: work/crew-roster.csv
    tool: docs/tools/crew-roster.md
    check: python docs/tools/checks/csv-has-columns.py work/crew-roster.csv name crew
    on_fail: retry
    next: [pack]
  - id: pack
    needs: [sites, schedule, roster]
    produces: night-board
    produce_path: out/night-board.md
    tool: docs/tools/spreadsheet.md
    check: python docs/tools/checks/file-exists.py out/night-board.md
    on_fail: retry
    next: []
```

Starter map. Replace tools and checks when the operator corrects this shop (**remember**).
