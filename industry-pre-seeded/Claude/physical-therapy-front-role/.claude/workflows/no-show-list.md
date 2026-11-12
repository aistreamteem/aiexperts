# No Show List

**When to use:** From the schedule or EHR export, list rows they already coded no-show, late cancel, or broken. Do not infer a no-show from a blank confirmation. Do not invent a fee or a discharge. Keep their status words. One clinic date unless they asked for a range and the file has dates. Prefer chart number. They decide who is offered a wait-list fill. You do not diagnose why the patient missed and you do not treat the miss as clinical progress.

**How to run:** Open or switch to a Work Item under `work-items/<id>/`. Follow this YAML with **continue** (one ready step, or the whole named job if requested). Read the named `docs/tools/` file. Write artifacts under this Work Item. Run each step’s check. **journal-keeper** after the step.

**Initial phase:** `role-job`

## Work map

```yaml
id: no-show-list
steps:
  - id: pull
    needs: []
    produces: day
    produce_path: work/day-list.csv
    tool: docs/tools/ehr-export.md
    check: python docs/tools/checks/file-exists.py work/day-list.csv
    on_fail: retry
    next: [columns]
  - id: columns
    needs: [day]
    produces: day-cols
    produce_path: work/day-list.csv
    tool: docs/tools/ehr-export.md
    check: python docs/tools/checks/csv-has-columns.py work/day-list.csv chart status
    on_fail: retry
    next: [write]
  - id: write
    needs: [day-cols]
    produces: ns-writeup
    produce_path: out/no-shows.md
    tool: docs/tools/spreadsheet.md
    check: python docs/tools/checks/file-exists.py out/no-shows.md
    on_fail: retry
    next: []
```

Starter work map. Replace tools and checks when they correct this clinic.
