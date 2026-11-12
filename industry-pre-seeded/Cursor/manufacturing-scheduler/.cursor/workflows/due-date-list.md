# Due Date List

**When to use:** Sort open work orders by due date from their export and flag lines that fall on a closed calendar day or that already miss the printed due. Do not invent a promise. Do not overwrite due with a late finish to make aging look on time. Shortages and outside promises that make a due infeasible stay named. Original versus current due both appear if the export has them. They slip dates.

**How to run:** Create or continue a Work Item under `work-items/<id>/` (use **workflow-selector** if the job is not yet chosen). Put source files in `in/`. Walk this file's YAML map one ready step at a time unless the operator asked for the whole named job: read the cited `docs/tools/` file, write `produce_path` inside this Work Item (`work/` and `out/` are relative to it), run the check from the Work Item folder, copy check logs to `evidence/`, then **journal-keeper**. Do not start a step whose `needs` files are missing. On check fail, retry at most three times from the tool doc, then record the blocker and ask. When the last step passes, write the pack into `out/` quoting export dates; do not treat chat as the deliverable.

**Initial phase:** `intake`

## Work map

```yaml
id: due-date-list
steps:
  - id: wo
    needs: []
    produces: wos
    produce_path: work/work-orders.csv
    tool: docs/tools/wo-export.md
    check: python docs/tools/checks/csv-has-columns.py work/work-orders.csv wo item qty
    on_fail: retry
    next: [cal]
  - id: cal
    needs: [wos]
    produces: cal
    produce_path: work/calendar.csv
    tool: docs/tools/calendar-file.md
    check: python docs/tools/checks/file-exists.py work/calendar.csv
    on_fail: retry
    next: [pack]
  - id: pack
    needs: [wos, cal]
    produces: due-pack
    produce_path: out/due-dates.md
    tool: docs/tools/spreadsheet.md
    check: python docs/tools/checks/file-exists.py out/due-dates.md
    on_fail: retry
    next: []
```

Starter work map. Replace tools and checks when the operator corrects how *this* shop works.
