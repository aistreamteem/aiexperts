# Showing Week

**When to use:** Build the week's tours from their calendar or availability sheet: vacant units, windows, asking rent they set, and any occupied row that is missing a notice log. No steering copy and no invented comps. Do not promise an application will be approved. Do not paste lockbox codes onto the week sheet. If they ask to describe who should apply, refuse. They run the tours; this pack is the schedule plus gaps.

**How to run:** Open or continue a Work Item under `work-items/<id>/`. Put source files in `in/`. Walk one ready YAML step (or the whole named job if requested): produce the file, run the check, then **journal-keeper**. Paths `work/` and `out/` are inside that Work Item.

**Initial phase:** `role-job`

## Work map

```yaml
id: showing-week
steps:
  - id: cal
    needs: []
    produces: show-raw
    produce_path: work/showings-raw.csv
    tool: docs/tools/calendar.md
    check: python docs/tools/checks/file-exists.py work/showings-raw.csv
    on_fail: retry
    next: [units]
  - id: units
    needs: [show-raw]
    produces: show-units
    produce_path: work/showings-units.csv
    tool: docs/tools/showing-sheet.md
    check: python docs/tools/checks/csv-has-columns.py work/showings-units.csv unit window
    on_fail: retry
    next: [show-pack]
  - id: show-pack
    needs: [show-units]
    produces: show-writeup
    produce_path: out/showings.md
    tool: docs/tools/showing-sheet.md
    check: python docs/tools/checks/file-exists.py out/showings.md
    on_fail: retry
    next: []
```

Starter work map. Replace tools and checks when they correct this shop (use **remember**).
