# Wait List

**When to use:** From their wait-list file, keep their order and requested type and therapist. Match open or cancelled slots from the day list only as listed options. They choose who is offered. You do not message patients and you do not invent that someone was reached. Emergency wording flags staff and is not a diagnosis. Extra phones the send-list does not need stay out of the pack. Prefer chart number. Cancel wait-fill still follows their order, not a jump you invent.

**How to run:** Open or switch to a Work Item under `work-items/<id>/`. Follow this YAML with **continue** (one ready step, or the whole named job if requested). Read the named `docs/tools/` file. Write artifacts under this Work Item. Run each step’s check. **journal-keeper** after the step.

**Initial phase:** `role-job`

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
    tool: docs/tools/schedule-csv.md
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

Starter work map. Replace tools and checks when they correct this clinic.
