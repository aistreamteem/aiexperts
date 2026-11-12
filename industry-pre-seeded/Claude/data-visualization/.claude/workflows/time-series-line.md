# Time-series line

**When to use:** Parse the date column they named, apply the date range they named, aggregate to the grain they named, and write a work series CSV plus a PNG line. Gaps stay gaps unless they said how to treat closed days. Do not extend the line as a forecast. Rolling mean only if they asked, labeled as history. Timezone and week-start: ask if missing. Name the source file in the write-up.

**Initial phase:** `question`

**Method:** `docs/role/work-item-method.md` — change-over-time charts.

## How to run

This file is self-contained. Walk it with **continue** / **journal-keeper**.

1. Confirm an active Work Item under `work-items/<id>/`. Paths below are **inside that folder**.
2. **Question gate:** they named the date column, the measure, the range, and the grain. Timezone and week-start: ask if the file does not say. Do not forecast.
3. Put the source file in `in/`. Load `docs/tools/pandas.md` and `docs/tools/matplotlib.md`.
4. Do one ready step per continue unless they asked for the whole job.
5. For each step: produce the file, run the check from the Work Item folder, log under `evidence/`. Retry at most three times, then ask.
6. **journal-keeper** after the step.

## Work map

```yaml
id: time-series-line
steps:
  - id: series
    needs: []
    produces: series
    produce_path: work/timeseries.csv
    tool: docs/tools/pandas.md
    check: python docs/tools/checks/csv-has-columns.py work/timeseries.csv date value
    on_fail: retry
    next: [chart]
  - id: chart
    needs: [series]
    produces: png
    produce_path: out/timeseries-line.png
    tool: docs/tools/matplotlib.md
    check: python docs/tools/checks/file-exists.py out/timeseries-line.png
    on_fail: retry
    next: [pack]
  - id: pack
    needs: [png]
    produces: writeup
    produce_path: out/timeseries-line.md
    tool: docs/tools/python.md
    check: python docs/tools/checks/file-exists.py out/timeseries-line.md
    on_fail: retry
    next: []
```

Starter work map. Replace tools and checks when they teach.
