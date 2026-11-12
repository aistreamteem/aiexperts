# WIP by Work Center

**When to use:** Group open work-order quantity by work center from the export and the work-center list. Do not hide WIP. Do not invent a location. Holds for shortage, ECO, or MRB stay labeled. Outside-process quantity stays on the outside row, not folded into an in-house center. If the export and a floor count they typed disagree, quote both. They move travelers; you list.

**How to run:** Create or continue a Work Item under `work-items/<id>/` (use **workflow-selector** if the job is not yet chosen). Put source files in `in/`. Walk this file's YAML map one ready step at a time unless the operator asked for the whole named job: read the cited `docs/tools/` file, write `produce_path` inside this Work Item (`work/` and `out/` are relative to it), run the check from the Work Item folder, copy check logs to `evidence/`, then **journal-keeper**. Do not start a step whose `needs` files are missing. On check fail, retry at most three times from the tool doc, then record the blocker and ask. When the last step passes, write the pack into `out/` quoting export dates; do not treat chat as the deliverable.

**Initial phase:** `intake`

## Work map

```yaml
id: wip-by-center
steps:
  - id: wo
    needs: []
    produces: wos
    produce_path: work/work-orders.csv
    tool: docs/tools/wo-export.md
    check: python docs/tools/checks/csv-has-columns.py work/work-orders.csv wo item qty
    on_fail: retry
    next: [centers]
  - id: centers
    needs: [wos]
    produces: centers
    produce_path: work/work-centers.csv
    tool: docs/tools/work-center-list.md
    check: python docs/tools/checks/file-exists.py work/work-centers.csv
    on_fail: retry
    next: [pack]
  - id: pack
    needs: [wos, centers]
    produces: wip-pack
    produce_path: out/wip-by-center.md
    tool: docs/tools/spreadsheet.md
    check: python docs/tools/checks/file-exists.py out/wip-by-center.md
    on_fail: retry
    next: []
```

Starter work map. Replace tools and checks when the operator corrects how *this* shop works.
