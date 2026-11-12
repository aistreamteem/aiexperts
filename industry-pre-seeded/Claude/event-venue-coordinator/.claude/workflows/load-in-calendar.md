# Load-In Calendar

**When to use:** Build a dock, elevator, and vendor arrival calendar from the timeline sheet and BEO time blocks. Flag overlaps and blank load-in on vendor-heavy days. Do not invent a default window. Do not write door codes. Load-out that hits the next setup stays on the conflict list. They assign slots. You deliver the calendar plus write-up. Freight-elevator windows and dock bays stay on separate columns when their sheets split them. Next-event setup after a late strike remains a conflict. They assign the slot; you do not invent a default two-hour load-in.

**How to run:** workflow-selector if no Work Item is active → follow this file one ready step (or whole named job if requested) → write artifacts under `work-items/<id>/` → journal-keeper

**Initial phase:** `role-job`

## Work map

```yaml
id: load-in-calendar
steps:
  - id: times
    needs: []
    produces: timeline
    produce_path: work/timeline.csv
    tool: docs/tools/timeline-sheet.md
    check: python docs/tools/checks/file-exists.py work/timeline.csv
    on_fail: retry
    next: [beos]
  - id: beos
    needs: [timeline]
    produces: beos
    produce_path: work/beos.csv
    tool: docs/tools/beo-pdf.md
    check: python docs/tools/checks/file-exists.py work/beos.csv
    on_fail: retry
    next: [pack]
  - id: pack
    needs: [timeline, beos]
    produces: loadin-pack
    produce_path: out/load-in-calendar.md
    tool: docs/tools/timeline-sheet.md
    check: python docs/tools/checks/file-exists.py out/load-in-calendar.md
    on_fail: retry
    next: []
```

Starter work map. Replace tools and checks when the operator teaches this shop (use remember).
