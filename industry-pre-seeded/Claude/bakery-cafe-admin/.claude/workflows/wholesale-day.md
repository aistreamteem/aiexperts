# Wholesale Day

**When to use:** Build the pick list from standing filtered to the weekday on their calendar, plus dated extras or standing-changes they filed. Do not invent a crate qty or a delivery day. Keep cafe case off the crates unless they asked. Route stops copy the route sheet if they use one. The pack is the list plus 86-wholesale and qty fights. They pack and drive.

**How to run:** Self-contained. Active Work Item under `work-items/<id>/`. For each ready step: read the tool doc → write `produce_path` inside that Work Item → run the check with working directory = the Work Item folder → journal-keeper.

**Initial phase:** `standing`

## Work map

```yaml
id: wholesale-day
steps:
  - id: standing
    needs: []
    produces: standing
    produce_path: work/wholesale-standing.csv
    tool: docs/tools/wholesale-standing-csv.md
    check: python docs/tools/checks/csv-has-columns.py work/wholesale-standing.csv account qty
    on_fail: retry
    next: [cal]
  - id: cal
    needs: [standing]
    produces: cal
    produce_path: work/production-calendar.csv
    tool: docs/tools/calendar.md
    check: python docs/tools/checks/file-exists.py work/production-calendar.csv
    on_fail: retry
    next: [pack]
  - id: pack
    needs: [standing, cal]
    produces: wholesale-pack
    produce_path: out/wholesale-day.md
    tool: docs/tools/wholesale-standing-csv.md
    check: python docs/tools/checks/file-exists.py out/wholesale-day.md
    on_fail: retry
    next: []
```

Starter work map. Replace tools and checks when the operator confirms how this shop files (`remember` / `integrate-docs`).
