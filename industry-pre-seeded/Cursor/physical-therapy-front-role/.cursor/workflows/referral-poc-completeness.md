# Referral and plan-of-care completeness

**When to use:** From the referral folder, list inbound scripts and plans of care as complete or missing named pages and physician signature as their form requires. Copy auth numbers only if already printed. Do not add a diagnosis and do not write the plan. Expired dates on their rule stay flagged. Do not copy extra referring notes into docs/ when a present-or-missing row will do. Match to the day list when they asked which of today’s evals still lack a packet. They send. You pack the completeness list plus a write-up.

**How to run:** Open or reuse `work-items/<id>/`. Put source files in `in/`. Follow this map in order: read the named `docs/tools/` file, write `produce_path` inside this Work Item, run the step `check`, retry at most 3 times on fail then ask. Pass produced files to the next step. One ready step per continue unless the operator asked for the whole job. Then journal-keeper.

**Initial phase:** `role-job`

## Work map

```yaml
id: referral-poc-completeness
steps:
  - id: refs
    needs: []
    produces: refs
    produce_path: work/referrals.csv
    tool: docs/tools/referral-folder.md
    check: python docs/tools/checks/file-exists.py work/referrals.csv
    on_fail: retry
    next: [day]
  - id: day
    needs: [refs]
    produces: day
    produce_path: work/day-list.csv
    tool: docs/tools/schedule-csv.md
    check: python docs/tools/checks/file-exists.py work/day-list.csv
    on_fail: retry
    next: [write]
  - id: write
    needs: [refs, day]
    produces: ref-writeup
    produce_path: out/referral-poc.md
    tool: docs/tools/spreadsheet.md
    check: python docs/tools/checks/file-exists.py out/referral-poc.md
    on_fail: retry
    next: []
```

Starter work map. Replace tools and checks when the operator confirms how this clinic works.
