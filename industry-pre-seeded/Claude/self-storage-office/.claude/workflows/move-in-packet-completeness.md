# Move In Packet Completeness

**When to use:** Check the agreement folder against their move-in checklist: agreement PDF, rate from the rate file, ID present under min-necessary, insurance form or waiver if they require it. Do not invent a prorate, promo, or tax. Do not write a gate code. If the unit is still occupied or auction-hold on occupancy, flag the clash. Unsigned drafts stay drafts. They take payment and they issue access. You list present-or-missing.

**How to run:** Open or continue a Work Item under `work-items/<id>/`. Put agreement PDFs and the rate file in `in/`. Read this file and `docs/tools/agreement-pdf-folder.md` / `docs/tools/rate-file.md`. Walk one ready YAML step (or the whole job if requested): produce the file under this Work Item’s `work/` or `out/`, run the check, then journal-keeper. Do not skip a step with a chat summary.

**Initial phase:** `role-job`

## Work map

```yaml
id: move-in-packet-completeness
steps:
  - id: agreements
    needs: []
    produces: agreements
    produce_path: work/agreements-index.csv
    tool: docs/tools/agreement-pdf-folder.md
    check: python docs/tools/checks/file-exists.py work/agreements-index.csv
    on_fail: retry
    next: [rates]
  - id: rates
    needs: [agreements]
    produces: rates
    produce_path: work/rates.csv
    tool: docs/tools/rate-file.md
    check: python docs/tools/checks/file-exists.py work/rates.csv
    on_fail: retry
    next: [pack]
  - id: pack
    needs: [agreements, rates]
    produces: move-in-pack
    produce_path: out/move-in-packet.md
    tool: docs/tools/agreement-pdf-folder.md
    check: python docs/tools/checks/file-exists.py out/move-in-packet.md
    on_fail: retry
    next: []
```

Starter work map. Replace tools and checks when the operator corrects this shop via **remember**.
