# Make Ready Pack

**When to use:** Build the punch for one vacant unit they name, using their checklist, then attach vendor dates from the quote or invoice files they provided. Flag missing photos and items still open. Rent-ready is their label, not an inspection pass or a habitability stamp. Do not add hotel-grade work they do not use, do not mark done without their file, and do not paste lockbox codes onto the punch. They award vendors and they pay.

**How to run:** Open or continue a Work Item under `work-items/<id>/`. Put source files in `in/`. Walk one ready YAML step (or the whole named job if requested): produce the file, run the check, then **journal-keeper**. Paths `work/` and `out/` are inside that Work Item.

**Initial phase:** `role-job`

## Work map

```yaml
id: make-ready-pack
steps:
  - id: punch
    needs: []
    produces: punch-raw
    produce_path: work/make-ready-punch.csv
    tool: docs/tools/make-ready-list.md
    check: python docs/tools/checks/csv-has-columns.py work/make-ready-punch.csv unit item status
    on_fail: retry
    next: [vendors]
  - id: vendors
    needs: [punch-raw]
    produces: punch-vendors
    produce_path: work/make-ready-vendors.csv
    tool: docs/tools/vendor-portal.md
    check: python docs/tools/checks/file-exists.py work/make-ready-vendors.csv
    on_fail: retry
    next: [ready-pack]
  - id: ready-pack
    needs: [punch-vendors]
    produces: make-ready-writeup
    produce_path: out/make-ready.md
    tool: docs/tools/make-ready-list.md
    check: python docs/tools/checks/file-exists.py out/make-ready.md
    on_fail: retry
    next: []
```

Starter work map. Replace tools and checks when they correct this shop (use **remember**).
