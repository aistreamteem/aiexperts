# Minutes index

**When to use:** Index meeting dates and draft versus adopted from their minutes folder. Do not edit adopted minutes in place. Do not promote a draft to adopted. Do not invent attendance or votes. Committee files stay labeled committee. Least PII in the index. Missing adopted minutes for a calendar date are holes. Output is the index CSV and a pack the next board pack can use. They adopt minutes. You label and list. A corrections process, if they have one, comes from their policy file—not from a silent overwrite.

**How to run:** Open or continue the Work Item under `work-items/<id>/`. Walk one ready YAML step (or the whole named job if requested): produce the file, run the check, then journal-keeper.

**Initial phase:** `role-job`

## Work map

```yaml
id: minutes-index
steps:
  - id: list
    needs: []
    produces: minutes
    produce_path: work/minutes-index.csv
    tool: docs/tools/minutes-folder.md
    check: python docs/tools/checks/file-exists.py work/minutes-index.csv
    on_fail: retry
    next: [pack]
  - id: pack
    needs: [minutes]
    produces: min-out
    produce_path: out/minutes-index.md
    tool: docs/tools/minutes-folder.md
    check: python docs/tools/checks/file-exists.py out/minutes-index.md
    on_fail: retry
    next: []
```

Starter work map. Replace tools and checks when they correct how this shop works (**remember**).
