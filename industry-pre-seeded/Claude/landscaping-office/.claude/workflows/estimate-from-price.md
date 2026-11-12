# Estimate From Price

**When to use:** Draft estimate lines from their price file and the proposal or takeoff they stored. Quantity they listed times unit price they listed. Blank price or blank qty: ask. Do not invent dump fees, hours, or a wage. Do not promise plant survival. Label the pack draft until they accept. They send the proposal. You do not treat the draft as sold work on a crew day.

**How to run:** Open or continue a Work Item under `work-items/<id>/`. Follow this file's steps in order. Read the cited tool doc, write artifacts under that Work Item's `work/` and `out/`, run the listed check against those same paths, then **journal-keeper**. Do not invent a missing ticket, price, or weather call — ask with **operator-qa**.

**Initial phase:** `role-job`

## Work map

```yaml
id: estimate-from-price
steps:
  - id: price
    needs: []
    produces: price
    produce_path: work/price-file.csv
    tool: docs/tools/price-file.md
    check: python docs/tools/checks/csv-has-columns.py work/price-file.csv item price
    on_fail: retry
    next: [proposal]
  - id: proposal
    needs: [price]
    produces: proposal
    produce_path: work/proposal.pdf
    tool: docs/tools/proposal-pdf.md
    check: python docs/tools/checks/file-exists.py work/proposal.pdf
    on_fail: retry
    next: [pack]
  - id: pack
    needs: [price, proposal]
    produces: estimate-pack
    produce_path: out/estimate.md
    tool: docs/tools/spreadsheet.md
    check: python docs/tools/checks/file-exists.py out/estimate.md
    on_fail: retry
    next: []
```

Starter work map. Replace tools and checks when they correct shop practice (**remember** / **integrate-docs**).
