# Machine-Down versus WIP

**When to use:** Put the machine-status file next to open work at those work centers. Down stays visible. Do not invent a repair duration or a diagnosis. Queued jobs remain on the list. Alternate-router moves wait for their file. Capacity hours on a down day are not available unless they wrote a workaround. Write-up quotes the status timestamp. They return the machine to service.

**How to run:** Create or continue a Work Item under `work-items/<id>/` (use **workflow-selector** if the job is not yet chosen). Put source files in `in/`. Walk this file's YAML map one ready step at a time unless the operator asked for the whole named job: read the cited `docs/tools/` file, write `produce_path` inside this Work Item (`work/` and `out/` are relative to it), run the check from the Work Item folder, copy check logs to `evidence/`, then **journal-keeper**. Do not start a step whose `needs` files are missing. On check fail, retry at most three times from the tool doc, then record the blocker and ask. When the last step passes, write the pack into `out/` quoting export dates; do not treat chat as the deliverable.

**Initial phase:** `intake`

## Work map

```yaml
id: machine-down-vs-wip
steps:
  - id: status
    needs: []
    produces: status
    produce_path: work/machine-status.csv
    tool: docs/tools/machine-status.md
    check: python docs/tools/checks/file-exists.py work/machine-status.csv
    on_fail: retry
    next: [wo]
  - id: wo
    needs: [status]
    produces: wos
    produce_path: work/work-orders.csv
    tool: docs/tools/wo-export.md
    check: python docs/tools/checks/csv-has-columns.py work/work-orders.csv wo item qty
    on_fail: retry
    next: [pack]
  - id: pack
    needs: [status, wos]
    produces: down-pack
    produce_path: out/machine-down-wip.md
    tool: docs/tools/spreadsheet.md
    check: python docs/tools/checks/file-exists.py out/machine-down-wip.md
    on_fail: retry
    next: []
```

Starter work map. Replace tools and checks when the operator corrects how *this* shop works.
