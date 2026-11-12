# POD Check

**When to use:** Match required stops to files in the POD folder. Unreadable images are questions. Use their signature-required flag; do not demand ink on a no-sig drop. Presence is file name yes/no, not a handwriting or porch analysis. Do not add coordinates to a photo. Ask when a required file is missing. Starter / guess until they teach this shop. If the required flag is missing on the stop row, ask before you mark a miss. Do not invent proof.

**How to run:** Self-contained. Use **continue** / **workflow-selector** / **journal-keeper**. See .claude/workflows/README.md.

1. Confirm or create `work-items/<id>/`. Put operator files in `in/`.
2. Load operations facts/rules, then walk the YAML map below (one ready step per continue unless they asked for the whole named job).
3. `work/` and `out/` are inside that Work Item. Read the named tool under `docs/tools/`. Run the step check against those paths. Retry at most 3 times, then ask with **operator-qa**.
4. Human gates: missing files, drafts, exception language, HOS/fuel questions, and treating a pack as dispatched or billed wait for the operator. "Continue" is not approval.

**Initial phase:** `role-job`

## Work map

```yaml
id: pod-check
steps:
  - id: stops
    needs: []
    produces: pod-stops
    produce_path: work/pod-required.csv
    tool: docs/tools/route-sheet.md
    check: python docs/tools/checks/csv-has-columns.py work/pod-required.csv stop pod_required
    on_fail: retry
    next: [pack]
  - id: pack
    needs: [pod-stops]
    produces: pod-pack
    produce_path: out/pod-check.md
    tool: docs/tools/pod-folder.md
    check: python docs/tools/checks/file-exists.py out/pod-check.md
    on_fail: retry
    next: []
```

Starter work map. Replace tools and checks when they **remember** a shop-specific change.
