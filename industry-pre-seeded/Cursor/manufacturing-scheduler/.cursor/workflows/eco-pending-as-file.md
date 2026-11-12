# Pending ECO as File

**When to use:** List open work orders against the ECO log and the drawing index. Pending changes stay pending. You do not approve an ECO. You do not mark a job safe to run through a hold. Effectivity blanks stay blank and become asks. Traveler rev versus to-rev mismatches stay on the pack. They stamp the change. You only show the file. Hold-WIP notes on the log keep those jobs visible as held on any dispatch you also touch. You do not approve the change.

**How to run:** Create or continue a Work Item under `work-items/<id>/` (use **workflow-selector** if the job is not yet chosen). Put source files in `in/`. Walk this file's YAML map one ready step at a time unless the operator asked for the whole named job: read the cited `docs/tools/` file, write `produce_path` inside this Work Item (`work/` and `out/` are relative to it), run the check from the Work Item folder, copy check logs to `evidence/`, then **journal-keeper**. Do not start a step whose `needs` files are missing. On check fail, retry at most three times from the tool doc, then record the blocker and ask. When the last step passes, write the pack into `out/` quoting export dates; do not treat chat as the deliverable.

**Initial phase:** `intake`

## Work map

```yaml
id: eco-pending-as-file
steps:
  - id: eco
    needs: []
    produces: eco
    produce_path: work/eco-log.csv
    tool: docs/tools/eco-log.md
    check: python docs/tools/checks/file-exists.py work/eco-log.csv
    on_fail: retry
    next: [wo]
  - id: wo
    needs: [eco]
    produces: wos
    produce_path: work/work-orders.csv
    tool: docs/tools/wo-export.md
    check: python docs/tools/checks/csv-has-columns.py work/work-orders.csv wo item qty
    on_fail: retry
    next: [dwg]
  - id: dwg
    needs: [eco, wos]
    produces: drawings
    produce_path: work/drawing-index.csv
    tool: docs/tools/drawing-index.md
    check: python docs/tools/checks/file-exists.py work/drawing-index.csv
    on_fail: retry
    next: [pack]
  - id: pack
    needs: [eco, wos, drawings]
    produces: eco-pack
    produce_path: out/eco-pending.md
    tool: docs/tools/eco-log.md
    check: python docs/tools/checks/file-exists.py out/eco-pending.md
    on_fail: retry
    next: []
```

Starter work map. Replace tools and checks when the operator corrects how *this* shop works.
