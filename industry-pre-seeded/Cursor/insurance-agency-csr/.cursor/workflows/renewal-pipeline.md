# Renewal Pipeline

**When to use:** Join their AMS export to the expiration CSV. Keep producer, CSR, line, and status as they coded it. Do not invent a renewal premium or a will-renew outcome. Remarket rows stay remarket, not quoted, until a producer quote PDF exists. Missing apps or decs are completeness rows. You do not bind the renewal. They chase. Label any starter stage names as starter if their codes differ.

**How to run:** Open or continue a Work Item under `work-items/<id>/`. Put AMS exports and PDFs in `in/`. Read this file and the named `docs/tools/` doc. Walk one ready YAML step (or the whole job if requested): produce the file under this Work Item’s `work/` or `out/`, run the check, then journal-keeper. Do not skip a step with a chat summary.

**Initial phase:** `role-job`

## Work map

```yaml
id: renewal-pipeline
steps:
  - id: ams
    needs: []
    produces: ams
    produce_path: work/ams-policies.csv
    tool: docs/tools/ams-export.md
    check: python docs/tools/checks/csv-has-columns.py work/ams-policies.csv policy named_insured
    on_fail: retry
    next: [exp]
  - id: exp
    needs: [ams]
    produces: exp
    produce_path: work/expirations.csv
    tool: docs/tools/expiration-csv.md
    check: python docs/tools/checks/file-exists.py work/expirations.csv
    on_fail: retry
    next: [pack]
  - id: pack
    needs: [ams, exp]
    produces: renew-pack
    produce_path: out/renewal-pipeline.md
    tool: docs/tools/spreadsheet.md
    check: python docs/tools/checks/file-exists.py out/renewal-pipeline.md
    on_fail: retry
    next: []
```

Starter work map. Replace tools and checks when the operator corrects this shop (remember / integrate-docs).
