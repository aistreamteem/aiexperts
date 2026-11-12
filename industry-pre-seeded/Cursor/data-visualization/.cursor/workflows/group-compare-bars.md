# Group-compare bars

**When to use:** Group the measure they named by the category they named. Write the aggregated work CSV, a PNG bar chart, and a write-up. Sort by the rule they named. Zero baseline for counts and dollars. Colorblind palette. Do not invent a category or a winner stamp. Say n per bar when slices are small. If seaborn is missing, matplotlib bars are fine; ask rather than fake a file.

**Initial phase:** `question`

**Method:** `docs/role/work-item-method.md` — comparison charts.

## How to run

This file is self-contained. Walk it with **continue** / **journal-keeper**.

1. Confirm an active Work Item under `work-items/<id>/`. Paths below are **inside that folder**.
2. **Question gate:** they named the measure, the category, the aggregation, and the sort rule. Stop and ask if not.
3. Put the source file in `in/`. Load `docs/tools/pandas.md` and `docs/tools/seaborn.md` (or `docs/tools/matplotlib.md`). Load operations facts/rules (bar chart, zero baseline, colorblind, sort order).
4. Do one ready step per continue unless they asked for the whole job.
5. For each step: produce the file, run the check from the Work Item folder, log under `evidence/`. Retry at most three times, then ask.
6. **journal-keeper** after the step.

## Work map

```yaml
id: group-compare-bars
steps:
  - id: agg
    needs: []
    produces: agg
    produce_path: work/group-compare.csv
    tool: docs/tools/pandas.md
    check: python docs/tools/checks/csv-has-columns.py work/group-compare.csv group value
    on_fail: retry
    next: [chart]
  - id: chart
    needs: [agg]
    produces: png
    produce_path: out/group-compare-bars.png
    tool: docs/tools/seaborn.md
    check: python docs/tools/checks/file-exists.py out/group-compare-bars.png
    on_fail: retry
    next: [pack]
  - id: pack
    needs: [png]
    produces: writeup
    produce_path: out/group-compare-bars.md
    tool: docs/tools/chart-output-folder.md
    check: python docs/tools/checks/file-exists.py out/group-compare-bars.md
    on_fail: retry
    next: []
```

Starter work map. Replace tools and checks when they teach *this* shop’s compare order.
