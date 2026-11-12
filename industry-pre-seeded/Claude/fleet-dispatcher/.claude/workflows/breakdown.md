# Breakdown

**When to use:** Unit down from their exception or GPS export. Location only if the file has it — no invented mile marker. Who they called only if they logged it. No out-of-service ruling and no tow ETA you invent. Put this write-up ahead of routine lates when you also touch the exception pack. Starter / guess until they teach this shop. If GPS and the exception log disagree on place or time, list both. No OOS language you chose.

**How to run:** Self-contained. Use **continue** / **workflow-selector** / **journal-keeper**. See .claude/workflows/README.md.

1. Confirm or create `work-items/<id>/`. Put operator files in `in/`.
2. Load operations facts/rules, then walk the YAML map below (one ready step per continue unless they asked for the whole named job).
3. `work/` and `out/` are inside that Work Item. Read the named tool under `docs/tools/`. Run the step check against those paths. Retry at most 3 times, then ask with **operator-qa**.
4. Human gates: missing files, drafts, exception language, HOS/fuel questions, and treating a pack as dispatched or billed wait for the operator. "Continue" is not approval.

**Initial phase:** `role-job`

## Work map

```yaml
id: breakdown
steps:
  - id: pull
    needs: []
    produces: brk-raw
    produce_path: work/breakdown.csv
    tool: docs/tools/exception-log.md
    check: python docs/tools/checks/csv-has-columns.py work/breakdown.csv unit time
    on_fail: retry
    next: [pack]
  - id: pack
    needs: [brk-raw]
    produces: brk-pack
    produce_path: out/breakdown.md
    tool: docs/tools/gps-export.md
    check: python docs/tools/checks/file-exists.py out/breakdown.md
    on_fail: retry
    next: []
```

Starter work map. Replace tools and checks when they **remember** a shop-specific change.
