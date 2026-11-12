# Eighty Six

**When to use:** Out items from their board photo or the POS export they named as source of truth. The list goes on top of the pack so expo and the line see it. Do not invent an 86 from an invoice short, a waste row, or a sales drop unless they taught that rule. If board and POS disagree, list both and ask. Undated photos are a question. Do not 86 the dining-room dish because catering took product unless they said to. This is their out list, not a menu change.

**How to run:** Self-contained. Active Work Item under `work-items/<id>/`. For each ready step: read the tool doc → write `produce_path` inside that Work Item → run the check with working directory = the Work Item folder → journal-keeper. One **continue** = one ready step unless they asked to finish this job.

**Initial phase:** `pull`

## Work map

```yaml
id: eighty-six
steps:
  - id: pull
    needs: []
    produces: 86-raw
    produce_path: work/86.csv
    tool: docs/tools/eighty-six-board.md
    check: python docs/tools/checks/csv-has-columns.py work/86.csv item shift
    on_fail: retry
    next: [pack]
  - id: pack
    needs: [86-raw]
    produces: 86-pack
    produce_path: out/86.md
    tool: docs/tools/eighty-six-board.md
    check: python docs/tools/checks/file-exists.py out/86.md
    on_fail: retry
    next: []
```

Starter work map. Replace tools and checks when the operator confirms how this kitchen files (`remember` / `integrate-docs`).
