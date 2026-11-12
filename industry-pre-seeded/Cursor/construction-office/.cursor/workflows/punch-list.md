# Punch List

**When to use:** One job. Room, item, owner, and done come from their sheet only. Do not close an item from a photo caption or invent rooms. Keep owner punch and contractor pre-punch on the lists they named if both exist. Reopened items stay open until they mark them. Their columns win, including informal cards they asked you to type. The pack quotes status words from the sheet the check can see and leaves missing owners as questions rather than assignments you make.

**How to run:** Follow `docs/role/work-item-method.md`. Use or create `work-items/<id>/`. Put source files in `in/`. For each YAML step below, in order: (1) do not start if `needs` files are missing — ask the operator; (2) read the `tool` file under `docs/tools/`; (3) write `produce_path` inside this Work Item folder (`work/` and `out/` are relative to the Work Item, not the expert root); (4) run `check` with those same relative paths; (5) on fail, retry at most 3 times then ask via **operator-qa**; (6) update the Work Item journal with **journal-keeper**. After the last step, the pack in `out/` must quote their source files. Do not invent counts, dates, approvals, or answers.

**Initial phase:** `intake`

## Work map

```yaml
id: punch-list
steps:
  - id: items
    needs: []
    produces: punch-raw
    produce_path: work/punch.csv
    tool: docs/tools/punch-sheet.md
    check: python docs/tools/checks/csv-has-columns.py work/punch.csv room item
    on_fail: retry
    next: [pack]
  - id: pack
    needs: [punch-raw]
    produces: punch-pack
    produce_path: out/punch.md
    tool: docs/tools/punch-sheet.md
    check: python docs/tools/checks/file-exists.py out/punch.md
    on_fail: retry
    next: []
```

Starter work map. Replace tools and checks when they confirm how this shop files.
