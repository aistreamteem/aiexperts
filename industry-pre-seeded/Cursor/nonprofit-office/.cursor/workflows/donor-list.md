# Donor CSV list (they communicate)

**When to use:** Filter the donor export they provided. List holes: missing fund or restriction code, missing acknowledgment flag, pledges mixed with cash, duplicate IDs. They communicate. No email, SMS, or CRM blast. Do not mark sent because you drafted a letter. Soft credit stays as their sheet defines it; do not move hard credit. Least PII in the pack. Output is the working CSV and a list they can use in their own tools. Segmentation is a filter, not a send. Employer-stack messaging is out of scope.

**How to run:** Open or continue the Work Item under `work-items/<id>/`. Walk one ready YAML step (or the whole named job if requested): produce the file, run the check, then journal-keeper.

**Initial phase:** `role-job`

## Work map

```yaml
id: donor-list
steps:
  - id: pull
    needs: []
    produces: donors
    produce_path: work/donors.csv
    tool: docs/tools/donor-csv.md
    check: python docs/tools/checks/csv-has-columns.py work/donors.csv date amount
    on_fail: retry
    next: [pack]
  - id: pack
    needs: [donors]
    produces: donor-out
    produce_path: out/donor-list.md
    tool: docs/tools/donor-csv.md
    check: python docs/tools/checks/file-exists.py out/donor-list.md
    on_fail: retry
    next: []
```

Starter work map. Replace tools and checks when they correct how this shop works (**remember**).
