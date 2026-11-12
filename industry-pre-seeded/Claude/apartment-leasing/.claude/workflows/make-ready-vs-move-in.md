# Make Ready Vs Move In

**When to use:** Read make-ready status and lease-start dates, then flag units whose commence date is earlier than ready. Do not slide the date silently and do not mark a unit ready from a tour. Occupied-on-notice starts still need their vacant date. You do not promise keys. They change the start or they finish the turn. Work orders stay on the other role.

**How to run:** Open or continue a Work Item under `work-items/<id>/`. Put make-ready and lease-start exports in `in/`. Read this file and the named tool docs. Walk one ready YAML step (or the whole job if requested): produce the file under this Work Item’s `work/` or `out/`, run the check, then journal-keeper. Do not skip a step with a chat summary.

**Initial phase:** `role-job`

## Work map

```yaml
id: make-ready-vs-move-in
steps:
  - id: ready
    needs: []
    produces: ready
    produce_path: work/make-ready.csv
    tool: docs/tools/make-ready-sheet.md
    check: python docs/tools/checks/csv-has-columns.py work/make-ready.csv unit status
    on_fail: retry
    next: [starts]
  - id: starts
    needs: [ready]
    produces: starts
    produce_path: work/lease-starts.csv
    tool: docs/tools/pms-export.md
    check: python docs/tools/checks/csv-has-columns.py work/lease-starts.csv unit start
    on_fail: retry
    next: [pack]
  - id: pack
    needs: [ready, starts]
    produces: ready-pack
    produce_path: out/make-ready-vs-move-in.md
    tool: docs/tools/make-ready-sheet.md
    check: python docs/tools/checks/file-exists.py out/make-ready-vs-move-in.md
    on_fail: retry
    next: []
```

Starter work map. Replace tools and checks when the operator corrects this shop (remember / integrate-docs).
