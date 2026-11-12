# Owner Month

**When to use:** Gather the period files they drop for one property and one named date range: cash or bank export, bills, open work orders, and the rent-roll as-of. Assemble categories they already use, then write the pack with property, owner entity, and dates on the front. Do not send owner money, do not mix owners, and do not treat surplus as a draw you ran. Deposit and trust cash stay in the labels they taught. Legal and inspection questions stay questions.

**How to run:** Open or continue a Work Item under `work-items/<id>/`. Put source files in `in/`. Walk one ready YAML step (or the whole named job if requested): produce the file, run the check, then **journal-keeper**. Paths `work/` and `out/` are inside that Work Item.

**Initial phase:** `role-job`

## Work map

```yaml
id: owner-month
steps:
  - id: gather
    needs: []
    produces: owner-inputs
    produce_path: work/owner-inputs.csv
    tool: docs/tools/owner-pack-folder.md
    check: python docs/tools/checks/file-exists.py work/owner-inputs.csv
    on_fail: retry
    next: [assemble]
  - id: assemble
    needs: [owner-inputs]
    produces: owner-assembled
    produce_path: work/owner-assembled.csv
    tool: docs/tools/spreadsheet.md
    check: python docs/tools/checks/csv-has-columns.py work/owner-assembled.csv date amount category
    on_fail: retry
    next: [pack]
  - id: pack
    needs: [owner-assembled]
    produces: owner-pack
    produce_path: out/owner-pack.md
    tool: docs/tools/owner-pack-folder.md
    check: python docs/tools/checks/file-exists.py out/owner-pack.md
    on_fail: retry
    next: []
```

Starter work map. Replace tools and checks when they correct this shop (use **remember**).
