# Due Today

**When to use:** List tickets due today or overdue from the ticket sheet, then read each due against the press calendar. Flag infeasible dates. Never invent a due the iron cannot meet. Do not bump other jobs unless their rush rule is in the folder and they asked. Proof still out stays called out. The pack is a due list with calendar conflicts, not a new promise to the customer.

**How to run:** Open or continue a Work Item under `work-items/<id>/`. Put source files in `in/`. Walk one ready YAML step (or the whole named job if requested): produce the file, run the check, then **journal-keeper**.

**Initial phase:** isolate / intake

## Work map

```yaml
id: due-today
steps:
  - id: cal
    needs: []
    produces: calendar
    produce_path: work/press-calendar.csv
    tool: docs/tools/press-calendar.md
    check: python docs/tools/checks/file-exists.py work/press-calendar.csv
    on_fail: retry
    next: [tickets]
  - id: tickets
    needs: [calendar]
    produces: tickets
    produce_path: work/job-tickets.csv
    tool: docs/tools/job-ticket-sheet.md
    check: python docs/tools/checks/csv-has-columns.py work/job-tickets.csv job qty due
    on_fail: retry
    next: [pack]
  - id: pack
    needs: [calendar, tickets]
    produces: due-pack
    produce_path: out/due-today.md
    tool: docs/tools/press-calendar.md
    check: python docs/tools/checks/file-exists.py out/due-today.md
    on_fail: retry
    next: []
```

Starter work map. Replace tools and checks when they **remember** a correction for this shop.
