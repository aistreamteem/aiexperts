# Wait List

**When to use:** From their wait-list file, keep their order and requested type and doctor. Match open or cancelled slots from the day list or calendar only as listed options. They choose who is offered. You do not message patients and you do not invent that someone was reached. Emergency wording flags staff and is not a diagnosis. Extra phones the send-list does not need stay out of the pack note. Prefer chart number. Exam types and optical types stay as stored. Do not reorder to favor a vision plan or a frame sale.

**How to run:** Select this job with **workflow-selector** (or name it). Keep artifacts under `work-items/<id>/`. Walk one ready step per **continue** unless they asked for the whole job. For each step: read the tool file, write `produce_path` inside the Work Item folder, run the check against that same path, store the log in `evidence/`, then **journal-keeper**. Do not start a step if its `needs` files are missing. On check fail, retry at most 3 times, then ask. If a required export is missing, ask; do not invent rows.

**Initial phase:** `intake`, then the first YAML step. Paths `work/` and `out/` mean inside the current Work Item.

## Work map

```yaml
id: wait-list
steps:
  - id: wait
    needs: []
    produces: wait
    produce_path: work/wait-list.csv
    tool: docs/tools/wait-list.md
    check: python docs/tools/checks/csv-has-columns.py work/wait-list.csv chart type
    on_fail: retry
    next: [slots]
  - id: slots
    needs: [wait]
    produces: slots
    produce_path: work/day-list.csv
    tool: docs/tools/day-list-csv.md
    check: python docs/tools/checks/file-exists.py work/day-list.csv
    on_fail: retry
    next: [write]
  - id: write
    needs: [wait, slots]
    produces: wait-writeup
    produce_path: out/wait-list.md
    tool: docs/tools/spreadsheet.md
    check: python docs/tools/checks/file-exists.py out/wait-list.md
    on_fail: retry
    next: []
```

Starter work map. Replace tools and checks when they correct this office via **remember**.
