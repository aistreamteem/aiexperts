# Fuel Outliers

**When to use:** Compare the fuel CSV to units on the roster. Odd gallons, wrong state versus the trip sheet, or unit/driver mismatch are questions, not accusations and not theft findings unless they defined a numeric rule. Do not invent gallons or store full card numbers. IFTA is not filed from this pack. Starter / guess until they teach this shop. Say which columns you compared. Full card numbers stay out. Humans decide what a spike means.

**How to run:** Self-contained. Use **continue** / **workflow-selector** / **journal-keeper**. See .claude/workflows/README.md.

1. Confirm or create `work-items/<id>/`. Put operator files in `in/`.
2. Load operations facts/rules, then walk the YAML map below (one ready step per continue unless they asked for the whole named job).
3. `work/` and `out/` are inside that Work Item. Read the named tool under `docs/tools/`. Run the step check against those paths. Retry at most 3 times, then ask with **operator-qa**.
4. Human gates: missing files, drafts, exception language, HOS/fuel questions, and treating a pack as dispatched or billed wait for the operator. "Continue" is not approval.

**Initial phase:** `role-job`

## Work map

```yaml
id: fuel-outliers
steps:
  - id: fuel
    needs: []
    produces: fuel-raw
    produce_path: work/fuel.csv
    tool: docs/tools/fuel-csv.md
    check: python docs/tools/checks/csv-has-columns.py work/fuel.csv unit gallons
    on_fail: retry
    next: [pack]
  - id: pack
    needs: [fuel-raw]
    produces: fuel-pack
    produce_path: out/fuel-questions.md
    tool: docs/tools/fuel-csv.md
    check: python docs/tools/checks/file-exists.py out/fuel-questions.md
    on_fail: retry
    next: []
```

Starter work map. Replace tools and checks when they **remember** a shop-specific change.
