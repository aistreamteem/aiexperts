# Pickup List

**When to use:** Build a door or aftercare check from their pickup file. Flag names on early-dismissal notes that are not on the list, and flag custody-file mismatches if they also dropped that PDF. Do not add a name. Do not release a child. Min necessary on the printed sheet. They train the door. You pack exceptions. Aftercare and bus sheets compare to the same list unless they split files. You do not release anyone. Verbal door claims are not rows. They update names.

**How to run:** Open or continue a Work Item under `work-items/<id>/`. Put source files in `in/`. Walk one ready YAML step (or the whole named job if requested): produce the file, run the check, then **journal-keeper**.

**Initial phase:** `role-job`

## Work map

```yaml
id: pickup-list
steps:
  - id: list
    needs: []
    produces: pickup
    produce_path: work/pickup.csv
    tool: docs/tools/pickup-list.md
    check: python docs/tools/checks/csv-has-columns.py work/pickup.csv student
    on_fail: retry
    next: [pack]
  - id: pack
    needs: [pickup]
    produces: pickup-pack
    produce_path: out/pickup-list.md
    tool: docs/tools/spreadsheet.md
    check: python docs/tools/checks/file-exists.py out/pickup-list.md
    on_fail: retry
    next: []
```

Starter work map. Replace tools and checks when they correct this office (use **remember**).
