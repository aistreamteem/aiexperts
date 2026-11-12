# Look Ahead

**When to use:** From their schedule export, list the next window they named. Plan versus actual stays labeled. Do not re-sequence, staff, or claim a critical path. If the look-ahead and a longer update disagree, quote both and ask which is current. Activity names stay theirs, even when informal. Weather and inspection constraints they listed are copied, not managed. The pack is a plan file the check can see, not proof the work happened. Actual work remains on the daily log they file separately.

**How to run:** Follow `docs/role/work-item-method.md`. Use or create `work-items/<id>/`. Put source files in `in/`. For each YAML step below, in order: (1) do not start if `needs` files are missing — ask the operator; (2) read the `tool` file under `docs/tools/`; (3) write `produce_path` inside this Work Item folder (`work/` and `out/` are relative to the Work Item, not the expert root); (4) run `check` with those same relative paths; (5) on fail, retry at most 3 times then ask via **operator-qa**; (6) update the Work Item journal with **journal-keeper**. After the last step, the pack in `out/` must quote their source files. Do not invent counts, dates, approvals, or answers.

**Initial phase:** `intake`

## Work map

```yaml
id: look-ahead
steps:
  - id: export
    needs: []
    produces: sched-raw
    produce_path: work/lookahead.csv
    tool: docs/tools/schedule-export.md
    check: python docs/tools/checks/csv-has-columns.py work/lookahead.csv activity date
    on_fail: retry
    next: [pack]
  - id: pack
    needs: [sched-raw]
    produces: sched-pack
    produce_path: out/lookahead.md
    tool: docs/tools/schedule-export.md
    check: python docs/tools/checks/file-exists.py out/lookahead.md
    on_fail: retry
    next: []
```

Starter work map. Replace tools and checks when they confirm how this shop files.
