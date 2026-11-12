# Day List

**When to use:** From the schedule export, list the day by time, chair, provider, and their patient label. Flag emergency wording for staff. No clinical notes and no diagnosis from the reason field. One clinic date and one location unless they asked for a multi-day book and the file has a date column. Keep closed blocks, lunch, and huddle rows. Flag overlaps; do not move chairs or providers to hide them. Prefer chart number. Confirm the export date before you treat it as tomorrow.

**How to run:** Open or reuse `work-items/<id>/`. Put the schedule export in `in/`. Follow this map in order: read the named `docs/tools/` file, write `produce_path` inside this Work Item, run the step `check`, retry at most 3 times on fail then ask. Pass produced files to the next step. One ready step per continue unless the operator asked for the whole job. Then journal-keeper.

**Initial phase:** `role-job`

## Work map

```yaml
id: day-list
steps:
  - id: pull
    needs: []
    produces: sched
    produce_path: work/schedule.csv
    tool: docs/tools/day-sheet-export.md
    check: python docs/tools/checks/file-exists.py work/schedule.csv
    on_fail: retry
    next: [columns]
  - id: columns
    needs: [sched]
    produces: sched-cols
    produce_path: work/schedule.csv
    tool: docs/tools/day-sheet-export.md
    check: python docs/tools/checks/csv-has-columns.py work/schedule.csv time provider
    on_fail: retry
    next: [write]
  - id: write
    needs: [sched-cols]
    produces: day-writeup
    produce_path: out/day-list.md
    tool: docs/tools/pms-export.md
    check: python docs/tools/checks/file-exists.py out/day-list.md
    on_fail: retry
    next: []
```

Starter work map. Replace tools and checks when the operator confirms how this office works.
