# COI Request Pack

**When to use:** Assemble one certificate request: holder as written, job or contract name, and the COI form they use. Pull limits and policy numbers only from the dec or AMS fields already on file. Flag additional-insured or waiver wording that is not on the endorsement file. Do not say they are covered. Do not sign. They issue. Missing dec or missing holder legal name stays an ask, not a guess.

**How to run:** Open or continue a Work Item under `work-items/<id>/`. Put AMS exports and PDFs in `in/`. Read this file and the named `docs/tools/` doc. Walk one ready YAML step (or the whole job if requested): produce the file under this Work Item’s `work/` or `out/`, run the check, then journal-keeper. Do not skip a step with a chat summary.

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

Starter work map. Replace tools and checks when the operator corrects this shop (remember / integrate-docs).
