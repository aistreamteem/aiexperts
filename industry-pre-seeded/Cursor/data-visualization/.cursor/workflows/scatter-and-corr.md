# Scatter and descriptive correlation

**When to use:** Plot two numeric columns they named. Write the point CSV, a descriptive correlation number, a PNG scatter, and a write-up that says the number is not a cause. No fit line as policy. No PII point labels. Small n said. If scipy.stats is missing, pandas or numpy correlation is enough — ask rather than fake a p-value file. They decide what the association means.

**Initial phase:** `question`

**Method:** `docs/role/work-item-method.md` — relationship charts.

## How to run

This file is self-contained. Walk it with **continue** / **journal-keeper**.

1. Confirm an active Work Item under `work-items/<id>/`. Paths below are **inside that folder**.
2. **Question gate:** they named both numeric columns. Write association wording only; do not claim a cause.
3. Put the source file in `in/`. Load `docs/tools/pandas.md`, `docs/tools/scipy-stats.md`, and `docs/tools/matplotlib.md`.
4. Do one ready step per continue unless they asked for the whole job.
5. For each step: produce the file, run the check from the Work Item folder, log under `evidence/`. Retry at most three times, then ask.
6. **journal-keeper** after the step.

## Work map

```yaml
id: scatter-and-corr
steps:
  - id: points
    needs: []
    produces: points
    produce_path: work/scatter-points.csv
    tool: docs/tools/pandas.md
    check: python docs/tools/checks/csv-has-columns.py work/scatter-points.csv x y
    on_fail: retry
    next: [corr]
  - id: corr
    needs: [points]
    produces: corr
    produce_path: work/scatter-corr.csv
    tool: docs/tools/scipy-stats.md
    check: python docs/tools/checks/csv-has-columns.py work/scatter-corr.csv x y correlation
    on_fail: retry
    next: [chart]
  - id: chart
    needs: [corr]
    produces: png
    produce_path: out/scatter.png
    tool: docs/tools/matplotlib.md
    check: python docs/tools/checks/file-exists.py out/scatter.png
    on_fail: retry
    next: [pack]
  - id: pack
    needs: [png]
    produces: writeup
    produce_path: out/scatter-and-corr.md
    tool: docs/tools/python.md
    check: python docs/tools/checks/file-exists.py out/scatter-and-corr.md
    on_fail: retry
    next: []
```

Starter work map. Replace tools and checks when they teach.
