# Job Board

**When to use:** Build a board from their ticket sheet: job number, customer, qty, stock, proof status, due, press, and bindery as they coded them. Flag blank dues, missing proofs, and stock holes only when the matching file is in the pack. Do not invent a due the calendar cannot meet. Do not treat drafts as live. They run the floor from the board; you do not bump jobs. The pack names which columns came from the ticket versus a guess you labeled.

**How to run:** Open or continue a Work Item under `work-items/<id>/`. Put source files in `in/`. Walk one ready YAML step (or the whole named job if requested): produce the file, run the check, then **journal-keeper**.

**Initial phase:** isolate / intake

## Work map

```yaml
id: job-board
steps:
  - id: tickets
    needs: []
    produces: tickets
    produce_path: work/job-tickets.csv
    tool: docs/tools/job-ticket-sheet.md
    check: python docs/tools/checks/csv-has-columns.py work/job-tickets.csv job qty due
    on_fail: retry
    next: [board]
  - id: board
    needs: [tickets]
    produces: job-board
    produce_path: out/job-board.md
    tool: docs/tools/spreadsheet.md
    check: python docs/tools/checks/file-exists.py out/job-board.md
    on_fail: retry
    next: []
```

Starter work map. Replace tools and checks when they **remember** a correction for this shop.
