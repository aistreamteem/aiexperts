# Guest Pass Log

**When to use:** Build the guest-pass log from check-ins plus the membership export for host rows if their file requires a host. Waiver present stays a join to the waiver folder when they asked. Do not invent a free pass or write a guest onto the member roster. Produce the log plus a pack note in `out/`. They sell the day pass. Starter until the operator corrects this club’s guest rules.

**How to run:** Open or reuse `work-items/<id>/` (workflow-selector if unset) → continue one ready YAML step (or the whole named job if requested) → journal-keeper. Paths `work/` and `out/` are inside that Work Item.

**Initial phase:** `intake`

## Work map

```yaml
id: guest-pass-log
steps:
  - id: checkins
    needs: []
    produces: checkins
    produce_path: work/check-in.csv
    tool: docs/tools/check-in-csv.md
    check: python docs/tools/checks/csv-has-columns.py work/check-in.csv member_id status
    on_fail: retry
    next: [members]
  - id: members
    needs: [checkins]
    produces: members
    produce_path: work/membership.csv
    tool: docs/tools/membership-export.md
    check: python docs/tools/checks/file-exists.py work/membership.csv
    on_fail: retry
    next: [pack]
  - id: pack
    needs: [checkins, members]
    produces: guest-pack
    produce_path: out/guest-pass-log.md
    tool: docs/tools/spreadsheet.md
    check: python docs/tools/checks/file-exists.py out/guest-pass-log.md
    on_fail: retry
    next: []
```

Starter work map. Replace tools and checks when the operator corrects this club.
