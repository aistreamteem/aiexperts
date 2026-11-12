# Receiving

**When to use:** Receiving log or marked ticket versus the invoice. Credits are drafted as questions from their short, damage, or reject notes plus the invoice line. No invented reject temperatures as law. No invented credit dollars. They submit the credit. If they have no receiving log, say the pack is invoice-only and ask. Catch-weight scale versus ticket weight is a question when both exist. You do not reject the truck in the write-up. Spec subs stay questions.

**How to run:** Self-contained. Active Work Item under `work-items/<id>/`. For each ready step: read the tool doc → write `produce_path` inside that Work Item → run the check with working directory = the Work Item folder → journal-keeper. One **continue** = one ready step unless they asked to finish this job.

**Initial phase:** `recv`

## Work map

```yaml
id: receiving
steps:
  - id: recv
    needs: []
    produces: recv-raw
    produce_path: work/receiving.csv
    tool: docs/tools/receiving-log.md
    check: python docs/tools/checks/csv-has-columns.py work/receiving.csv item qty
    on_fail: retry
    next: [pack]
  - id: pack
    needs: [recv-raw]
    produces: recv-pack
    produce_path: out/receiving.md
    tool: docs/tools/invoice-pdf.md
    check: python docs/tools/checks/file-exists.py out/receiving.md
    on_fail: retry
    next: []
```

Starter work map. Replace tools and checks when the operator confirms how this kitchen files (`remember` / `integrate-docs`).
