# Rate From File

**When to use:** Tabulate street, web, in-place, and promo rates from the rate file they saved. Blank cells stay blank and become asks. Do not invent a size band or a first-month special. Expired promos stay labeled expired. If the occupancy export shows a different in-place rate, quote both. Tax stays on their tax file. They approve any number they will say. You do not send a rate letter.

**How to run:** Open or continue a Work Item under `work-items/<id>/`. Put the rate file in `in/`. Read this file and `docs/tools/rate-file.md`. Walk one ready YAML step (or the whole job if requested): produce the file under this Work Item’s `work/` or `out/`, run the check, then journal-keeper. Do not skip a step with a chat summary.

**Initial phase:** `role-job`

## Work map

```yaml
id: rate-from-file
steps:
  - id: rates
    needs: []
    produces: rates
    produce_path: work/rates.csv
    tool: docs/tools/rate-file.md
    check: python docs/tools/checks/csv-has-columns.py work/rates.csv size rate
    on_fail: retry
    next: [pack]
  - id: pack
    needs: [rates]
    produces: rate-pack
    produce_path: out/rates.md
    tool: docs/tools/rate-file.md
    check: python docs/tools/checks/file-exists.py out/rates.md
    on_fail: retry
    next: []
```

Starter work map. Replace tools and checks when the operator corrects this shop via **remember**.
