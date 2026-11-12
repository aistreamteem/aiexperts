# Stale And Waste

**When to use:** Recap their waste and stale logs for the dates they named, next to case par if they asked why the case overbaked. Do not invent waste or stales. Do not hide stales inside a par cut. Do not relabel as donation. Do not write theft. Patterns are questions for mix or par. The pack is the recap plus asks. They change the plan.

**How to run:** Self-contained. Active Work Item under `work-items/<id>/`. For each ready step: read the tool doc → write `produce_path` inside that Work Item → run the check with working directory = the Work Item folder → journal-keeper.

**Initial phase:** `logs`

## Work map

```yaml
id: stale-and-waste
steps:
  - id: logs
    needs: []
    produces: logs
    produce_path: work/waste-stales.csv
    tool: docs/tools/spreadsheet.md
    check: python docs/tools/checks/file-exists.py work/waste-stales.csv
    on_fail: retry
    next: [pars]
  - id: pars
    needs: [logs]
    produces: case-par
    produce_path: work/case-par.csv
    tool: docs/tools/case-par-sheet.md
    check: python docs/tools/checks/file-exists.py work/case-par.csv
    on_fail: retry
    next: [pack]
  - id: pack
    needs: [logs, case-par]
    produces: stale-pack
    produce_path: out/stale-and-waste.md
    tool: docs/tools/spreadsheet.md
    check: python docs/tools/checks/file-exists.py out/stale-and-waste.md
    on_fail: retry
    next: []
```

Starter work map. Replace tools and checks when the operator confirms how this shop files (`remember` / `integrate-docs`).
