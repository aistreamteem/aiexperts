# Referral Paperwork

**When to use:** From the referral PDF folder, list inbound and outbound packets as complete or missing named pages. Copy auth numbers only if already printed. Do not pick a specialist as care, do not add a diagnosis, and do not write a clinical argument. Expired dates on their rule stay flagged. Do not copy extra referring notes into docs/ when a present-or-missing row will do. They send. You pack the completeness list plus a write-up.

**How to run:** Open or continue a Work Item under `work-items/<id>/`. Follow this file's steps in order. Read the named tool doc, write artifacts under this Work Item's `work/` and `out/`, then run **journal-keeper**.

**Initial phase:** `role-job`

## Work map

```yaml
id: referral-paperwork
steps:
  - id: refs
    needs: []
    produces: refs
    produce_path: work/referrals.csv
    tool: docs/tools/referral-pdf-folder.md
    check: python docs/tools/checks/file-exists.py work/referrals.csv
    on_fail: retry
    next: [day]
  - id: day
    needs: [refs]
    produces: day
    produce_path: work/day-list.csv
    tool: docs/tools/day-list-csv.md
    check: python docs/tools/checks/file-exists.py work/day-list.csv
    on_fail: retry
    next: [write]
  - id: write
    needs: [refs, day]
    produces: ref-writeup
    produce_path: out/referral-check.md
    tool: docs/tools/spreadsheet.md
    check: python docs/tools/checks/file-exists.py out/referral-check.md
    on_fail: retry
    next: []
```

Starter work map. Replace tools and checks when the operator confirms how this clinic files.
