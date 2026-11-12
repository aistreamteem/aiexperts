# Emergency Queue

**When to use:** Jobs they marked emergency or that match their life-safety words. Windows, tech, parts. No clock-time promise they did not give. Gas, CO, sparking, freeze no-heat, and active flood stay at the front if they used those words. Ask their definition; do not invent a medical file. After-hours rates are their book. Do not diagnose. Do not park these rows behind a membership. Parts gaps still show as questions. The queue lists job, window, and tech from their board. Utility or 911 first when they already say so.

**How to run:** Open or continue a Work Item under `work-items/<id>/`. Put source files in `in/`. Walk one ready YAML step (or the whole named job if requested): produce the file, run the check, then **journal-keeper**.

**Initial phase:** `role-job`

## Work map

```yaml
id: emergency-queue
steps:
  - id: priority
    needs: []
    produces: emerg-raw
    produce_path: work/emergency-raw.csv
    tool: docs/tools/schedule-sheet.md
    check: python docs/tools/checks/file-exists.py work/emergency-raw.csv
    on_fail: retry
    next: [windows]
  - id: windows
    needs: [emerg-raw]
    produces: emerg-windows
    produce_path: work/emergency-windows.csv
    tool: docs/tools/schedule-sheet.md
    check: python docs/tools/checks/csv-has-columns.py work/emergency-windows.csv job window tech
    on_fail: retry
    next: [emerg-pack]
  - id: emerg-pack
    needs: [emerg-windows]
    produces: emergency-writeup
    produce_path: out/emergency-queue.md
    tool: docs/tools/schedule-sheet.md
    check: python docs/tools/checks/file-exists.py out/emergency-queue.md
    on_fail: retry
    next: []
```

Starter work map. Replace tools and checks when they correct this shop (**remember**).
