# Hold and Will-call List

**When to use:** From the pick or address file, list credit holds, ship-complete holds, hold-for-pickup, and will-call. Do not put those orders on a street manifest. Do not invent a hold site or a pickup name. Ask before releasing a hold. Will-call is shop pickup, not carrier hold. You do not hand goods to a visitor. They release at the counter or they change the order.

**How to run:** Open or switch to a Work Item under `work-items/<id>/`. Put source files in that item’s `in/`. Follow the YAML steps below — one ready step per **continue**, or the whole named job if requested. Read the named `docs/tools/` doc. Produce files under this Work Item. Run each step’s check. Then **journal-keeper**.

**Initial phase:** `role-job`

## Work map

```yaml
id: hold-and-will-call
steps:
  - id: picks
    needs: []
    produces: picks
    produce_path: work/picks.csv
    tool: docs/tools/pick-csv.md
    check: python docs/tools/checks/csv-has-columns.py work/picks.csv order sku qty
    on_fail: retry
    next: [addr]
  - id: addr
    needs: [picks]
    produces: addr
    produce_path: work/addresses.csv
    tool: docs/tools/address-file.md
    check: python docs/tools/checks/file-exists.py work/addresses.csv
    on_fail: retry
    next: [pack]
  - id: pack
    needs: [picks, addr]
    produces: hold-pack
    produce_path: out/hold-will-call.md
    tool: docs/tools/spreadsheet.md
    check: python docs/tools/checks/file-exists.py out/hold-will-call.md
    on_fail: retry
    next: []
```

Starter work map. Replace tools and checks when they **remember** a shop correction.
