# Showing Day

**When to use:** Read the showing calendar and the availability sheet, then list today's tours with unit or floorplan as booked. Flag slots that sit outside posted hours only if you already have the hours file in another pack; here, still do not invent a unit. Do not promise the home will stay vacant. No-shows stay no-shows. They walk the halls; you do not hand keys.

**How to run:** Open or continue a Work Item under `work-items/<id>/`. Put the showing calendar and availability sheet in `in/`. Read this file and the named tool docs. Walk one ready YAML step (or the whole job if requested): produce the file under this Work Item’s `work/` or `out/`, run the check, then journal-keeper. Do not skip a step with a chat summary.

**Initial phase:** `role-job`

## Work map

```yaml
id: showing-day
steps:
  - id: calendar
    needs: []
    produces: calendar
    produce_path: work/showings.csv
    tool: docs/tools/showing-calendar.md
    check: python docs/tools/checks/csv-has-columns.py work/showings.csv date unit prospect
    on_fail: retry
    next: [avail]
  - id: avail
    needs: [calendar]
    produces: avail
    produce_path: work/availability.csv
    tool: docs/tools/availability-sheet.md
    check: python docs/tools/checks/csv-has-columns.py work/availability.csv unit status
    on_fail: retry
    next: [pack]
  - id: pack
    needs: [calendar, avail]
    produces: showing-pack
    produce_path: out/showing-list.md
    tool: docs/tools/showing-calendar.md
    check: python docs/tools/checks/file-exists.py out/showing-list.md
    on_fail: retry
    next: []
```

Starter work map. Replace tools and checks when the operator corrects this shop (remember / integrate-docs).
