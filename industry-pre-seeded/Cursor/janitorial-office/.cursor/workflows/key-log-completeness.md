# Key Log Completeness

**When to use:** Match issued key-ids on the key log to sites on the site list. Flag out-without-in and sites with no key row if their process requires one. Never copy a key or store a combination or alarm code. Contract-end returned lists use the issued set they stored. Write-up is outstanding rings plus questions. They collect hardware. You pack the gaps. Badge rows stay on this pack only if they keep badges on the same log.

**How to run:** Use **continue** with this workflow. Work inside `work-items/<id>/`. For each step: read the tool doc, produce the file, run the check (retry at most 3, then ask), then **journal-keeper**. Never copy a key or store a combination.

**Initial phase:** `keys`

## Work map

```yaml
id: key-log-completeness
steps:
  - id: keys
    needs: []
    produces: keys
    produce_path: work/key-log.csv
    tool: docs/tools/key-log.md
    check: python docs/tools/checks/csv-has-columns.py work/key-log.csv site key
    on_fail: retry
    next: [sites]
  - id: sites
    needs: [keys]
    produces: sites
    produce_path: work/key-sites.csv
    tool: docs/tools/site-list.md
    check: python docs/tools/checks/file-exists.py work/key-sites.csv
    on_fail: retry
    next: [pack]
  - id: pack
    needs: [keys, sites]
    produces: key-pack
    produce_path: out/key-log.md
    tool: docs/tools/spreadsheet.md
    check: python docs/tools/checks/file-exists.py out/key-log.md
    on_fail: retry
    next: []
```

Starter map. Replace tools and checks when the operator corrects this shop (**remember**).
