# Weigh Ticket Pack

**When to use:** Index scale slips they stored: tare, gross, net, unit, date. Never invent a pound. Say which slip is missing if only one side is present. If a survey weight disagrees, list both and keep the ticket as the weight field when their rule says ticket wins. They send the truck back to the scale if needed. You pack slips, the job row, and questions. No DOT weighing opinion.

**How to run:** This file is the instruction. After **workflow-selector** records this job:

1. Confirm `work-items/<id>/` exists. Operator scale slips go in `in/`.
2. For the next ready step, read the named tool under `docs/tools/`.
3. Write the artifact inside the Work Item folder.
4. Run the check from the Work Item folder. Exit 0 = pass. On fail, retry at most 3 times, then ask.
5. **journal-keeper**. One ready step per **continue** unless they asked for the whole job.

**Human gates:** Operator sends the truck back to the scale if a slip is missing. You never invent a pound.

**Initial phase:** `role-job` (method phase: load-docs)

## Work map

```yaml
id: weigh-ticket-pack
steps:
  - id: tickets
    needs: []
    produces: tickets
    produce_path: work/weigh-tickets.md
    tool: docs/tools/weigh-ticket-folder.md
    check: python docs/tools/checks/file-exists.py work/weigh-tickets.md
    on_fail: retry
    next: [jobs]
  - id: jobs
    needs: [tickets]
    produces: jobs
    produce_path: work/jobs.csv
    tool: docs/tools/spreadsheet.md
    check: python docs/tools/checks/csv-has-columns.py work/jobs.csv job date
    on_fail: retry
    next: [pack]
  - id: pack
    needs: [tickets, jobs]
    produces: weigh-pack
    produce_path: out/weigh-ticket-pack.md
    tool: docs/tools/spreadsheet.md
    check: python docs/tools/checks/file-exists.py out/weigh-ticket-pack.md
    on_fail: retry
    next: []
```

Starter work map. Replace tools and checks when the operator confirms how *this* shop files.
