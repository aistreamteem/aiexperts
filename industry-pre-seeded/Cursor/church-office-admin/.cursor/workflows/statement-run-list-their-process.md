# Statement run list from their process

**When to use:** Read their statement-process file first. Then list households or gift rows the process includes from the giving export they named. Do not invent who is on the run. Do not invent a deductible total. Do not send email or SMS. Flag open batches, missing funds, and missing mail names only if their process requires those fields. Write-up is a run list plus holes. They review and they send.

**How to run:** Open or continue the Work Item under `work-items/<id>/`. Walk one ready YAML step (or the whole named job if requested): produce the file, run the check, then journal-keeper.

**Initial phase:** `role-job`

## Work map

```yaml
id: statement-run-list-their-process
steps:
  - id: process
    needs: []
    produces: process
    produce_path: work/statement-process.md
    tool: docs/tools/statement-process-file.md
    check: python docs/tools/checks/file-exists.py work/statement-process.md
    on_fail: retry
    next: [export]
  - id: export
    needs: [process]
    produces: gifts
    produce_path: work/giving-export.csv
    tool: docs/tools/giving-export.md
    check: python docs/tools/checks/csv-has-columns.py work/giving-export.csv amount fund
    on_fail: retry
    next: [pack]
  - id: pack
    needs: [process, gifts]
    produces: statement-pack
    produce_path: out/statement-run-list.md
    tool: docs/tools/spreadsheet.md
    check: python docs/tools/checks/file-exists.py out/statement-run-list.md
    on_fail: retry
    next: []
```

Starter work map. Replace tools and checks when they correct this shop (**remember**).
