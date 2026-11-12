# Week-of events board

**When to use:** Build a week board from their event-order export and calendar: event, date, venue as address, style, guarantee or expected labeled as such, delivery window, and vehicle if the calendar has one. Flag missing guarantees that are past cutoff, missing windows, and van overlaps. Do not invent a date or a room. Do not treat a saved venue BEO as the hall's hold board. Write-up names which columns came from the order versus a guess you labeled. They run the week; you do not bump jobs.

## How to run

This file is the whole job. **continue** and **workflow-selector** walk it. Do not look for deleted process skills.

1. Confirm or open a Work Item under `work-items/<id>/` (use **workflow-selector** if none is active). Record this job id as the workflow type.
2. Load `facts/MEMORY-INDEX.md`, then `facts/facts-operations.md` and `facts/rules-operations.md`. Load Work Item facts/rules if present.
3. Put operator files in `work-items/<id>/in/`. Working extracts go in `work-items/<id>/work/`. Finished packs go in `work-items/<id>/out/`. Check logs go in `work-items/<id>/evidence/`.
4. Read only the tool docs named on each step.
5. Walk steps in order. Rewrite every `work/` and `out/` path so it sits under the Work Item folder. Do not start a step whose `needs` files are missing — ask.
6. After each step, run the listed check from the expert root with those rewritten paths. The step passes only when the check exits 0. On fail, retry at most 3 times, then ask. If a step has no check, propose a check and get operator approval before marking it passed.
7. Update the Work Item journal with **journal-keeper**. Missing shop knowledge: ask; do not invent. Requests outside `MyRole.txt`: refuse and stop.
8. Job is done when every step has a passing check (or a documented exception), the pack exists under `out/`, and holes stay visible.

**Initial phase:** `role-job`


## Work map

```yaml
id: week-of-events
steps:
  - id: orders
    needs: []
    produces: orders
    produce_path: work/event-orders.csv
    tool: docs/tools/event-order-pdf.md
    check: python docs/tools/checks/csv-has-columns.py work/event-orders.csv event date venue
    on_fail: retry
    next: [cal]
  - id: cal
    needs: [orders]
    produces: calendar
    produce_path: work/week-calendar.csv
    tool: docs/tools/calendar.md
    check: python docs/tools/checks/csv-has-columns.py work/week-calendar.csv event date
    on_fail: retry
    next: [pack]
  - id: pack
    needs: [orders, calendar]
    produces: week-board
    produce_path: out/week-of-events.md
    tool: docs/tools/spreadsheet.md
    check: python docs/tools/checks/file-exists.py out/week-of-events.md
    on_fail: retry
    next: []
```

Starter work map. Replace tools and checks when they correct the shop and **remember**.
