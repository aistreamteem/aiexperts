# Background dates as file

**When to use:** From the volunteer roster, list background dates and their status words next to roles their policy PDF tags as date-required. Do not say anyone is cleared or safe. Do not invent a renewal law. Do not store a full report or an SSN. Missing dates on tagged roles stay flags. Write-up is dates versus roles, not a verdict. They talk to the person.

**How to run:** Open or continue the Work Item under `work-items/<id>/`. Walk one ready YAML step (or the whole named job if requested): produce the file, run the check, then journal-keeper.

**Initial phase:** `role-job`

## Work map

```yaml
id: background-dates-as-file
steps:
  - id: policy
    needs: []
    produces: policy
    produce_path: work/child-policy.md
    tool: docs/tools/handbook-or-policy-pdf.md
    check: python docs/tools/checks/file-exists.py work/child-policy.md
    on_fail: retry
    next: [roster]
  - id: roster
    needs: [policy]
    produces: roster
    produce_path: work/volunteer-roster.csv
    tool: docs/tools/volunteer-roster.md
    check: python docs/tools/checks/csv-has-columns.py work/volunteer-roster.csv volunteer ministry
    on_fail: retry
    next: [pack]
  - id: pack
    needs: [policy, roster]
    produces: bg-pack
    produce_path: out/background-dates.md
    tool: docs/tools/spreadsheet.md
    check: python docs/tools/checks/file-exists.py out/background-dates.md
    on_fail: retry
    next: []
```

Starter work map. Replace tools and checks when they correct this shop (**remember**).
