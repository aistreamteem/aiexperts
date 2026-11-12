# Handbook Ack Missing

**When to use:** Compare the live handbook version string to each acknowledgment on their roster or ack sheet. List people with no ack, or an ack whose version does not match the live PDF. Do not invent an ack date. Do not interpret handbook clauses as employment law. Draft books stay draft. Write the missing-or-mismatch list and a write-up. They collect signatures. You do not treat a signed ack as a legal waiver you explain.

**How to run:** Select this workflow on a Work Item under `work-items/<id>/`. Follow each YAML step: read the `tool` doc, write `produce_path` in this Work Item, run `check`, retry at most 3 then ask. Update the Work Item journal after each step. One ready step per continue unless they asked for the whole pack.

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

Starter work map. Replace tools and checks when they correct how *this* shop files.
