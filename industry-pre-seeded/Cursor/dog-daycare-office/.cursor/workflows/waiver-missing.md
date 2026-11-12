# Waiver Missing

**When to use:** From the waiver folder and the stay list, list dogs whose waiver is unsigned, undated, wrong version, or missing pages. Do not give a legal opinion. Do not skip a trial day unless they wrote an exception. Photo-release pages are separate if their packet splits them. A complete waiver is not a medical clearance. Starter / guess until they teach the current version and e-sign rules.

**How to run:** Open or continue a Work Item under `work-items/<id>/`. Put source files in `in/`. Walk one ready YAML step (or the whole named job if requested): read the named tool doc, produce the file, run the check, then **journal-keeper**.

**Initial phase:** `role-job`

## Work map

```yaml
id: waiver-missing
steps:
  - id: folder
    needs: []
    produces: waivers
    produce_path: work/waivers.csv
    tool: docs/tools/waiver-folder.md
    check: python docs/tools/checks/csv-has-columns.py work/waivers.csv patient file
    on_fail: retry
    next: [stays]
  - id: stays
    needs: [waivers]
    produces: stays
    produce_path: work/boarding.csv
    tool: docs/tools/boarding-csv.md
    check: python docs/tools/checks/csv-has-columns.py work/boarding.csv patient stay
    on_fail: retry
    next: [write]
  - id: write
    needs: [waivers, stays]
    produces: waiver-pack
    produce_path: out/waiver-missing.md
    tool: docs/tools/waiver-folder.md
    check: python docs/tools/checks/file-exists.py out/waiver-missing.md
    on_fail: retry
    next: []
```

Starter work map. Replace tools and checks when they correct this shop.
