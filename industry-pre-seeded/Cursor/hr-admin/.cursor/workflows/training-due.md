# Training due

**When to use:** Read their training log. List people with a due or refresh date on or before the pack date they asked for, plus rows with a blank completed date for a course they already assigned. Do not invent a required course from a remembered safety list. Do not mark complete without their date. Certificates are present-or-missing flags. No LMS password. Write the due list and a pack summary under `out/`. They assign and they chase. Expired refresh dates stay visible.

## How to run

1. Open or switch to one Work Item under `work-items/<id>/` (`workflow-selector` if the job is not selected yet). Put source files in that item's `in/`.
2. Follow this file's YAML: one ready step per **continue**, or the whole named job if the operator requested it. Read the named `docs/tools/` doc. Write `produce_path` under this Work Item. Run the step `check`. Retry at most three times, then ask.
3. Run **journal-keeper** after the step (or job) completes.

**Initial phase:** `role-job`

## Work map

```yaml
id: training-due
steps:
  - id: log
    needs: []
    produces: train
    produce_path: work/training-log.csv
    tool: docs/tools/training-log.md
    check: python docs/tools/checks/csv-has-columns.py work/training-log.csv name due_date
    on_fail: retry
    next: [pack]
  - id: pack
    needs: [train]
    produces: train-pack
    produce_path: out/training-due.md
    tool: docs/tools/spreadsheet.md
    check: python docs/tools/checks/file-exists.py out/training-due.md
    on_fail: retry
    next: []
```

Starter work map. Replace tools and checks when they correct this shop.
