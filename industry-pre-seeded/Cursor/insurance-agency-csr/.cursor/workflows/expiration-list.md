# Expiration List

**When to use:** Build the expiration list from their expiration CSV. Copy policy, named insured, and expiration date as exported. Do not invent an x-date and do not promise renewal. Flag rows past or inside their aging window if they named one; otherwise list dates only and label a starter window as a guess. Keep status as they coded it. They call the book. You do not bind or quote from this list.

**How to run:** Open or continue a Work Item under `work-items/<id>/`. Put AMS exports and PDFs in `in/`. Read this file and the named `docs/tools/` doc. Walk one ready YAML step (or the whole job if requested): produce the file under this Work Item’s `work/` or `out/`, run the check, then journal-keeper. Do not skip a step with a chat summary.

**Initial phase:** `role-job`

## Work map

```yaml
id: expiration-list
steps:
  - id: pull
    needs: []
    produces: exp
    produce_path: work/expirations.csv
    tool: docs/tools/expiration-csv.md
    check: python docs/tools/checks/csv-has-columns.py work/expirations.csv policy named_insured exp_date
    on_fail: retry
    next: [pack]
  - id: pack
    needs: [exp]
    produces: exp-pack
    produce_path: out/expiration-list.md
    tool: docs/tools/spreadsheet.md
    check: python docs/tools/checks/file-exists.py out/expiration-list.md
    on_fail: retry
    next: []
```

Starter work map. Replace tools and checks when the operator corrects this shop (remember / integrate-docs).
