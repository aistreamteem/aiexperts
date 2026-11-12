# Detention

**When to use:** In and out times from their scan, route sheet, or site file. No invented dwell minutes or claim amount. Missing arrive or depart is a question. Long dwell is flagged for a human, not filed as a claim by you. Do not apply a shipper free-time table unless they gave that file. Starter / guess until they teach this shop.

**How to run:** Self-contained. Use **continue** / **workflow-selector** / **journal-keeper**. See .cursor/workflows/README.md.

1. Confirm or create `work-items/<id>/`. Put operator files in `in/`.
2. Load operations facts/rules, then walk the YAML map below (one ready step per continue unless they asked for the whole named job).
3. `work/` and `out/` are inside that Work Item. Read the named tool under `docs/tools/`. Run the step check against those paths. Retry at most 3 times, then ask with **operator-qa**.
4. Human gates: missing files, drafts, exception language, HOS/fuel questions, and treating a pack as dispatched or billed wait for the operator. "Continue" is not approval.

**Initial phase:** `role-job`

## Work map

```yaml
id: detention
steps:
  - id: times
    needs: []
    produces: dwell-raw
    produce_path: work/dwell.csv
    tool: docs/tools/route-sheet.md
    check: python docs/tools/checks/csv-has-columns.py work/dwell.csv stop arrive depart
    on_fail: retry
    next: [pack]
  - id: pack
    needs: [dwell-raw]
    produces: dwell-pack
    produce_path: out/detention.md
    tool: docs/tools/site-file.md
    check: python docs/tools/checks/file-exists.py out/detention.md
    on_fail: retry
    next: []
```

Starter work map. Replace tools and checks when they **remember** a shop-specific change.
