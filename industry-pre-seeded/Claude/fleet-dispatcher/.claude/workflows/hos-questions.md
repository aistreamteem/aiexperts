# HOS Questions

**When to use:** List gaps from their ELD export as questions: certify, unassigned, edits, malfunctions, date-range misses. No compliance stamp. No remaining-hours legal math. Do not assign unassigned driving or suggest a duty-status change. Say public limit names are orientation only. A human decides status. Starter / guess until they teach this shop. Date range must cover the route date; if it does not, that is the first question. No fake ELD math.

**How to run:** Self-contained. Use **continue** / **workflow-selector** / **journal-keeper**. See .claude/workflows/README.md.

1. Confirm or create `work-items/<id>/`. Put operator files in `in/`.
2. Load operations facts/rules, then walk the YAML map below (one ready step per continue unless they asked for the whole named job).
3. `work/` and `out/` are inside that Work Item. Read the named tool under `docs/tools/`. Run the step check against those paths. Retry at most 3 times, then ask with **operator-qa**.
4. Human gates: missing files, drafts, exception language, HOS/fuel questions, and treating a pack as dispatched or billed wait for the operator. "Continue" is not approval.

**Initial phase:** `role-job`

## Work map

```yaml
id: hos-questions
steps:
  - id: pull
    needs: []
    produces: eld-raw
    produce_path: work/eld.csv
    tool: docs/tools/eld-export.md
    check: python docs/tools/checks/csv-has-columns.py work/eld.csv driver status
    on_fail: retry
    next: [pack]
  - id: pack
    needs: [eld-raw]
    produces: eld-pack
    produce_path: out/hos-questions.md
    tool: docs/tools/eld-export.md
    check: python docs/tools/checks/file-exists.py out/hos-questions.md
    on_fail: retry
    next: []
```

Starter work map. Replace tools and checks when they **remember** a shop-specific change.
