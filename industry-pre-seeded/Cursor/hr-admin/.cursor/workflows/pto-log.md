# PTO log

**When to use:** List balances and requests from their PTO sheet. Keep their column names for vacation, sick, or combined banks. Status stays as they coded it. You do not approve or deny. You do not invent remaining hours or an accrual rate. If balance is blank, ask or leave blank. Overlaps are flags they resolve. Write the log and a pack summary under `out/`. Holiday calendars stay a separate file unless they already rolled hours in.

## How to run

1. Open or switch to one Work Item under `work-items/<id>/` (`workflow-selector` if the job is not selected yet). Put source files in that item's `in/`.
2. Follow this file's YAML: one ready step per **continue**, or the whole named job if the operator requested it. Read the named `docs/tools/` doc. Write `produce_path` under this Work Item. Run the step `check`. Retry at most three times, then ask.
3. Run **journal-keeper** after the step (or job) completes.

**Initial phase:** `role-job`

## Work map

```yaml
id: pto-log
steps:
  - id: pto
    needs: []
    produces: pto
    produce_path: work/pto.csv
    tool: docs/tools/pto-sheet.md
    check: python docs/tools/checks/csv-has-columns.py work/pto.csv name
    on_fail: retry
    next: [pack]
  - id: pack
    needs: [pto]
    produces: pto-pack
    produce_path: out/pto-log.md
    tool: docs/tools/spreadsheet.md
    check: python docs/tools/checks/file-exists.py out/pto-log.md
    on_fail: retry
    next: []
```

Starter work map. Replace tools and checks when they correct this shop.
