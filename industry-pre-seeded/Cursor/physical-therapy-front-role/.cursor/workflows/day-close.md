# Day-close tender

**When to use:** From their close report or drawer sheet, list tender types and amounts they recorded for one clinic date. Do not store PAN or check account numbers. Do not send a deposit or mark a bill paid. Short-or-over versus their expected total is a flag from their math, not a silent fix. Copay posted amounts, if compared, come from their posted sheet — do not invent expected collect. Insurance posting is not tender. One location unless they asked. Remaining visits do not belong in the cash total.

**How to run:** Open or reuse `work-items/<id>/`. Put source files in `in/`. Follow this map in order: read the named `docs/tools/` file, write `produce_path` inside this Work Item, run the step `check`, retry at most 3 times on fail then ask. Pass produced files to the next step. One ready step per continue unless the operator asked for the whole job. Then journal-keeper.

**Initial phase:** `role-job`

## Work map

```yaml
id: day-close
steps:
  - id: close
    needs: []
    produces: close
    produce_path: work/day-close.csv
    tool: docs/tools/ehr-export.md
    check: python docs/tools/checks/file-exists.py work/day-close.csv
    on_fail: retry
    next: [copay]
  - id: copay
    needs: [close]
    produces: copay
    produce_path: work/posted-copay.csv
    tool: docs/tools/fee-posted.md
    check: python docs/tools/checks/file-exists.py work/posted-copay.csv
    on_fail: retry
    next: [write]
  - id: write
    needs: [close, copay]
    produces: close-writeup
    produce_path: out/day-close.md
    tool: docs/tools/spreadsheet.md
    check: python docs/tools/checks/file-exists.py out/day-close.md
    on_fail: retry
    next: []
```

Starter work map. Replace tools and checks when the operator confirms how this clinic works.
