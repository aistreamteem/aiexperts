# Pick / Wave List

**When to use:** Build today’s pick list from their pick export. Keep wave ids if they use them; do not invent a wave. Order, sku, and qty stay as exported. Short or unreleased lines stay visible. Locations come only if the file has them. This is outbound — not a receiving count. Write up exceptions. They release and they pick. You do not mark picked without their pack or pick-complete file.

**How to run:** Open or switch to a Work Item under `work-items/<id>/`. Put source files in that item's `in/`. Follow the YAML steps below — one ready step per **continue**, or the whole named job if requested. Read the named `docs/tools/` doc. Produce files under this Work Item. Run each step's check. Then **journal-keeper**.

**Initial phase:** `role-job`

## Work map

```yaml
id: pick-wave
steps:
  - id: pull
    needs: []
    produces: picks
    produce_path: work/picks.csv
    tool: docs/tools/pick-csv.md
    check: python docs/tools/checks/csv-has-columns.py work/picks.csv order sku qty
    on_fail: retry
    next: [pack]
  - id: pack
    needs: [picks]
    produces: pick-pack
    produce_path: out/pick-wave.md
    tool: docs/tools/spreadsheet.md
    check: python docs/tools/checks/file-exists.py out/pick-wave.md
    on_fail: retry
    next: []
```

Starter work map. Replace tools and checks when they correct this shop.
