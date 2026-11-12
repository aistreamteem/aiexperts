# Sub COI

**When to use:** Roster plus certificate dates they already track. Flag missing or past dates. Do not invent insurance, type in force, or decide additional-insured wording is enough. Copy named insured and expirations as the PDF shows. A company on last week's daily is not automatically on this roster. Missing endorsement pages are missing pages. The flag file is a date compare, not a legal opinion. The pack lists who is on their sheet and which certificates need their broker or sub to refresh.

**How to run:** Follow `docs/role/work-item-method.md`. Use or create `work-items/<id>/`. Put source files in `in/`. For each YAML step below, in order: (1) do not start if `needs` files are missing — ask the operator; (2) read the `tool` file under `docs/tools/`; (3) write `produce_path` inside this Work Item folder (`work/` and `out/` are relative to the Work Item, not the expert root); (4) run `check` with those same relative paths; (5) on fail, retry at most 3 times then ask via **operator-qa**; (6) update the Work Item journal with **journal-keeper**. After the last step, the pack in `out/` must quote their source files. Do not invent counts, dates, approvals, or answers.

**Initial phase:** `intake`

## Work map

```yaml
id: sub-coi
steps:
  - id: roster
    needs: []
    produces: subs
    produce_path: work/sub-roster.csv
    tool: docs/tools/sub-roster.md
    check: python docs/tools/checks/csv-has-columns.py work/sub-roster.csv company trade
    on_fail: retry
    next: [flag]
  - id: flag
    needs: [subs]
    produces: coi-flags
    produce_path: work/coi-flags.csv
    tool: docs/tools/sub-roster.md
    check: python docs/tools/checks/csv-has-columns.py work/coi-flags.csv company flag
    on_fail: retry
    next: [pack]
  - id: pack
    needs: [coi-flags]
    produces: coi-pack
    produce_path: out/sub-coi.md
    tool: docs/tools/sub-roster.md
    check: python docs/tools/checks/file-exists.py out/sub-coi.md
    on_fail: retry
    next: []
```

Starter work map. Replace tools and checks when they confirm how this shop files.
