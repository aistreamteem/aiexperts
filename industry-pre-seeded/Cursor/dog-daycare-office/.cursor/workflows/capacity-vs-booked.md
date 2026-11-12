# Capacity Vs Booked

**When to use:** Compare their capacity file to the boarding export for the date they asked. Use their max, not a number from another kennel. Do not raise a cap on paper. Do not staff the floor. Split daycare and overnight if their columns split. Quote both numbers in the pack when booked meets or exceeds max. Starter / guess until they teach weekday versus peak caps.

**How to run:** Open or continue a Work Item under `work-items/<id>/`. Put source files in `in/`. Walk one ready YAML step (or the whole named job if requested): read the named tool doc, produce the file, run the check, then **journal-keeper**.

**Initial phase:** `role-job`

## Work map

```yaml
id: capacity-vs-booked
steps:
  - id: cap
    needs: []
    produces: cap
    produce_path: work/capacity.csv
    tool: docs/tools/capacity-file.md
    check: python docs/tools/checks/csv-has-columns.py work/capacity.csv room max
    on_fail: retry
    next: [booked]
  - id: booked
    needs: [cap]
    produces: booked
    produce_path: work/boarding.csv
    tool: docs/tools/boarding-csv.md
    check: python docs/tools/checks/csv-has-columns.py work/boarding.csv patient stay
    on_fail: retry
    next: [write]
  - id: write
    needs: [cap, booked]
    produces: cap-pack
    produce_path: out/capacity-vs-booked.md
    tool: docs/tools/capacity-file.md
    check: python docs/tools/checks/file-exists.py out/capacity-vs-booked.md
    on_fail: retry
    next: []
```

Starter work map. Replace tools and checks when they correct this shop.
