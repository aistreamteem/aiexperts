# Credential Expirations

**When to use:** From their credential log and employee list, list types with expiration or issued dates on or before the pack date they asked for, plus blank dates on types they said they track. Do not invent a date or a required cert. Do not decide the license is the right class. Do not copy license numbers when dates will do. Do not write a background verdict. Write the due-and-missing list and a pack. They decide who may still be sent.

**How to run:** Open or continue a Work Item under `work-items/<id>/`. Put credential log and employee list in `in/`. Read this file and the named `docs/tools/` doc. Walk one ready YAML step (or the whole job if requested): produce the file under this Work Item’s `work/` or `out/`, run the check, then journal-keeper. Do not skip a step with a chat summary.

**Initial phase:** `role-job`

## Work map

```yaml
id: credential-expirations
steps:
  - id: creds
    needs: []
    produces: creds
    produce_path: work/credentials.csv
    tool: docs/tools/credential-log.md
    check: python docs/tools/checks/csv-has-columns.py work/credentials.csv name date
    on_fail: retry
    next: [people]
  - id: people
    needs: [creds]
    produces: people
    produce_path: work/employee-list.csv
    tool: docs/tools/employee-list.md
    check: python docs/tools/checks/file-exists.py work/employee-list.csv
    on_fail: retry
    next: [pack]
  - id: pack
    needs: [creds, people]
    produces: cred-pack
    produce_path: out/credential-expirations.md
    tool: docs/tools/spreadsheet.md
    check: python docs/tools/checks/file-exists.py out/credential-expirations.md
    on_fail: retry
    next: []
```

Starter work map. Replace tools and checks when they correct this shop.
