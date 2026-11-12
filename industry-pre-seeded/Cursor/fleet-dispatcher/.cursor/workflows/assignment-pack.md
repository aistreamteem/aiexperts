# Assignment Pack

**When to use:** Who is on which unit from the roster for the date. Draft options only if they asked and you label the draft. Do not invent qualifications, split a team, or put an off-roster driver on a unit as if dispatched. Copy only fields already in the export; no license images in docs/. Live board stays theirs. Starter / guess until they teach this shop.

**How to run:** Self-contained. Use **continue** / **workflow-selector** / **journal-keeper**. See .cursor/workflows/README.md.

1. Confirm or create `work-items/<id>/`. Put operator files in `in/`.
2. Load operations facts/rules, then walk the YAML map below (one ready step per continue unless they asked for the whole named job).
3. `work/` and `out/` are inside that Work Item. Read the named tool under `docs/tools/`. Run the step check against those paths. Retry at most 3 times, then ask with **operator-qa**.
4. Human gates: missing files, drafts, exception language, HOS/fuel questions, and treating a pack as dispatched or billed wait for the operator. "Continue" is not approval.

**Initial phase:** `role-job`

## Work map

```yaml
id: assignment-pack
steps:
  - id: pull
    needs: []
    produces: assign-raw
    produce_path: work/assignments.csv
    tool: docs/tools/roster.md
    check: python docs/tools/checks/csv-has-columns.py work/assignments.csv driver unit
    on_fail: retry
    next: [pack]
  - id: pack
    needs: [assign-raw]
    produces: assign-pack
    produce_path: out/assignments.md
    tool: docs/tools/roster.md
    check: python docs/tools/checks/file-exists.py out/assignments.md
    on_fail: retry
    next: []
```

Starter work map. Replace tools and checks when they **remember** a shop-specific change.
