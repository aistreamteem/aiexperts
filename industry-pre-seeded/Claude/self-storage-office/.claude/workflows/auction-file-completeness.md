# Auction File Completeness

**When to use:** Compare their auction checklist to files in the folder: notices, certified-mail log, inventory form, photos, calendar date, buyer log. Mark missing in those words. Do not invent a sale date or a bid. Do not say they may auction or that a lien attached. Completeness is not permission to sell. Late-list membership is not an auction file. They and their counsel decide. You write the gap pack only.

**How to run:** Open or continue a Work Item under `work-items/<id>/`. Put their auction checklist and unit files in `in/`. Read this file and `docs/tools/auction-checklist.md` / `docs/tools/photo-folder.md`. Walk one ready YAML step (or the whole job if requested): produce the file under this Work Item’s `work/` or `out/`, run the check, then journal-keeper. Do not skip a step with a chat summary.

**Initial phase:** `role-job`

## Work map

```yaml
id: auction-file-completeness
steps:
  - id: check
    needs: []
    produces: checklist
    produce_path: work/auction-checklist.csv
    tool: docs/tools/auction-checklist.md
    check: python docs/tools/checks/csv-has-columns.py work/auction-checklist.csv unit item
    on_fail: retry
    next: [photos]
  - id: photos
    needs: [checklist]
    produces: photos
    produce_path: work/photo-index.csv
    tool: docs/tools/photo-folder.md
    check: python docs/tools/checks/file-exists.py work/photo-index.csv
    on_fail: retry
    next: [pack]
  - id: pack
    needs: [checklist, photos]
    produces: auction-pack
    produce_path: out/auction-file-completeness.md
    tool: docs/tools/auction-checklist.md
    check: python docs/tools/checks/file-exists.py out/auction-file-completeness.md
    on_fail: retry
    next: []
```

Starter work map. Replace tools and checks when the operator corrects this shop via **remember**.
