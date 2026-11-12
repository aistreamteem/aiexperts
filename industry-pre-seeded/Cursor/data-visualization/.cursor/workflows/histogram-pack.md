# Histogram pack

**When to use:** From the numeric column they named, write a work CSV of the plotted values, a PNG histogram, and a write-up. Bin width is an ask or a stated default — do not hunt bins for a story. Say n, units, missing count, and what was not claimed. If matplotlib or seaborn is missing, ask and install; do not fake a PNG. Outliers stay unless they asked to list them aside.

**Initial phase:** `question`

**Method:** `docs/role/work-item-method.md` — distribution charts.

## How to run

This file is self-contained. Walk it with **continue** / **journal-keeper**.

1. Confirm an active Work Item under `work-items/<id>/`. Paths below are **inside that folder**.
2. **Question gate:** they named the numeric column. Bin width is an ask or a stated default written in the pack. Stop and ask if the column is missing.
3. Put the source file in `in/`. Load `docs/tools/pandas.md` and `docs/tools/matplotlib.md`.
4. Do one ready step per continue unless they asked for the whole job.
5. For each step: produce the file, run the check from the Work Item folder, log under `evidence/`. Retry at most three times, then ask.
6. **journal-keeper** after the step.

## Work map

```yaml
id: histogram-pack
steps:
  - id: values
    needs: []
    produces: values
    produce_path: work/histogram-values.csv
    tool: docs/tools/pandas.md
    check: python docs/tools/checks/csv-has-columns.py work/histogram-values.csv value
    on_fail: retry
    next: [chart]
  - id: chart
    needs: [values]
    produces: png
    produce_path: out/histogram.png
    tool: docs/tools/matplotlib.md
    check: python docs/tools/checks/file-exists.py out/histogram.png
    on_fail: retry
    next: [pack]
  - id: pack
    needs: [png]
    produces: writeup
    produce_path: out/histogram-pack.md
    tool: docs/tools/chart-output-folder.md
    check: python docs/tools/checks/file-exists.py out/histogram-pack.md
    on_fail: retry
    next: []
```

Starter work map. Replace tools and checks when they teach.
