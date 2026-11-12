# DVIR Gap

**When to use:** Which units on today’s roster have a DVIR file. Missing is missing. No invented clean reports and no copy-forward from yesterday or from the tractor onto a trailer. Join roster units to the inspection export, then write gaps the checks can see. Defect text is copied, not closed by you. Not an out-of-service ruling. Starter / guess until they teach this shop.

**How to run:** Self-contained. Use **continue** / **workflow-selector** / **journal-keeper**. See .cursor/workflows/README.md.

1. Confirm or create `work-items/<id>/`. Put operator files in `in/`.
2. Load operations facts/rules, then walk the YAML map below (one ready step per continue unless they asked for the whole named job).
3. `work/` and `out/` are inside that Work Item. Read the named tool under `docs/tools/`. Run the step check against those paths. Retry at most 3 times, then ask with **operator-qa**.
4. Human gates: missing files, drafts, exception language, HOS/fuel questions, and treating a pack as dispatched or billed wait for the operator. "Continue" is not approval.

**Initial phase:** `role-job`

## Work map

```yaml
id: dvir-gap
steps:
  - id: units
    needs: []
    produces: units-raw
    produce_path: work/units.csv
    tool: docs/tools/roster.md
    check: python docs/tools/checks/csv-has-columns.py work/units.csv unit driver
    on_fail: retry
    next: [dvirs]
  - id: dvirs
    needs: [units-raw]
    produces: dvir-raw
    produce_path: work/dvir.csv
    tool: docs/tools/dvir.md
    check: python docs/tools/checks/csv-has-columns.py work/dvir.csv unit date defect
    on_fail: retry
    next: [pack]
  - id: pack
    needs: [dvir-raw]
    produces: dvir-pack
    produce_path: out/dvir-gaps.md
    tool: docs/tools/dvir.md
    check: python docs/tools/checks/file-exists.py out/dvir-gaps.md
    on_fail: retry
    next: []
```

Starter work map. Replace tools and checks when they **remember** a shop-specific change.
