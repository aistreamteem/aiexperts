# Week Schedule

**When to use:** Week view: crew PTO, overbook, sold installs without parts. Ask before moving a customer window. Join the board export to the tech calendar they provided. Two-person and weather-hold flags, if their SOP names them, are conflicts when the helper is off or the hold is live. Do not cancel a membership to fit a sold install without asking. Do not invent capacity policy. List each collision with job id and issue. Parts promise slips belong here as questions, not silent delays. Their headers win.

**How to run:** Open or continue a Work Item under `work-items/<id>/`. Walk one ready YAML step (or the whole named job if requested). Produce the file, run the check, then **journal-keeper**.

**Initial phase:** `role-job`

## Work map

```yaml
id: week-schedule
steps:
  - id: board
    needs: []
    produces: week-raw
    produce_path: work/week-board.csv
    tool: docs/tools/schedule-sheet.md
    check: python docs/tools/checks/file-exists.py work/week-board.csv
    on_fail: retry
    next: [conflicts]
  - id: conflicts
    needs: [week-raw]
    produces: week-conflicts
    produce_path: work/week-conflicts.csv
    tool: docs/tools/tech-calendar.md
    check: python docs/tools/checks/csv-has-columns.py work/week-conflicts.csv job issue
    on_fail: retry
    next: [week-pack]
  - id: week-pack
    needs: [week-conflicts]
    produces: week-writeup
    produce_path: out/week-board.md
    tool: docs/tools/schedule-sheet.md
    check: python docs/tools/checks/file-exists.py out/week-board.md
    on_fail: retry
    next: []
```

Starter work map. Replace tools and checks when they correct this shop (**remember**).
