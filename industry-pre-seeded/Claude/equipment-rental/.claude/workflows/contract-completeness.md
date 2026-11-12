# Contract Completeness

**When to use:** Read contract PDFs against their required fields: renter, unit or serial, dates, rate lines from the rate file, waiver or RPP box, tax or exempt cert pointer, PO if the account needs one, and COI if required. Do not invent a rate, tax, or deposit. Draft is not signed out. Blank required fields become asks. No PAN copied from a scan. Produce the missing-fields list and pack. They sign and they collect.

**How to run:** Open or continue a Work Item under `work-items/<id>/`. Follow this file one ready step (or the whole named job if requested). Read the named tool under `docs/tools/`. Write artifacts under this Work Item (`work/` and `out/` mean `work-items/<id>/work/` and `work-items/<id>/out/`). Run the step check against those paths. After each step, run **journal-keeper**. If a required file or shop rule is missing, ask (**operator-qa** when the answer would change the pack). Do not invent rates, meters, serials, zones, deposits, or fees.

**Initial phase:** `role-job`

## Work map

```yaml
id: contract-completeness
steps:
  - id: pdf
    needs: []
    produces: contracts
    produce_path: work/contracts.csv
    tool: docs/tools/contract-pdf-folder.md
    check: python docs/tools/checks/file-exists.py work/contracts.csv
    on_fail: retry
    next: [rates]
  - id: rates
    needs: [contracts]
    produces: rates
    produce_path: work/rate-file.csv
    tool: docs/tools/rate-file.md
    check: python docs/tools/checks/file-exists.py work/rate-file.csv
    on_fail: retry
    next: [pack]
  - id: pack
    needs: [contracts, rates]
    produces: contract-pack
    produce_path: out/contract-completeness.md
    tool: docs/tools/spreadsheet.md
    check: python docs/tools/checks/file-exists.py out/contract-completeness.md
    on_fail: retry
    next: []
```

Starter work map. Replace tools and checks when the operator confirms this yard's process (save with **remember**).
