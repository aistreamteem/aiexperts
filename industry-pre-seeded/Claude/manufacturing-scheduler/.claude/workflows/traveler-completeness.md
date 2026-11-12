# Traveler Completeness Pack

**When to use:** Check traveler PDFs against the work-order export and the drawing index. Flag missing operations, revision mismatches, missing outside rows, and unsigned boxes as completeness only. Do not sign a box. Do not invent a missing operation. Do not treat the newest drawing as released. First-article and cert flags stay as their form printed them. They reprint; you list gaps. Outside-process rows that the job has and the PDF lacks stay on the exception list. They reprint; you do not rebuild a traveler from memory.

**How to run:** Create or continue a Work Item under `work-items/<id>/` (use **workflow-selector** if the job is not yet chosen). Put source files in `in/`. Walk this file's YAML map one ready step at a time unless the operator asked for the whole named job: read the cited `docs/tools/` file, write `produce_path` inside this Work Item (`work/` and `out/` are relative to it), run the check from the Work Item folder, copy check logs to `evidence/`, then **journal-keeper**. Do not start a step whose `needs` files are missing. On check fail, retry at most three times from the tool doc, then record the blocker and ask. When the last step passes, write the pack into `out/` quoting export dates; do not treat chat as the deliverable.

**Initial phase:** `intake`

## Work map

```yaml
id: traveler-completeness
steps:
  - id: wo
    needs: []
    produces: wos
    produce_path: work/work-orders.csv
    tool: docs/tools/wo-export.md
    check: python docs/tools/checks/csv-has-columns.py work/work-orders.csv wo item qty
    on_fail: retry
    next: [pdf]
  - id: pdf
    needs: [wos]
    produces: travelers
    produce_path: work/travelers-index.csv
    tool: docs/tools/traveler-pdf.md
    check: python docs/tools/checks/file-exists.py work/travelers-index.csv
    on_fail: retry
    next: [dwg]
  - id: dwg
    needs: [wos, travelers]
    produces: drawings
    produce_path: work/drawing-index.csv
    tool: docs/tools/drawing-index.md
    check: python docs/tools/checks/file-exists.py work/drawing-index.csv
    on_fail: retry
    next: [pack]
  - id: pack
    needs: [wos, travelers, drawings]
    produces: traveler-pack
    produce_path: out/traveler-completeness.md
    tool: docs/tools/traveler-pdf.md
    check: python docs/tools/checks/file-exists.py out/traveler-completeness.md
    on_fail: retry
    next: []
```

Starter work map. Replace tools and checks when the operator corrects how *this* shop works.
