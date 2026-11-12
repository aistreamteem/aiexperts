# Quote To Job

**When to use:** One sold estimate: parts from the PDF, schedule question, permit question. Do not schedule if not marked sold. Deposit rules are theirs; do not send money. Packing-list SKUs follow the PDF, not a usual kit. If the board already shows a crew day and the PDF still says estimate, raise that. Ask whether this job needs a permit row. Do not invent ETAs or a city number. The job pack names the PDF, the parts CSV, and open questions. Their convert-to-job marks win.

**How to run:** Open or continue a Work Item under `work-items/<id>/`. Put source files in `in/`. Walk one ready YAML step (or the whole named job if requested): produce the file, run the check, then **journal-keeper**.

**Initial phase:** `role-job`

## Work map

```yaml
id: quote-to-job
steps:
  - id: quote
    needs: []
    produces: sold-scope
    produce_path: work/sold-scope.csv
    tool: docs/tools/quote-pdf.md
    check: python docs/tools/checks/file-exists.py work/sold-scope.csv
    on_fail: retry
    next: [parts]
  - id: parts
    needs: [sold-scope]
    produces: sold-parts
    produce_path: work/sold-parts.csv
    tool: docs/tools/packing-list-sheet.md
    check: python docs/tools/checks/csv-has-columns.py work/sold-parts.csv sku qty
    on_fail: retry
    next: [sched-ask]
  - id: sched-ask
    needs: [sold-parts]
    produces: sold-job-pack
    produce_path: out/sold-job.md
    tool: docs/tools/schedule-sheet.md
    check: python docs/tools/checks/file-exists.py out/sold-job.md
    on_fail: retry
    next: []
```

Starter work map. Replace tools and checks when they correct this shop (**remember**).
