# Denied File Routing

**When to use:** Read their screening-status export and route rows by their code only — pending, complete, or the word they used. Do not write pass or fail. Do not decide approve or deny. Do not send or draft an adverse-action letter. Do not paste full report text into the pack. Missing codes stay missing. They decide and they or their vendor send notices.

**How to run:** Open or continue a Work Item under `work-items/<id>/`. Put the screening-status export in `in/`. Read this file and `docs/tools/screening-status-export.md`. Walk one ready YAML step (or the whole job if requested): produce the file under this Work Item’s `work/` or `out/`, run the check, then journal-keeper. Do not skip a step with a chat summary.

**Initial phase:** `role-job`

## Work map

```yaml
id: denied-file-routing
steps:
  - id: status
    needs: []
    produces: status
    produce_path: work/screening-status.csv
    tool: docs/tools/screening-status-export.md
    check: python docs/tools/checks/csv-has-columns.py work/screening-status.csv applicant status
    on_fail: retry
    next: [pack]
  - id: pack
    needs: [status]
    produces: routing-pack
    produce_path: out/screening-status-routing.md
    tool: docs/tools/screening-status-export.md
    check: python docs/tools/checks/file-exists.py out/screening-status-routing.md
    on_fail: retry
    next: []
```

Starter work map. Replace tools and checks when the operator corrects this shop (remember / integrate-docs).
