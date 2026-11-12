# Closeout Photos

**When to use:** For jobs they mark complete: required photos present or missing. Do not invent an inspection pass. Ask their list per job type: before, plate, after, and others they named. Do not store ID photos. Unreadable plates are asks, not guessed serials. As-builts are extra if they require them. A scheduled inspection in the folder is not a pass. The write-up lists missing types by job id. Naming with job id and type helps the check. Their SOP list wins.

**How to run:** Open or continue a Work Item under `work-items/<id>/`. Walk one ready YAML step (or the whole named job if requested). Produce the file, run the check, then **journal-keeper**.

**Initial phase:** `role-job`

## Work map

```yaml
id: closeout-photos
steps:
  - id: photos
    needs: []
    produces: photo-index
    produce_path: work/photo-index.csv
    tool: docs/tools/photo-folder.md
    check: python docs/tools/checks/file-exists.py work/photo-index.csv
    on_fail: retry
    next: [missing]
  - id: missing
    needs: [photo-index]
    produces: photo-missing
    produce_path: work/photo-missing.csv
    tool: docs/tools/photo-folder.md
    check: python docs/tools/checks/csv-has-columns.py work/photo-missing.csv job missing
    on_fail: retry
    next: [photo-pack]
  - id: photo-pack
    needs: [photo-missing]
    produces: closeout-writeup
    produce_path: out/closeout-photos.md
    tool: docs/tools/job-folder.md
    check: python docs/tools/checks/file-exists.py out/closeout-photos.md
    on_fail: retry
    next: []
```

Starter work map. Replace tools and checks when they correct this shop (**remember**).
