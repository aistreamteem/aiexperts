# Missing Dec Pages

**When to use:** Compare the AMS policy list to the dec-page folder. List issued or in-force rows with no current-term dec PDF. Do not invent limits to stand in for a missing dec. Do not say those policies are covered. Pending new business without a number stays pending, not missing-dec, unless they asked you to treat binder files as the stand-in and the binder is also missing. They pull decs. You keep the gap list.

**How to run:** Open or continue a Work Item under `work-items/<id>/`. Put AMS exports and PDFs in `in/`. Read this file and the named `docs/tools/` doc. Walk one ready YAML step (or the whole job if requested): produce the file under this Work Item’s `work/` or `out/`, run the check, then journal-keeper. Do not skip a step with a chat summary.

**Initial phase:** `role-job`

## Work map

```yaml
id: missing-dec-pages
steps:
  - id: ams
    needs: []
    produces: ams
    produce_path: work/ams-policies.csv
    tool: docs/tools/ams-export.md
    check: python docs/tools/checks/csv-has-columns.py work/ams-policies.csv policy
    on_fail: retry
    next: [dec]
  - id: dec
    needs: [ams]
    produces: dec
    produce_path: work/dec-index.csv
    tool: docs/tools/dec-page-folder.md
    check: python docs/tools/checks/file-exists.py work/dec-index.csv
    on_fail: retry
    next: [pack]
  - id: pack
    needs: [ams, dec]
    produces: dec-pack
    produce_path: out/missing-dec-pages.md
    tool: docs/tools/dec-page-folder.md
    check: python docs/tools/checks/file-exists.py out/missing-dec-pages.md
    on_fail: retry
    next: []
```

Starter work map. Replace tools and checks when the operator corrects this shop (remember / integrate-docs).
