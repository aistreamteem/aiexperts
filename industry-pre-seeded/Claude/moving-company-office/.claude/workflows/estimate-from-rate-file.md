# Estimate From Rate File

**When to use:** Draft the estimate from their rate file plus the inventory they stored. Copy extras only when the survey already names them. Leave weight and cube blank unless a scale ticket or their sheet already has a number — never invent either. Binding type stays as their file or an ask. Fuel comes only from their memo. They send the estimate. You write the draft and the questions the check can see.

**How to run:** This file is the instruction. After **workflow-selector** records this job:

1. Confirm `work-items/<id>/` exists (`in/`, `work/`, `out/`, `evidence/`). Operator source files go in `in/`.
2. For the next ready step, read the named tool under `docs/tools/`.
3. Write the artifact at that path **inside the Work Item folder**.
4. Run the check from the Work Item folder. Exit 0 = pass. On fail, retry at most 3 times, then record the blocker and ask (**operator-qa** if clarification would change the draft).
5. **journal-keeper**. One ready step per **continue** unless they asked for the whole job.

**Human gates:** Operator confirms the rate file is the live one. Operator picks binding type if missing. Operator sends the estimate. Do not invent extras, fuel, weight, or cube.

**Initial phase:** `role-job` (method phase: estimate)

## Work map

```yaml
id: estimate-from-rate-file
steps:
  - id: rate
    needs: []
    produces: rate
    produce_path: work/rate-file.csv
    tool: docs/tools/rate-file.md
    check: python docs/tools/checks/file-exists.py work/rate-file.csv
    on_fail: retry
    next: [inv]
  - id: inv
    needs: [rate]
    produces: inv
    produce_path: work/inventory.csv
    tool: docs/tools/inventory-sheet.md
    check: python docs/tools/checks/csv-has-columns.py work/inventory.csv job item qty
    on_fail: retry
    next: [pack]
  - id: pack
    needs: [rate, inv]
    produces: estimate-pack
    produce_path: out/estimate-draft.md
    tool: docs/tools/spreadsheet.md
    check: python docs/tools/checks/file-exists.py out/estimate-draft.md
    on_fail: retry
    next: []
```

Starter work map. Replace tools and checks when the operator confirms how *this* shop files.
