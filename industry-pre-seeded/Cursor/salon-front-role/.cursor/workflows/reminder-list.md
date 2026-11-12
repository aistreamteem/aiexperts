# Reminder List

**When to use:** Build a list of guests due a confirmation or reminder from their export. They send the messages. Do not mail or SMS from this folder. Include bounce or failed-delivery rows if the export has them. Guest labels stay thin unless they asked for the contact column they already export—and they still send. This is a list, not a CRM product. Stop before send. Starter until they teach this shop’s reminder report.

**How to run:** Open or continue a Work Item under `work-items/<id>/`. Put source files in that item's `in/`. Walk one ready YAML step (or the whole named job if requested): produce the file, run the check, then **journal-keeper**. Paths `in/`, `work/`, `out/`, and `evidence/` are inside that Work Item.

**Initial phase:** `role-job`

## Work map

```yaml
id: reminder-list
steps:
  - id: pull
    needs: []
    produces: remind
    produce_path: work/reminder-due.csv
    tool: docs/tools/reminder-list.md
    check: python docs/tools/checks/csv-has-columns.py work/reminder-due.csv guest start
    on_fail: retry
    next: [pack]
  - id: pack
    needs: [remind]
    produces: remind-pack
    produce_path: out/reminder-list.md
    tool: docs/tools/reminder-list.md
    check: python docs/tools/checks/file-exists.py out/reminder-list.md
    on_fail: retry
    next: []
```

Starter work map. Replace tools and checks when the operator corrects this shop (**remember**).
