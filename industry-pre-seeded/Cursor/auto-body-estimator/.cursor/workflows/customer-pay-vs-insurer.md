# Customer-pay versus insurer

**When to use:** Split estimate lines by the pay type they coded: insurer, deductible as posted, and customer-pay. Do not roll CP into insurer totals. Do not invent a CP price or a deductible. Write-up is the split plus asks, not a card you run and not a coverage opinion. Distinct from a mechanical customer-pay-versus-policy RO pack. Deductible stays as posted, not as CP, unless they coded it that way. You do not invent a split. Write-up names the pay column. You do not store PAN to collect either side.

**How to run:** Confirm the Work Item under `work-items/<id>/`. Walk the YAML steps in this file via **continue** (one ready step, or the whole named job if requested). Read the cited `docs/tools/` file, write artifacts under this Work Item's `work/` and `out/`, run the step `check` against those paths, then **journal-keeper**.

**Initial phase:** first YAML step in this file

## Work map

```yaml
id: customer-pay-vs-insurer
steps:
  - id: est
    needs: []
    produces: est
    produce_path: work/estimate-export.csv
    tool: docs/tools/estimate-export.md
    check: python docs/tools/checks/csv-has-columns.py work/estimate-export.csv claim pay
    on_fail: retry
    next: [pack]
  - id: pack
    needs: [est]
    produces: pay-pack
    produce_path: out/customer-pay-vs-insurer.md
    tool: docs/tools/spreadsheet.md
    check: python docs/tools/checks/file-exists.py out/customer-pay-vs-insurer.md
    on_fail: retry
    next: []
```

Starter work map. Replace tools and checks when the operator corrects this shop's process (**remember**).
