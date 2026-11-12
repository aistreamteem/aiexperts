# Group Block Vs Pickup

**When to use:** Compare contracted block rooms to pickup on their group sheet and the arrivals export. List remaining, cutoff, and wash only as written. Blank cutoff is an ask. Do not invent a group rate or release rooms. Rooming-list names must already be on their file. Attach a BEO note only if they dropped one. They cut or wash. You deliver the comparison and write-up.

**How to run:** Self-contained for **continue** / **workflow-selector**.

1. Confirm an active Work Item under `work-items/<id>/`. Put the group sheet and arrivals export in `in/`.
2. Load `facts/MEMORY-INDEX.md`, then operations facts/rules, plus Work Item facts/rules if present.
3. Walk the steps below in order. Paths (`work/`, `out/`) are relative to `work-items/<id>/`. For each step: read the named tool doc, write the artifact, run the check. Missing needs → ask. Check fail → retry at most 3, then ask.
4. After the pack step, leave the finished list plus a short write-up in `out/` (docs used, artifacts, checks, open asks).
5. **journal-keeper**. One ready step per **continue** unless they asked for the whole named job.

**Initial phase:** `role-job`

## Work map

```yaml
id: group-block-vs-pickup
steps:
  - id: block
    needs: []
    produces: block
    produce_path: work/group-block.csv
    tool: docs/tools/group-block-sheet.md
    check: python docs/tools/checks/csv-has-columns.py work/group-block.csv group pickup
    on_fail: retry
    next: [arr]
  - id: arr
    needs: [block]
    produces: arrivals
    produce_path: work/arrivals.csv
    tool: docs/tools/arrivals-csv.md
    check: python docs/tools/checks/file-exists.py work/arrivals.csv
    on_fail: retry
    next: [pack]
  - id: pack
    needs: [block, arrivals]
    produces: group-pack
    produce_path: out/group-block-vs-pickup.md
    tool: docs/tools/spreadsheet.md
    check: python docs/tools/checks/file-exists.py out/group-block-vs-pickup.md
    on_fail: retry
    next: []
```

Starter step list. Replace tools and checks when they correct this property (**remember**).
