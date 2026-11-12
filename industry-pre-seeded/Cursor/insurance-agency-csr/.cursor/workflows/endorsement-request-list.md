# Endorsement Request List

**When to use:** List open policy-change requests from their endorsement sheet: type, requested effective date, and supporting-doc present or missing. Do not mark issued without an endorsement PDF or their issued AMS code. Do not backdate. Do not invent VIN, driver, or location fields. Vehicle, driver, and location adds stay separate rows. They submit. You keep the open list and the pack summary. Producer questions stay labeled as questions.

**How to run:** Open or continue a Work Item under `work-items/<id>/`. Put AMS exports and PDFs in `in/`. Read this file and the named `docs/tools/` doc. Walk one ready YAML step (or the whole job if requested): produce the file under this Work Item’s `work/` or `out/`, run the check, then journal-keeper. Do not skip a step with a chat summary.

**Initial phase:** `role-job`

## Work map

```yaml
id: endorsement-request-list
steps:
  - id: sheet
    needs: []
    produces: endorsements
    produce_path: work/endorsements.csv
    tool: docs/tools/endorsement-sheet.md
    check: python docs/tools/checks/csv-has-columns.py work/endorsements.csv request_type effective_date
    on_fail: retry
    next: [pack]
  - id: pack
    needs: [endorsements]
    produces: end-pack
    produce_path: out/endorsement-list.md
    tool: docs/tools/spreadsheet.md
    check: python docs/tools/checks/file-exists.py out/endorsement-list.md
    on_fail: retry
    next: []
```

Starter work map. Replace tools and checks when the operator corrects this shop (remember / integrate-docs).
