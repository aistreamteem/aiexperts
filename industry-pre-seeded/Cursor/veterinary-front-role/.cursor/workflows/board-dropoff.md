# Board Dropoff

**When to use:** From their form, list pickup time, feeding as written, and missing signatures. Not medical advice. Copy belongings, emergency contacts, and authorized pickup names. Medication lines stay exact; do not convert units or add a drug. Surgery packets and daycare packets may differ; use the one they handed you. Unreadable writing is a question. Starter / guess until they teach who reviews the packet before kennel.

**How to run:** Open/reuse a Work Item under `work-items/<id>/`. Follow this map one ready step (or the whole named job if requested). Read the named `docs/tools/` file. Write produce_path inside this Work Item. Run the step check. Then journal-keeper.

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

Starter work map. Replace tools and checks when they confirm how this clinic works.
