# Violations

**When to use:** From their log or export, list open items, lots, categories they use, status against their adopted notice steps, and missing photos or blank lots. Produce the CSV the checks can see, then a write-up. No legal finding that a lot is in violation. Do not skip a logged step or mail as counsel. One association per list unless they asked to combine and each row names the community.

**How to run:** Open or continue a Work Item under `work-items/<id>/`. Put operator files in `in/`. Walk the YAML steps below in order (one ready step per **continue** unless the operator asked for the whole named job). For each step: read the cited tool doc under `docs/tools/`, write the produced file under this Work Item (`work/` or `out/`), run the listed check against those same paths, copy check logs to `evidence/`, then update the Work Item journal with **journal-keeper**. Do not start a step whose `needs` files are missing. On check fail, retry the same step at most three times, then record the blocker and ask the operator. Human gates in `docs/role/work-item-method.md` are not passed by the word continue.

**Initial phase:** `role-job`

## Work map

```yaml
id: violations
steps:
  - id: pull
    needs: []
    produces: viol-raw
    produce_path: work/violations.csv
    tool: docs/tools/spreadsheet.md
    check: python docs/tools/checks/file-exists.py work/violations.csv
    on_fail: retry
    next: [columns]
  - id: columns
    needs: [viol-raw]
    produces: viol-cols
    produce_path: work/violations.csv
    tool: docs/tools/spreadsheet.md
    check: python docs/tools/checks/csv-has-columns.py work/violations.csv lot status
    on_fail: retry
    next: [write]
  - id: write
    needs: [viol-cols]
    produces: viol-writeup
    produce_path: out/violations.md
    tool: docs/tools/spreadsheet.md
    check: python docs/tools/checks/file-exists.py out/violations.md
    on_fail: retry
    next: []
```

Starter work map. Replace tools and checks when the operator **remember**s how this shop actually files.
