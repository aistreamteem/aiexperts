# Closeout Binder

**When to use:** Presence and absence of closeout files they named. No stamp. No warranty legal call. Do not mark a manual received unless the file is there. As-builts you index are markups, not sealed record drawings unless they said so. Photos support listed items; they do not create new closeout lines. Keys and codes are counts they wrote, not secrets stored here. The checklist and photo note feed a pack that quotes their list so missing O&M, warranties, and attic stock stay questions.

**How to run:** Follow `docs/role/work-item-method.md`. Use or create `work-items/<id>/`. Put source files in `in/`. For each YAML step below, in order: (1) do not start if `needs` files are missing — ask the operator; (2) read the `tool` file under `docs/tools/`; (3) write `produce_path` inside this Work Item folder (`work/` and `out/` are relative to the Work Item, not the expert root); (4) run `check` with those same relative paths; (5) on fail, retry at most 3 times then ask via **operator-qa**; (6) update the Work Item journal with **journal-keeper**. After the last step, the pack in `out/` must quote their source files. Do not invent counts, dates, approvals, or answers.

**Initial phase:** `intake`

## Work map

```yaml
id: closeout-binder
steps:
  - id: checklist
    needs: []
    produces: close-raw
    produce_path: work/closeout-checklist.csv
    tool: docs/tools/punch-sheet.md
    check: python docs/tools/checks/csv-has-columns.py work/closeout-checklist.csv item present
    on_fail: retry
    next: [photos]
  - id: photos
    needs: [close-raw]
    produces: close-photos
    produce_path: work/closeout-photos.md
    tool: docs/tools/photo-folder.md
    check: python docs/tools/checks/file-exists.py work/closeout-photos.md
    on_fail: retry
    next: [pack]
  - id: pack
    needs: [close-photos]
    produces: close-pack
    produce_path: out/closeout.md
    tool: docs/tools/drawings-folder.md
    check: python docs/tools/checks/file-exists.py out/closeout.md
    on_fail: retry
    next: []
```

Starter work map. Replace tools and checks when they confirm how this shop files.
