# Quality Checklist Pack

**When to use:** Assemble their quality form and any photo index they stored for the walk. Do not invent a score or a rubric. Do not stamp OSHA. If photos and the form disagree, quote both. Punch-list items stay open until they close them. Write-up is the pack plus missing-form asks, not a compliance verdict. They walk. You file what the check can see.

**How to run:** Use **continue** with this workflow. Work inside `work-items/<id>/`. For each step: read the tool doc, produce the file, run the check (retry at most 3, then ask), then **journal-keeper**. Do not invent a score or stamp OSHA.

**Initial phase:** `form`

## Work map

```yaml
id: quality-checklist-pack
steps:
  - id: form
    needs: []
    produces: form
    produce_path: work/quality-form.pdf
    tool: docs/tools/quality-form.md
    check: python docs/tools/checks/file-exists.py work/quality-form.pdf
    on_fail: retry
    next: [photos]
  - id: photos
    needs: [form]
    produces: photos
    produce_path: work/photo-index.csv
    tool: docs/tools/photo-folder.md
    check: python docs/tools/checks/file-exists.py work/photo-index.csv
    on_fail: retry
    next: [pack]
  - id: pack
    needs: [form, photos]
    produces: quality-pack
    produce_path: out/quality-pack.md
    tool: docs/tools/spreadsheet.md
    check: python docs/tools/checks/file-exists.py out/quality-pack.md
    on_fail: retry
    next: []
```

Starter map. Replace tools and checks when the operator corrects this shop (**remember**).
