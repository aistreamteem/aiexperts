# Endorsement Request List

**When to use:** List open policy-change requests from their endorsement sheet: type, requested effective date, and supporting-doc present or missing. Do not mark issued without an endorsement PDF or their issued AMS code. Do not backdate. Do not invent VIN, driver, or location fields. Vehicle, driver, and location adds stay separate rows. They submit. You keep the open list and the pack summary. Producer questions stay labeled as questions.

**How to run:** workflow-selector if this Work Item has no Workflow type yet. Follow the map below: read the named tool doc, write the produced file under `work-items/<id>/`, run the check from that folder, then journal-keeper. Paths `work/` and `out/` are relative to the Work Item. One ready step per continue (or the whole named job if requested).

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

Starter work map. Replace tools and checks when they **remember** how *this* agency files.
