# Mail Log

**When to use:** What arrived. Checks seen only — they deposit; you never endorse or move funds. Confidential stays unopened. Copy date, sender, type, and who received it from their binder or export. Do not retype account numbers. Missing recipient: flag, do not guess. Certified numbers copy only if they already write them. Postage funding is not yours. Starter mailroom notes; they still teach this shop's log and week range.

**How to run:** Open or continue a Work Item under `work-items/<id>/`. Put source files in `in/`. Walk one ready YAML step (or the whole named job if requested): read the named tool doc, produce the file, run the check, then **journal-keeper**.

**Initial phase:** `role-job`

## Work map

```yaml
id: mail-log
steps:
  - id: log
    needs: []
    produces: mail-raw
    produce_path: work/mail-log.csv
    tool: docs/tools/mail-log.md
    check: python docs/tools/checks/csv-has-columns.py work/mail-log.csv date sender
    on_fail: retry
    next: [pack]
  - id: pack
    needs: [mail-raw]
    produces: mail-pack
    produce_path: out/mail-log.md
    tool: docs/tools/mail-log.md
    check: python docs/tools/checks/file-exists.py out/mail-log.md
    on_fail: retry
    next: []
```

Starter work map. Replace tools and checks when they correct this shop.
