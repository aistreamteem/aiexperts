# Arrivals Day

**When to use:** Build today’s arrivals list from their CSV and mark ready versus not-ready using the room-status sheet. Do not assign a dirty or OOO room. Do not invent a rate or a room number the export left blank. Early check-in stays an ask. Group and OTA rows keep their source labels. DNR matches against their list are manager asks. They assign rooms and they check guests in. You deliver the list and write-up.

**How to run:** Self-contained for **continue** / **workflow-selector**.

1. Confirm an active Work Item under `work-items/<id>/`. Put the arrivals CSV and room-status sheet in `in/`.
2. Load `facts/MEMORY-INDEX.md`, then operations facts/rules, plus Work Item facts/rules if present.
3. Walk the steps below in order. Paths (`work/`, `out/`) are relative to `work-items/<id>/`. For each step: read the named tool doc, write the artifact, run the check. Missing needs → ask. Check fail → retry at most 3, then ask.
4. After the pack step, leave the finished list plus a short write-up in `out/` (docs used, artifacts, checks, open asks).
5. **journal-keeper**. One ready step per **continue** unless they asked for the whole named job.

**Initial phase:** `role-job`

## Work map

```yaml
id: arrivals-day
steps:
  - id: arrivals
    needs: []
    produces: arrivals
    produce_path: work/arrivals.csv
    tool: docs/tools/arrivals-csv.md
    check: python docs/tools/checks/csv-has-columns.py work/arrivals.csv confirmation room_type
    on_fail: retry
    next: [status]
  - id: status
    needs: [arrivals]
    produces: status
    produce_path: work/room-status.csv
    tool: docs/tools/room-status-sheet.md
    check: python docs/tools/checks/file-exists.py work/room-status.csv
    on_fail: retry
    next: [pack]
  - id: pack
    needs: [arrivals, status]
    produces: arrivals-pack
    produce_path: out/arrivals-day.md
    tool: docs/tools/spreadsheet.md
    check: python docs/tools/checks/file-exists.py out/arrivals-day.md
    on_fail: retry
    next: []
```

Starter step list. Replace tools and checks when they correct this property (**remember**).
