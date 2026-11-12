# Renter COI Missing

**When to use:** Compare commercial or flagged contracts to the renter COI folder. List missing, expired, or name-mismatch certificates using only their checklist fields. Do not give a coverage opinion and do not invent a limit. Waiver or RPP does not replace COI unless their policy file says so. They hold the reservation or they waive in writing. Produce the missing list and pack. No insurer-portal password and no card PAN.

**How to run:** Open or continue a Work Item under `work-items/<id>/`. Follow this file one ready step (or the whole named job if requested). Read the named tool under `docs/tools/`. Write artifacts under this Work Item (`work/` and `out/` mean `work-items/<id>/work/` and `work-items/<id>/out/`). Run the step check against those paths. After each step, run **journal-keeper**. If a required file or shop rule is missing, ask (**operator-qa** when the answer would change the pack). Do not invent rates, meters, serials, zones, deposits, or fees.

**Initial phase:** `role-job`

## Work map

```yaml
id: renter-coi-missing
steps:
  - id: coi
    needs: []
    produces: cois
    produce_path: work/renter-cois.csv
    tool: docs/tools/renter-coi-folder.md
    check: python docs/tools/checks/file-exists.py work/renter-cois.csv
    on_fail: retry
    next: [contracts]
  - id: contracts
    needs: [cois]
    produces: contracts
    produce_path: work/contracts.csv
    tool: docs/tools/contract-pdf-folder.md
    check: python docs/tools/checks/file-exists.py work/contracts.csv
    on_fail: retry
    next: [pack]
  - id: pack
    needs: [cois, contracts]
    produces: coi-pack
    produce_path: out/renter-coi-missing.md
    tool: docs/tools/spreadsheet.md
    check: python docs/tools/checks/file-exists.py out/renter-coi-missing.md
    on_fail: retry
    next: []
```

Starter work map. Replace tools and checks when the operator confirms this yard's process (save with **remember**).
