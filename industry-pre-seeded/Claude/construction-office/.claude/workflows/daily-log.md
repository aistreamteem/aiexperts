# Daily Log

**When to use:** Fill or extract today's log for one job number into work/, then a pack that quotes their rows. Their template wins over starter columns. Keep weather, manpower, equipment, and notes as they wrote them; blank stays blank with an ask. Do not reconstruct a missing day from photos or last week. One job per pack unless they asked for a job column. Incidents on the log are flagged and leave this workflow. The pack should name the source sheet and the job number the check can see.

**How to run:** Follow `docs/role/work-item-method.md`. Use or create `work-items/<id>/`. Put source files in `in/`. For each YAML step below, in order: (1) do not start if `needs` files are missing — ask the operator; (2) read the `tool` file under `docs/tools/`; (3) write `produce_path` inside this Work Item folder (`work/` and `out/` are relative to the Work Item, not the expert root); (4) run `check` with those same relative paths; (5) on fail, retry at most 3 times then ask via **operator-qa**; (6) update the Work Item journal with **journal-keeper**. After the last step, the pack in `out/` must quote their source files. Do not invent counts, dates, approvals, or answers.

**Initial phase:** `intake`

## Work map

```yaml
id: daily-log
steps:
  - id: collect
    needs: []
    produces: log-raw
    produce_path: work/daily-log.csv
    tool: docs/tools/log-sheet.md
    check: python docs/tools/checks/csv-has-columns.py work/daily-log.csv date job
    on_fail: retry
    next: [pack]
  - id: pack
    needs: [log-raw]
    produces: log-pack
    produce_path: out/daily-log.md
    tool: docs/tools/log-sheet.md
    check: python docs/tools/checks/file-exists.py out/daily-log.md
    on_fail: retry
    next: []
```

Starter work map. Replace tools and checks when they confirm how this shop files.
