# Incident Routing

**When to use:** From the incident log, list dated forms that still need a director signature, a parent-notice box, or a missing page. Route to the director. You do not diagnose, do not treat, and do not call a parent as this product unless they taught that step. Do not copy injury photos or extra medical notes into docs/. Other children’s names stay off the write-up when one child row will do. Serious wording is an immediate flag, not a scene you manage. Licensing notification stays their duty if their handbook says so.

**How to run:** Self-contained. Confirm an active Work Item at `work-items/<id>/` (copy `work-items/_TEMPLATE/` if needed). Paths `in/`, `work/`, `out/`, and `evidence/` are inside that folder. Load operations memory, then walk the map: a step is ready when every `needs` artifact exists on disk. Read the named `docs/tools/` file, produce `produce_path`, run `check` from the Work Item folder. On fail, retry at most 3 times, then ask with **operator-qa**. Do not invent a pass. After each step, **journal-keeper**. One ready step per **continue** unless the operator asked for the whole job. Finished pack lands in `out/`. Director gates (start, release, signatures) are not skipped.

**Initial phase:** `role-job`

## Work map

```yaml
id: incident-routing
steps:
  - id: log
    needs: []
    produces: log
    produce_path: work/incidents.csv
    tool: docs/tools/incident-log.md
    check: python docs/tools/checks/csv-has-columns.py work/incidents.csv date child
    on_fail: retry
    next: [grid]
  - id: grid
    needs: [log]
    produces: grid
    produce_path: work/incident-open.csv
    tool: docs/tools/spreadsheet.md
    check: python docs/tools/checks/file-exists.py work/incident-open.csv
    on_fail: retry
    next: [write]
  - id: write
    needs: [log, grid]
    produces: inc-pack
    produce_path: out/incident-routing.md
    tool: docs/tools/incident-log.md
    check: python docs/tools/checks/file-exists.py out/incident-routing.md
    on_fail: retry
    next: []
```

Starter work map. Replace tools and checks when the operator corrects them through **remember**.
