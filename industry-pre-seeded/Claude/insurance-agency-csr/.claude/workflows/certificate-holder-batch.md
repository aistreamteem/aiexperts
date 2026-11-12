# Certificate Holder Batch

**When to use:** Batch the holder list against their COI form for one client or job list they named. Keep legal names exact. Pull policy numbers and limits only from files already in the folder. Flag AI or waiver asks that the endorsement file does not support. Do not issue live certificates and do not say anyone is covered. One pack plus a request CSV. They issue from AMS. Repeat holders stay as the library shows, not cleaned up.

**How to run:** workflow-selector if this Work Item has no Workflow type yet. Follow the map below: read the named tool doc, write the produced file under `work-items/<id>/`, run the check from that folder, then journal-keeper. Paths `work/` and `out/` are relative to the Work Item. One ready step per continue (or the whole named job if requested).

**Initial phase:** `role-job`

## Work map

```yaml
id: certificate-holder-batch
steps:
  - id: list
    needs: []
    produces: holders
    produce_path: work/holders.csv
    tool: docs/tools/certificate-holder-list.md
    check: python docs/tools/checks/csv-has-columns.py work/holders.csv holder
    on_fail: retry
    next: [form]
  - id: form
    needs: [holders]
    produces: batch
    produce_path: work/coi-batch.csv
    tool: docs/tools/coi-form.md
    check: python docs/tools/checks/file-exists.py work/coi-batch.csv
    on_fail: retry
    next: [pack]
  - id: pack
    needs: [holders, batch]
    produces: holder-pack
    produce_path: out/holder-batch.md
    tool: docs/tools/certificate-holder-list.md
    check: python docs/tools/checks/file-exists.py out/holder-batch.md
    on_fail: retry
    next: []
```

Starter work map. Replace tools and checks when they **remember** how *this* agency files.
