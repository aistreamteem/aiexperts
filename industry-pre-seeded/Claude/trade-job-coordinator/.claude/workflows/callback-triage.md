# Callback Triage

**When to use:** List returns to recent jobs. Flag warranty versus billable per their marks. Do not admit legal fault. Same symptom inside their window is a flag before the row is booked as new revenue. Quote original and return job ids and the symptom in their words. Labor and parts clocks differ; do not extend either. Missing bill mark is a question for the person who owns pricing. Do not invent no-charge. The write-up keeps callbacks off the new-sale pile. Their type codes win.

**How to run:** Open or continue a Work Item under `work-items/<id>/`. Walk one ready YAML step (or the whole named job if requested). Produce the file, run the check, then **journal-keeper**.

**Initial phase:** `role-job`

## Work map

```yaml
id: callback-triage
steps:
  - id: list
    needs: []
    produces: callback-raw
    produce_path: work/callback-raw.csv
    tool: docs/tools/callback-log.md
    check: python docs/tools/checks/file-exists.py work/callback-raw.csv
    on_fail: retry
    next: [flag]
  - id: flag
    needs: [callback-raw]
    produces: callback-flagged
    produce_path: work/callback-flagged.csv
    tool: docs/tools/callback-log.md
    check: python docs/tools/checks/csv-has-columns.py work/callback-flagged.csv job type bill
    on_fail: retry
    next: [cb-pack]
  - id: cb-pack
    needs: [callback-flagged]
    produces: callback-writeup
    produce_path: out/callbacks.md
    tool: docs/tools/callback-log.md
    check: python docs/tools/checks/file-exists.py out/callbacks.md
    on_fail: retry
    next: []
```

Starter work map. Replace tools and checks when they correct this shop (**remember**).
