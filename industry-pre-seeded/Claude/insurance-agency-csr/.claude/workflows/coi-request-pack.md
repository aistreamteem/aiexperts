# COI Request Pack

**When to use:** Assemble one certificate request: holder as written, job or contract name, and the COI form they use. Pull limits and policy numbers only from the dec or AMS fields already on file. Flag additional-insured or waiver wording that is not on the endorsement file. Do not say they are covered. Do not sign. They issue. Missing dec or missing holder legal name stays an ask, not a guess.

**How to run:** workflow-selector if this Work Item has no Workflow type yet. Follow the map below: read the named tool doc, write the produced file under `work-items/<id>/`, run the check from that folder, then journal-keeper. Paths `work/` and `out/` are relative to the Work Item. One ready step per continue (or the whole named job if requested).

**Initial phase:** `role-job`

## Work map

```yaml
id: coi-request-pack
steps:
  - id: holders
    needs: []
    produces: holders
    produce_path: work/holders.csv
    tool: docs/tools/certificate-holder-list.md
    check: python docs/tools/checks/csv-has-columns.py work/holders.csv holder
    on_fail: retry
    next: [form]
  - id: form
    needs: [holders]
    produces: coi-req
    produce_path: work/coi-request.csv
    tool: docs/tools/coi-form.md
    check: python docs/tools/checks/file-exists.py work/coi-request.csv
    on_fail: retry
    next: [pack]
  - id: pack
    needs: [holders, coi-req]
    produces: coi-pack
    produce_path: out/coi-request-pack.md
    tool: docs/tools/coi-form.md
    check: python docs/tools/checks/file-exists.py out/coi-request-pack.md
    on_fail: retry
    next: []
```

Starter work map. Replace tools and checks when they **remember** how *this* agency files.
