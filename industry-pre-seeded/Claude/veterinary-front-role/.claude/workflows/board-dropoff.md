# Board Dropoff

**When to use:** From their form, list pickup time, feeding as written, and missing signatures. Not medical advice. Copy belongings, emergency contacts, and authorized pickup names. Medication lines stay exact; do not convert units or add a drug. Surgery packets and daycare packets may differ; use the one they handed you. Unreadable writing is a question. Starter / guess until they teach who reviews the packet before kennel.

**How to run:** Open or continue a Work Item under `work-items/<id>/`. Put their boarding form in `in/`. Read this file and the named `docs/tools/` doc. Walk one ready YAML step (or the whole job if requested): produce the file under this Work Item’s `work/` or `out/`, run the check, then journal-keeper. Do not skip a step with a chat summary.

**Initial phase:** `role-job`

## Work map

```yaml
id: board-dropoff
steps:
  - id: list
    needs: []
    produces: board-raw
    produce_path: work/boarding.csv
    tool: docs/tools/boarding-form.md
    check: python docs/tools/checks/file-exists.py work/boarding.csv
    on_fail: retry
    next: [write]
  - id: write
    needs: [board-raw]
    produces: board-writeup
    produce_path: out/boarding.md
    tool: docs/tools/boarding-form.md
    check: python docs/tools/checks/file-exists.py out/boarding.md
    on_fail: retry
    next: []
```

Starter work map. Replace tools and checks when they correct this clinic.
