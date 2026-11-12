# Departures Due Out

**When to use:** List due-outs and planned departures from the in-house export and room status. Late-checkout asks stay asks. Unsettled folios are exceptions, not skippers unless they coded skipper. Do not invent a late fee. A due-out who extended must follow their export, not hope. They check guests out. You deliver the due-out list and write-up. Express-checkout flags stay as coded. Do not email a folio that shows PAN. Bags-in-room notes they wrote stay on the row. They settle tenders.

**How to run:** Self-contained for **continue** / **workflow-selector**.

1. Confirm an active Work Item under `work-items/<id>/`. Put the in-house export and room-status sheet in `in/`.
2. Load `facts/MEMORY-INDEX.md`, then operations facts/rules, plus Work Item facts/rules if present.
3. Walk the steps below in order. Paths (`work/`, `out/`) are relative to `work-items/<id>/`. For each step: read the named tool doc, write the artifact, run the check. Missing needs → ask. Check fail → retry at most 3, then ask.
4. After the pack step, leave the finished list plus a short write-up in `out/` (docs used, artifacts, checks, open asks).
5. **journal-keeper**. One ready step per **continue** unless they asked for the whole named job.

**Initial phase:** `role-job`

## Work map

```yaml
id: departures-due-out
steps:
  - id: inh
    needs: []
    produces: inhouse
    produce_path: work/in-house.csv
    tool: docs/tools/in-house-csv.md
    check: python docs/tools/checks/csv-has-columns.py work/in-house.csv room departure
    on_fail: retry
    next: [status]
  - id: status
    needs: [inhouse]
    produces: status
    produce_path: work/room-status.csv
    tool: docs/tools/room-status-sheet.md
    check: python docs/tools/checks/file-exists.py work/room-status.csv
    on_fail: retry
    next: [pack]
  - id: pack
    needs: [inhouse, status]
    produces: dept-pack
    produce_path: out/departures-due-out.md
    tool: docs/tools/spreadsheet.md
    check: python docs/tools/checks/file-exists.py out/departures-due-out.md
    on_fail: retry
    next: []
```

Starter step list. Replace tools and checks when they correct this property (**remember**).
