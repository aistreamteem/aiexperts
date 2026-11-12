# Claims Routing

**When to use:** Assemble the claim row, named photos, and BOL number if present. Route to the owner they named. Do not decide fault or a settlement dollar. Quote deadline words from their form only — not a legal bar date. Do not invent a missing piece. High-value list presence stays a flag if their rule requires it. They adjust. You write the routing pack and the hole list.

**How to run:** This file is the instruction. After **workflow-selector** records this job:

1. Confirm `work-items/<id>/` exists. Operator claims log, photos, and BOL go in `in/`.
2. For the next ready step, read the named tool under `docs/tools/`.
3. Write the artifact inside the Work Item folder.
4. Run the check from the Work Item folder. Exit 0 = pass. On fail, retry at most 3 times, then ask.
5. **journal-keeper**. One ready step per **continue** unless they asked for the whole job.

**Human gates:** Operator names who owns the log. They adjust or send to the van line. You do not settle.

**Initial phase:** `role-job` (method phase: claims)

## Work map

```yaml
id: claims-routing
steps:
  - id: log
    needs: []
    produces: log
    produce_path: work/claims-log.csv
    tool: docs/tools/claims-log.md
    check: python docs/tools/checks/csv-has-columns.py work/claims-log.csv claim job
    on_fail: retry
    next: [photos]
  - id: photos
    needs: [log]
    produces: photos
    produce_path: work/claim-photos.csv
    tool: docs/tools/photo-folder.md
    check: python docs/tools/checks/file-exists.py work/claim-photos.csv
    on_fail: retry
    next: [pack]
  - id: pack
    needs: [log, photos]
    produces: claims-pack
    produce_path: out/claims-routing.md
    tool: docs/tools/spreadsheet.md
    check: python docs/tools/checks/file-exists.py out/claims-routing.md
    on_fail: retry
    next: []
```

Starter work map. Replace tools and checks when the operator confirms how *this* shop files.
