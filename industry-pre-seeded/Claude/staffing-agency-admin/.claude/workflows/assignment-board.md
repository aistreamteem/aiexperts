# Assignment Board

**When to use:** Build a board from their assignment sheet, employee list, and calendar: person, client, shift, start, expected end, status, and DNS/unavailable filters they already coded. Do not invent a placement. Do not invent a start. Do not fire anyone. Rates stay pointers to the rate file, not guessed markups. Write the board CSV and a short pack. They dispatch. You list holes. SSNs stay out of the board.

**How to run:** Open or continue a Work Item under `work-items/<id>/`. Put assignment sheet, employee list, and calendar in `in/`. Read this file and `docs/tools/assignment-sheet.md` / `docs/tools/employee-list.md` / `docs/tools/spreadsheet.md`. Walk one ready YAML step (or the whole job if requested): produce the file under this Work Item’s `work/` or `out/`, run the check, then journal-keeper. Do not skip a step with a chat summary.

**Initial phase:** `role-job`

## Work map

```yaml
id: assignment-board
steps:
  - id: assign
    needs: []
    produces: assign
    produce_path: work/assignments.csv
    tool: docs/tools/assignment-sheet.md
    check: python docs/tools/checks/csv-has-columns.py work/assignments.csv employee client start
    on_fail: retry
    next: [people]
  - id: people
    needs: [assign]
    produces: people
    produce_path: work/employee-list.csv
    tool: docs/tools/employee-list.md
    check: python docs/tools/checks/csv-has-columns.py work/employee-list.csv name
    on_fail: retry
    next: [pack]
  - id: pack
    needs: [assign, people]
    produces: board
    produce_path: out/assignment-board.md
    tool: docs/tools/spreadsheet.md
    check: python docs/tools/checks/file-exists.py out/assignment-board.md
    on_fail: retry
    next: []
```

Starter work map. Replace tools and checks when they correct this shop.
