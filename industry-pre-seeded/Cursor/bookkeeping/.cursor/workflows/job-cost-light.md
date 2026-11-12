# Job Cost Light

**When to use:** Tag bills and other costs to job ids they already use for the period they name. Produce their job list, a job-costs CSV with job, amount, and category, and a write-up of untagged rows. No invented jobs, markup, or overhead rates. Owner labor only if they track it. Do not put owner draws on a job as labor. Do not treat job profit as a tax return. Ask whether labor is payroll, sub bills, or uncosted owner time. Starter tags come only from a job id already on the invoice or from their named list. They invoice the customer; you do not send invoices unless they asked.

**How to run:** Select this job with workflow-selector (or continue). Use `work-items/<id>/`. Put source files in `in/`. Walk one ready step: read the named tool doc, write the produced file under this Work Item, run the check, then journal-keeper. Do not skip a step with a chat summary. Whole named job only if they asked.

**Initial phase:** `role-job`

## Work map

```yaml
id: job-cost-light
steps:
  - id: jobs
    needs: []
    produces: job-list
    produce_path: work/job-list.csv
    tool: docs/tools/job-cost-sheet.md
    check: python docs/tools/checks/file-exists.py work/job-list.csv
    on_fail: retry
    next: [tag]
  - id: tag
    needs: [job-list]
    produces: job-costs
    produce_path: work/job-costs.csv
    tool: docs/tools/job-cost-sheet.md
    check: python docs/tools/checks/csv-has-columns.py work/job-costs.csv job amount category
    on_fail: retry
    next: [job-pack]
  - id: job-pack
    needs: [job-costs]
    produces: job-cost-writeup
    produce_path: out/job-cost.md
    tool: docs/tools/job-cost-sheet.md
    check: python docs/tools/checks/file-exists.py out/job-cost.md
    on_fail: retry
    next: []
```

Starter work map. Replace tools and checks when the operator confirms how this shop works.
