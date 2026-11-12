# Late Rent List

**When to use:** Take balances from the roll or aging export they name. Add questions on partials, NSF reversals, and whether they accept plans — their SOP, not a plan you invent. No pay-or-quit text, no court advice, no lockout language. Do not apply a late fee they did not configure and do not delete an NSF receipt to clean the list. They or counsel send any legal notice. You never collect a card or move deposit cash to cover a balance.

**How to run:** Open or continue a Work Item under `work-items/<id>/`. Put source files in `in/`. Walk one ready YAML step (or the whole named job if requested): produce the file, run the check, then **journal-keeper**. Paths `work/` and `out/` are inside that Work Item.

**Initial phase:** `role-job`

## Work map

```yaml
id: late-rent-list
steps:
  - id: roll
    needs: []
    produces: late-raw
    produce_path: work/late-rent-raw.csv
    tool: docs/tools/rent-roll-export.md
    check: python docs/tools/checks/file-exists.py work/late-rent-raw.csv
    on_fail: retry
    next: [status]
  - id: status
    needs: [late-raw]
    produces: late-status
    produce_path: work/late-rent-status.csv
    tool: docs/tools/rent-roll-export.md
    check: python docs/tools/checks/csv-has-columns.py work/late-rent-status.csv unit balance status
    on_fail: retry
    next: [late-pack]
  - id: late-pack
    needs: [late-status]
    produces: late-questions
    produce_path: out/late-rent.md
    tool: docs/tools/spreadsheet.md
    check: python docs/tools/checks/file-exists.py out/late-rent.md
    on_fail: retry
    next: []
```

Starter work map. Replace tools and checks when they correct this shop (use **remember**).
