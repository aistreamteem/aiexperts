# Missing report and outlier list

**When to use:** Write a missing-count CSV for the columns they named and an outlier-list CSV using the fence or threshold they named. The write-up lists source file, n, the rule, and that listed points were not deleted unless they asked. Do not impute. Do not call a point an error without their file. If numpy is missing and they wanted a numeric fence, ask; do not invent rows.

**Initial phase:** `question`

**Method:** `docs/role/work-item-method.md` — profile / quality lists.

## How to run

This file is self-contained. Walk it with **continue** / **journal-keeper**.

1. Confirm an active Work Item under `work-items/<id>/`. Paths below are **inside that folder**.
2. **Question gate:** they named the columns and the outlier fence or threshold. Stop and ask if the fence is missing; do not invent IQR vs a shop rule.
3. Put the source file in `in/`. Load `docs/tools/pandas.md` and `docs/tools/numpy.md`. Do not impute.
4. Do one ready step per continue unless they asked for the whole job.
5. For each step: produce the file, run the check from the Work Item folder, log under `evidence/`. Retry at most three times, then ask.
6. **journal-keeper** after the step.

## Work map

```yaml
id: missing-and-outliers
steps:
  - id: missing
    needs: []
    produces: missing
    produce_path: work/missing-report.csv
    tool: docs/tools/pandas.md
    check: python docs/tools/checks/csv-has-columns.py work/missing-report.csv column count missing
    on_fail: retry
    next: [outliers]
  - id: outliers
    needs: [missing]
    produces: outliers
    produce_path: work/outlier-list.csv
    tool: docs/tools/numpy.md
    check: python docs/tools/checks/file-exists.py work/outlier-list.csv
    on_fail: retry
    next: [pack]
  - id: pack
    needs: [missing, outliers]
    produces: writeup
    produce_path: out/missing-and-outliers.md
    tool: docs/tools/python.md
    check: python docs/tools/checks/file-exists.py out/missing-and-outliers.md
    on_fail: retry
    next: []
```

Starter work map. Replace tools and checks when they teach.
