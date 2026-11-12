# Describe a CSV they dropped

**When to use:** Load the CSV they named with pandas. Write a summary CSV of count, missing, min, max, and mean for numeric columns they named. The write-up states the question, the source file name, the columns, any filters, and that no cause was claimed. Do not invent a column. Do not impute. If pandas is missing, ask and stop; do not fake a summary. They read the pack; you do not call it a census of the shop.

**Initial phase:** `question`

**Method:** `docs/role/work-item-method.md` — this job covers profile + pack (and intake). Default registry job.

## How to run

This file is self-contained. Walk it with **continue** / **journal-keeper**. Use **operator-qa** if the question or columns are missing.

1. Confirm an active Work Item under `work-items/<id>/` (**workflow-selector** if none). Paths below are **inside that folder**.
2. **Question gate:** they named the question and the columns (or “all numeric columns they named”). Stop and ask if not.
3. Put the source file in `in/`. Load `docs/tools/csv-folder.md` and `docs/tools/pandas.md`. Load operations facts/rules.
4. Do one ready step per continue unless they asked for the whole job.
5. For each step: produce the file, run the check from the Work Item folder, capture the log under `evidence/`. Retry at most three times, then ask. Do not invent a pass.
6. **journal-keeper** after the step.

## Work map

```yaml
id: describe-csv
steps:
  - id: load
    needs: []
    produces: source
    produce_path: work/describe-source.csv
    tool: docs/tools/csv-folder.md
    check: python docs/tools/checks/file-exists.py work/describe-source.csv
    on_fail: retry
    next: [summary]
  - id: summary
    needs: [source]
    produces: summary
    produce_path: work/describe-summary.csv
    tool: docs/tools/pandas.md
    check: python docs/tools/checks/csv-has-columns.py work/describe-summary.csv column count missing min max mean
    on_fail: retry
    next: [pack]
  - id: pack
    needs: [summary]
    produces: writeup
    produce_path: out/describe-csv.md
    tool: docs/tools/python.md
    check: python docs/tools/checks/file-exists.py out/describe-csv.md
    on_fail: retry
    next: []
```

Starter work map. Replace tools and checks when they teach how *this* shop exports.
