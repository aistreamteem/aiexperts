# Closeout

**When to use:** From the POS export, list sales types, tenders, tips, voids, and gift-card activity. They count cash. Do not invent a drawer total. Split booth versus employee only if the roster is on file; if a provider has no role, ask before one pile. Quote holes—missing cash column, missing tickets—without plug lines. You do not take payment or close tickets in the live POS. Starter until they teach the official close report.

**How to run:** Open or continue a Work Item under `work-items/<id>/`. Put source files in that item’s `in/`. Walk one ready YAML step (or the whole named job if requested): produce the file, run the check, then **journal-keeper**. Paths `in/`, `work/`, `out/`, and `evidence/` are inside that Work Item.

**Initial phase:** `role-job`

## Work map

```yaml
id: closeout
steps:
  - id: pull
    needs: []
    produces: close
    produce_path: work/close.csv
    tool: docs/tools/pos-export.md
    check: python docs/tools/checks/file-exists.py work/close.csv
    on_fail: retry
    next: [roster]
  - id: roster
    needs: [close]
    produces: roster
    produce_path: work/booth-roster.csv
    tool: docs/tools/booth-roster.md
    check: python docs/tools/checks/file-exists.py work/booth-roster.csv
    on_fail: retry
    next: [pack]
  - id: pack
    needs: [close, roster]
    produces: close-pack
    produce_path: out/closeout.md
    tool: docs/tools/pos-export.md
    check: python docs/tools/checks/file-exists.py out/closeout.md
    on_fail: retry
    next: []
```

Starter work map. Replace tools and checks when the operator corrects this shop (**remember**).
