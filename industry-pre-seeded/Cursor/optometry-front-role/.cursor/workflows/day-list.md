# Day list

**When to use:** From the schedule export, list the day by time, doctor, type, and their patient label. Keep closed blocks, lunch, huddle, and optical-only rows. Flag dilation and contact-training flags as stored. Flag emergency wording for staff. No clinical notes, no diagnosis from the reason field, and no Rx interpretation. One clinic date and one location unless they asked for a multi-day book and the file has a date column. Prefer chart or account number. Confirm the export date before you treat it as tomorrow. This is an optometry book, not a dental chair sheet.

**How to run:** Select this job with **workflow-selector** (or name it). Keep artifacts under `work-items/<id>/`. Walk one ready step per **continue** unless they asked for the whole job. For each step: read the tool file, write `produce_path` inside the Work Item folder, run the check against that same path, store the log in `evidence/`, then **journal-keeper**. Do not start a step if its `needs` files are missing. On check fail, retry at most 3 times, then ask. If a required export is missing, ask; do not invent rows.

**Initial phase:** `intake`, then the first YAML step. Paths `work/` and `out/` mean inside the current Work Item.

## Work map

```yaml
id: day-list
steps:
  - id: pull
    needs: []
    produces: sched
    produce_path: work/day-list.csv
    tool: docs/tools/day-list-csv.md
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

Starter work map. Replace tools and checks when the operator confirms how this office works via **remember**.
