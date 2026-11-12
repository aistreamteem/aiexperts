# Handbook acknowledgments missing

**When to use:** Compare the live handbook version string to each acknowledgment on their roster or ack sheet. List people with no ack, or an ack whose version does not match the live PDF. Do not invent an ack date. Do not interpret handbook clauses as employment law. Draft books stay draft. Write the missing-or-mismatch list and a pack summary under `out/`. They collect signatures. You do not treat a signed ack as a legal waiver you explain.

## How to run

1. Open or switch to one Work Item under `work-items/<id>/` (`workflow-selector` if the job is not selected yet). Put source files in that item's `in/`.
2. Follow this file's YAML: one ready step per **continue**, or the whole named job if the operator requested it. Read the named `docs/tools/` doc. Write `produce_path` under this Work Item. Run the step `check`. Retry at most three times, then ask.
3. Run **journal-keeper** after the step (or job) completes.

**Initial phase:** `role-job`

## Work map

```yaml
id: handbook-ack-missing
steps:
  - id: book
    needs: []
    produces: handbook
    produce_path: work/handbook-version.txt
    tool: docs/tools/handbook-pdf.md
    check: python docs/tools/checks/file-exists.py work/handbook-version.txt
    on_fail: retry
    next: [acks]
  - id: acks
    needs: [handbook]
    produces: acks
    produce_path: work/handbook-acks.csv
    tool: docs/tools/spreadsheet.md
    check: python docs/tools/checks/csv-has-columns.py work/handbook-acks.csv name
    on_fail: retry
    next: [pack]
  - id: pack
    needs: [handbook, acks]
    produces: ack-pack
    produce_path: out/handbook-acks-missing.md
    tool: docs/tools/handbook-pdf.md
    check: python docs/tools/checks/file-exists.py out/handbook-acks-missing.md
    on_fail: retry
    next: []
```

Starter work map. Replace tools and checks when they correct this shop.
