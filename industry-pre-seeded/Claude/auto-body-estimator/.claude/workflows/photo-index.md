# Photo index

**When to use:** Index the photo folder with their file names and required angles if they stored a shot list. Do not invent a photo. Do not hide prior-damage or personal-items shots. Missing required names stay missing. Write-up is an index plus asks, not a hidden-damage diagnosis and not an MPI. You do not rename away their claim or stage meaning unless they asked.

**How to run:** Confirm the Work Item under `work-items/<id>/`. Walk the YAML steps in this file via **continue** (one ready step, or the whole named job if requested). Read the cited `docs/tools/` file, write artifacts under this Work Item’s `work/` and `out/`, run the step `check` against those paths, then **journal-keeper**.

**Initial phase:** first YAML step in this file

## Work map

```yaml
id: photo-index
steps:
  - id: photos
    needs: []
    produces: photos
    produce_path: work/photo-index.csv
    tool: docs/tools/photo-folder.md
    check: python docs/tools/checks/csv-has-columns.py work/photo-index.csv name
    on_fail: retry
    next: [pack]
  - id: pack
    needs: [photos]
    produces: photo-pack
    produce_path: out/photo-index.md
    tool: docs/tools/spreadsheet.md
    check: python docs/tools/checks/file-exists.py out/photo-index.md
    on_fail: retry
    next: []
```

Starter work map. Replace tools and checks when the operator corrects this shop's process (**remember**).
