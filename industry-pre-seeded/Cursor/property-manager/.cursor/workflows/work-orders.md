# Work Orders

**When to use:** Pull the live work-order export they name, then flag rows that lack a unit or that carry life-safety words this shop treats as emergency. Keep their status vocabulary. The pack is an open-ticket list plus flags, not a close-the-board exercise. Do not close tickets from a vendor text or a chat recap, do not merge two residents' issues, and do not invent a habitability ruling from a description. They dispatch and they pay vendors. Lockbox codes and portal passwords stay out of the pack.

**How to run:** Open or continue a Work Item under `work-items/<id>/`. Put source files in `in/`. Walk one ready YAML step (or the whole named job if requested): produce the file, run the check, then **journal-keeper**. Paths `work/` and `out/` are inside that Work Item.

**Initial phase:** `role-job`

## Work map

```yaml
id: work-orders
steps:
  - id: pull
    needs: []
    produces: wo-raw
    produce_path: work/wo-raw.csv
    tool: docs/tools/wo-export.md
    check: python docs/tools/checks/file-exists.py work/wo-raw.csv
    on_fail: retry
    next: [flag]
  - id: flag
    needs: [wo-raw]
    produces: wo-flagged
    produce_path: work/wo-flagged.csv
    tool: docs/tools/wo-export.md
    check: python docs/tools/checks/csv-has-columns.py work/wo-flagged.csv unit status flag
    on_fail: retry
    next: [pack]
  - id: pack
    needs: [wo-flagged]
    produces: wo-pack
    produce_path: out/work-orders.md
    tool: docs/tools/spreadsheet.md
    check: python docs/tools/checks/file-exists.py out/work-orders.md
    on_fail: retry
    next: []
```

Starter work map. Replace tools and checks when they correct this shop (use **remember**).
