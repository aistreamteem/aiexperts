# FNOL Routing

**When to use:** From their claim log and the loss-notice PDFs, list date of loss, policy number, missing required fields, and where the file says to send the notice. Do not invent a narrative. Do not adjust, set reserve, or say they are covered. When a claim number returns, add it exactly. After-hours contacts come only from their carrier-contact file. They or the carrier own the claim. You route and you log.

**How to run:** Open or continue a Work Item under `work-items/<id>/`. Put AMS exports and PDFs in `in/`. Read this file and the named `docs/tools/` doc. Walk one ready YAML step (or the whole job if requested): produce the file under this Work Item’s `work/` or `out/`, run the check, then journal-keeper. Do not skip a step with a chat summary.

**Initial phase:** `role-job`

## Work map

```yaml
id: fnol-routing
steps:
  - id: log
    needs: []
    produces: claims
    produce_path: work/claims.csv
    tool: docs/tools/claim-log.md
    check: python docs/tools/checks/csv-has-columns.py work/claims.csv date_of_loss policy
    on_fail: retry
    next: [pack]
  - id: pack
    needs: [claims]
    produces: fnol-pack
    produce_path: out/fnol-routing.md
    tool: docs/tools/claim-log.md
    check: python docs/tools/checks/file-exists.py out/fnol-routing.md
    on_fail: retry
    next: []
```

Starter work map. Replace tools and checks when the operator corrects this shop (remember / integrate-docs).
