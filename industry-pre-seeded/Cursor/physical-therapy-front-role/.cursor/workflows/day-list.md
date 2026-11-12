# Day list

**When to use:** From the schedule export, list the day by time, therapist, type, and their patient label. Keep closed blocks, lunch, and documentation rows. Flag emergency wording for staff. No treatment notes and no diagnosis from the reason field. One clinic date and one location unless they asked for a multi-day book and the file has a date column. Flag overlaps that their double-book rule does not allow. Prefer chart or MRN. Confirm the export date before you treat it as tomorrow. Do not invent remaining visits on the huddle list.

**How to run:** Open or reuse `work-items/<id>/`. Put source files in `in/`. Follow this map in order: read the named `docs/tools/` file, write `produce_path` inside this Work Item, run the step `check`, retry at most 3 times on fail then ask. Pass produced files to the next step. One ready step per continue unless the operator asked for the whole job. Then journal-keeper.

**Initial phase:** `role-job`

## Work map

```yaml
id: day-list
steps:
  - id: pull
    needs: []
    produces: sched
    produce_path: work/day-list.csv
    tool: docs/tools/schedule-csv.md
    check: python docs/tools/checks/file-exists.py work/day-list.csv
    on_fail: retry
    next: [blocks]
  - id: blocks
    needs: [sched]
    produces: blocks
    produce_path: work/blocks.csv
    tool: docs/tools/calendar.md
    check: python docs/tools/checks/file-exists.py work/blocks.csv
    on_fail: retry
    next: [write]
  - id: write
    needs: [sched, blocks]
    produces: day-writeup
    produce_path: out/day-list.md
    tool: docs/tools/spreadsheet.md
    check: python docs/tools/checks/file-exists.py out/day-list.md
    on_fail: retry
    next: []
```

Starter work map. Replace tools and checks when the operator confirms how this clinic works.
