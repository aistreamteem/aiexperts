# Today's Routes

**When to use:** Stops and missing PODs from their sheet for one service date. Sequence stays theirs unless they asked for a labeled draft. Pull the route export into the work CSV, then write the pack the checks can see. Do not invent addresses, windows, or a second day’s stops. POD presence is yes/no from their process and folder, not a signature you invent. Starter / guess until they teach this shop.

**How to run:** Self-contained. Use **continue** / **workflow-selector** / **journal-keeper**. See .cursor/workflows/README.md.

1. Confirm or create `work-items/<id>/`. Put operator files in `in/`.
2. Load operations facts/rules, then walk the YAML map below (one ready step per continue unless they asked for the whole named job).
3. `work/` and `out/` are inside that Work Item. Read the named tool under `docs/tools/`. Run the step check against those paths. Retry at most 3 times, then ask with **operator-qa**.
4. Human gates: missing files, drafts, exception language, HOS/fuel questions, and treating a pack as dispatched or billed wait for the operator. "Continue" is not approval.

**Initial phase:** `role-job`

## Work map

```yaml
id: todays-routes
steps:
  - id: pull
    needs: []
    produces: routes
    produce_path: work/routes.csv
    tool: docs/tools/route-sheet.md
    check: python docs/tools/checks/csv-has-columns.py work/routes.csv route stop date
    on_fail: retry
    next: [pack]
  - id: pack
    needs: [routes]
    produces: route-pack
    produce_path: out/routes.md
    tool: docs/tools/route-sheet.md
    check: python docs/tools/checks/file-exists.py out/routes.md
    on_fail: retry
    next: []
```

Starter work map. Replace tools and checks when they **remember** a shop-specific change.
