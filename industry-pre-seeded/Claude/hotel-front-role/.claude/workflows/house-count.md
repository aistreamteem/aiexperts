# House Count

**When to use:** Restate tonight’s house count from their PMS export and in-house list: occupied, vacant-sellable, OOO, arrivals not in, and due-outs, by type if their report splits them. Occupancy percent and ADR only if their flash already printed them or they wrote the math. If the three files disagree, quote all three. Do not invent a percent. They decide what to sell. You deliver the count and write-up.

**How to run:** Self-contained for **continue** / **workflow-selector**.

1. Confirm an active Work Item under `work-items/<id>/`. Put the PMS export and in-house list in `in/`.
2. Load `facts/MEMORY-INDEX.md`, then operations facts/rules, plus Work Item facts/rules if present.
3. Walk the steps below in order. Paths (`work/`, `out/`) are relative to `work-items/<id>/`. For each step: read the named tool doc, write the artifact, run the check. Missing needs → ask. Check fail → retry at most 3, then ask.
4. After the pack step, leave the finished list plus a short write-up in `out/` (docs used, artifacts, checks, open asks).
5. **journal-keeper**. One ready step per **continue** unless they asked for the whole named job.

**Initial phase:** `role-job`

## Work map

```yaml
id: house-count
steps:
  - id: pms
    needs: []
    produces: pms
    produce_path: work/pms-house.csv
    tool: docs/tools/pms-export.md
    check: python docs/tools/checks/file-exists.py work/pms-house.csv
    on_fail: retry
    next: [inh]
  - id: inh
    needs: [pms]
    produces: inhouse
    produce_path: work/in-house.csv
    tool: docs/tools/in-house-csv.md
    check: python docs/tools/checks/csv-has-columns.py work/in-house.csv room status
    on_fail: retry
    next: [pack]
  - id: pack
    needs: [pms, inhouse]
    produces: count-pack
    produce_path: out/house-count.md
    tool: docs/tools/spreadsheet.md
    check: python docs/tools/checks/file-exists.py out/house-count.md
    on_fail: retry
    next: []
```

Starter step list. Replace tools and checks when they correct this property (**remember**).
