# License Watch

**When to use:** Expire dates from their tracker or certificate images. Flag past or blank. No compliance stamp and no filing with a city or carrier. Copy policy type and dates from the binder; do not pick coverage or say a claim is covered. Missing scan pages: say missing. Insurance and license rows may share the tracker if they already do. This is orientation paperwork, not a legal or payroll-tax opinion. Ask which file is current when two dates disagree.

**How to run:** Open or continue a Work Item under `work-items/<id>/`. Put source files in `in/`. Walk one ready YAML step (or the whole named job if requested): read the named tool doc, produce the file, run the check, then **journal-keeper**.

**Initial phase:** `role-job`

## Work map

```yaml
id: license-watch
steps:
  - id: pull
    needs: []
    produces: lic-raw
    produce_path: work/licenses.csv
    tool: docs/tools/license-tracker.md
    check: python docs/tools/checks/csv-has-columns.py work/licenses.csv name expire
    on_fail: retry
    next: [flag]
  - id: flag
    needs: [lic-raw]
    produces: lic-flags
    produce_path: work/license-flags.csv
    tool: docs/tools/license-tracker.md
    check: python docs/tools/checks/csv-has-columns.py work/license-flags.csv name flag
    on_fail: retry
    next: [pack]
  - id: pack
    needs: [lic-flags]
    produces: lic-pack
    produce_path: out/licenses.md
    tool: docs/tools/license-tracker.md
    check: python docs/tools/checks/file-exists.py out/licenses.md
    on_fail: retry
    next: []
```

Starter work map. Replace tools and checks when they correct this shop.
