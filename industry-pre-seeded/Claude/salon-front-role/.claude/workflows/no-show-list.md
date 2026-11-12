# No Show List

**When to use:** From the book export and their policy file, list cancelled and no-show rows. Quote the policy. They decide fees. They contact guests. Use their status labels; do not rewrite cancelled as no-show. Do not invent a dollar amount. Deposits already on the export are listed as shown. You do not text or charge a card. If the policy file is missing, list names and ask. Starter until they teach this shop’s posted rule.

**How to run:** Open or continue a Work Item under `work-items/<id>/`. Put source files in that item’s `in/`. Walk one ready YAML step (or the whole named job if requested): produce the file, run the check, then **journal-keeper**. Paths `in/`, `work/`, `out/`, and `evidence/` are inside that Work Item.

**Initial phase:** `role-job`

## Work map

```yaml
id: no-show-list
steps:
  - id: pull
    needs: []
    produces: book
    produce_path: work/book.csv
    tool: docs/tools/booking-export.md
    check: python docs/tools/checks/file-exists.py work/book.csv
    on_fail: retry
    next: [policy]
  - id: policy
    needs: [book]
    produces: policy
    produce_path: work/no-show-policy.md
    tool: docs/tools/no-show-policy-file.md
    check: python docs/tools/checks/file-exists.py work/no-show-policy.md
    on_fail: retry
    next: [pack]
  - id: pack
    needs: [book, policy]
    produces: noshow-pack
    produce_path: out/no-shows.md
    tool: docs/tools/no-show-policy-file.md
    check: python docs/tools/checks/file-exists.py out/no-shows.md
    on_fail: retry
    next: []
```

Starter work map. Replace tools and checks when the operator corrects this shop (**remember**).
