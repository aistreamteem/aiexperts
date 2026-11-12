# Seasonal Calendar

**When to use:** List upcoming seasonal extras from their calendar and match properties that already have tickets. Do not invent a leaf week or an aeration window from climate memory. Chemical rounds stay labels, not a mix. After they call weather, note slides they wrote. Start-up week uses this pack plus the height file questions. They choose to pull a week forward. You do not declare the season open.

**How to run:** Open or continue a Work Item under `work-items/<id>/`. Follow this file's steps in order. Read the cited tool doc, write artifacts under that Work Item's `work/` and `out/`, run the listed check against those same paths, then **journal-keeper**. Do not invent a missing ticket, price, or weather call — ask with **operator-qa**.

**Initial phase:** `role-job`

## Work map

```yaml
id: seasonal-calendar
steps:
  - id: cal
    needs: []
    produces: calendar
    produce_path: work/seasonal-calendar.csv
    tool: docs/tools/seasonal-calendar.md
    check: python docs/tools/checks/file-exists.py work/seasonal-calendar.csv
    on_fail: retry
    next: [tickets]
  - id: tickets
    needs: [calendar]
    produces: tickets
    produce_path: work/seasonal-tickets.csv
    tool: docs/tools/job-ticket-sheet.md
    check: python docs/tools/checks/file-exists.py work/seasonal-tickets.csv
    on_fail: retry
    next: [pack]
  - id: pack
    needs: [calendar, tickets]
    produces: season-pack
    produce_path: out/seasonal-calendar.md
    tool: docs/tools/spreadsheet.md
    check: python docs/tools/checks/file-exists.py out/seasonal-calendar.md
    on_fail: retry
    next: []
```

Starter work map. Replace tools and checks when they correct shop practice (**remember** / **integrate-docs**).
