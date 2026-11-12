# Work Orders

**When to use:** From their export, list open common-area jobs, locations, vendors, and missing vendor or photo fields. No engineering judgment and no owner-versus-association legal call unless you quote their matrix. Emergency flags use their on-call list, not a web search. One community per list unless they asked for a labeled portfolio. Produce the CSV the checks can see, then the write-up. Confirm the association name on the export header before you list jobs.

**How to run:** Open or continue a Work Item under `work-items/<id>/`. Put operator files in `in/`. Walk the YAML steps below in order (one ready step per **continue** unless the operator asked for the whole named job). For each step: read the cited tool doc under `docs/tools/`, write the produced file under this Work Item (`work/` or `out/`), run the listed check against those same paths, copy check logs to `evidence/`, then update the Work Item journal with **journal-keeper**. Do not start a step whose `needs` files are missing. On check fail, retry the same step at most three times, then record the blocker and ask the operator. Human gates in `docs/role/work-item-method.md` are not passed by the word continue.

**Initial phase:** `role-job`

## Work map

```yaml
id: work-orders
steps:
  - id: pull
    needs: []
    produces: wo-raw
    produce_path: work/work-orders.csv
    tool: docs/tools/work-order-export.md
    check: python docs/tools/checks/file-exists.py work/work-orders.csv
    on_fail: retry
    next: [columns]
  - id: columns
    needs: [wo-raw]
    produces: wo-cols
    produce_path: work/work-orders.csv
    tool: docs/tools/work-order-export.md
    check: python docs/tools/checks/csv-has-columns.py work/work-orders.csv wo status
    on_fail: retry
    next: [write]
  - id: write
    needs: [wo-cols]
    produces: wo-writeup
    produce_path: out/work-orders.md
    tool: docs/tools/work-order-export.md
    check: python docs/tools/checks/file-exists.py out/work-orders.md
    on_fail: retry
    next: []
```

Starter work map. Replace tools and checks when the operator **remember**s how this shop actually files.
