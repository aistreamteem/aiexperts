# Staffing from their file

**When to use:** Build a staffing board from the roster and the event-order labor grid: chef, captain, servers, bartender-as-count, driver. Flag missing rosters, invented-looking blanks, and people booked on overlapping windows. Do not invent a ratio. Do not stamp a bartender licensed. Overtime stays off unless their file has a rule. Write-up quotes the roster. They call staff. You do not fire anyone.

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
id: staffing-from-file
steps:
  - id: roster
    needs: []
    produces: roster
    produce_path: work/staff-roster.csv
    tool: docs/tools/staff-roster.md
    check: python docs/tools/checks/csv-has-columns.py work/staff-roster.csv event role
    on_fail: retry
    next: [orders]
  - id: orders
    needs: [roster]
    produces: orders
    produce_path: work/staff-orders.csv
    tool: docs/tools/event-order-pdf.md
    check: python docs/tools/checks/csv-has-columns.py work/staff-orders.csv event date
    on_fail: retry
    next: [pack]
  - id: pack
    needs: [roster, orders]
    produces: staff-pack
    produce_path: out/staffing-from-file.md
    tool: docs/tools/spreadsheet.md
    check: python docs/tools/checks/file-exists.py out/staffing-from-file.md
    on_fail: retry
    next: []
```

Starter work map. Replace tools and checks when they correct the shop and **remember**.
