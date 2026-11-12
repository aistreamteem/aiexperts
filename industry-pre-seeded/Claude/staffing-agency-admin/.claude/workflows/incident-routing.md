# Incident Routing

**When to use:** Read the incident log and matching assignments. List form-present, date, site, and who their process names as the receiver. Do not decide fault. Do not give a workers'-comp opinion. Do not copy extra medical narrative into docs/. Near-miss versus injury stays their label. Write the routing pack. They investigate. You flag missing forms. OSHA temporary-worker pages are orientation only.

**How to run:** Open or continue a Work Item under `work-items/<id>/`. Put incident log and assignments in `in/`. Read this file and the named `docs/tools/` doc. Walk one ready YAML step (or the whole job if requested): produce the file under this Work Item’s `work/` or `out/`, run the check, then journal-keeper. Do not skip a step with a chat summary.

**Initial phase:** `role-job`

## Work map

```yaml
id: incident-routing
steps:
  - id: inc
    needs: []
    produces: incidents
    produce_path: work/incidents.csv
    tool: docs/tools/incident-log.md
    check: python docs/tools/checks/csv-has-columns.py work/incidents.csv name date
    on_fail: retry
    next: [assign]
  - id: assign
    needs: [incidents]
    produces: assign
    produce_path: work/assignments.csv
    tool: docs/tools/assignment-sheet.md
    check: python docs/tools/checks/file-exists.py work/assignments.csv
    on_fail: retry
    next: [pack]
  - id: pack
    needs: [incidents, assign]
    produces: inc-pack
    produce_path: out/incident-routing.md
    tool: docs/tools/incident-log.md
    check: python docs/tools/checks/file-exists.py out/incident-routing.md
    on_fail: retry
    next: []
```

Starter work map. Replace tools and checks when they correct this shop.
