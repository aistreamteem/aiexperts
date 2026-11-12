# Photo Condition Pack

**When to use:** Index photos in the folder against occupancy or vacant units: filename, unit, type (move-in, move-out, damage, inventory). Do not invent a photo or a condition code. Ready-to-rent stays their code. No full ID faces, PAN, or gate codes in the index. Flood or police stills stay in those event files if they split them. They shoot and they mark ready. You write the index and missing-photo questions.

**How to run:** Open or continue a Work Item under `work-items/<id>/`. Put photos and the occupancy export in `in/`. Read this file and `docs/tools/photo-folder.md` / `docs/tools/occupancy-export.md`. Walk one ready YAML step (or the whole job if requested): produce the file under this Work Item’s `work/` or `out/`, run the check, then journal-keeper. Do not skip a step with a chat summary.

**Initial phase:** `role-job`

## Work map

```yaml
id: photo-condition-pack
steps:
  - id: photos
    needs: []
    produces: photos
    produce_path: work/photo-index.csv
    tool: docs/tools/photo-folder.md
    check: python docs/tools/checks/file-exists.py work/photo-index.csv
    on_fail: retry
    next: [occ]
  - id: occ
    needs: [photos]
    produces: occ
    produce_path: work/occupancy.csv
    tool: docs/tools/occupancy-export.md
    check: python docs/tools/checks/file-exists.py work/occupancy.csv
    on_fail: retry
    next: [pack]
  - id: pack
    needs: [photos, occ]
    produces: photo-pack
    produce_path: out/photo-condition.md
    tool: docs/tools/photo-folder.md
    check: python docs/tools/checks/file-exists.py out/photo-condition.md
    on_fail: retry
    next: []
```

Starter work map. Replace tools and checks when the operator corrects this shop via **remember**.
