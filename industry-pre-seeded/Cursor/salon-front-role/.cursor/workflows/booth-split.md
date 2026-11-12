# Booth Split

**When to use:** Using the roster and the POS or book export, list tickets and totals in two piles: house employees versus booth renters. Ask if a provider has no label. Do not merge processor batches. Courtesy house-book listings are not house revenue unless they taught that. You do not give a classification opinion. Rent ledgers stay off this pack unless they asked for a separate rent list. Starter until they teach this floor’s ownership split.

**How to run:** Open or continue a Work Item under `work-items/<id>/`. Put source files in that item's `in/`. Walk one ready YAML step (or the whole named job if requested): produce the file, run the check, then **journal-keeper**. Paths `in/`, `work/`, `out/`, and `evidence/` are inside that Work Item.

**Initial phase:** `role-job`

## Work map

```yaml
id: booth-split
steps:
  - id: roster
    needs: []
    produces: roster
    produce_path: work/booth-roster.csv
    tool: docs/tools/booth-roster.md
    check: python docs/tools/checks/csv-has-columns.py work/booth-roster.csv provider role
    on_fail: retry
    next: [close]
  - id: close
    needs: [roster]
    produces: close
    produce_path: work/close.csv
    tool: docs/tools/pos-export.md
    check: python docs/tools/checks/file-exists.py work/close.csv
    on_fail: retry
    next: [pack]
  - id: pack
    needs: [roster, close]
    produces: split-pack
    produce_path: out/booth-split.md
    tool: docs/tools/booth-roster.md
    check: python docs/tools/checks/file-exists.py out/booth-split.md
    on_fail: retry
    next: []
```

Starter work map. Replace tools and checks when the operator corrects this shop (**remember**).
