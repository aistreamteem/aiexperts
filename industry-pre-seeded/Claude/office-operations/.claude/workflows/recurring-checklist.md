# Recurring Checklist

**When to use:** Only lines they named. Missing owner: ask in the write-up, do not assign. Tick a backup or walk line only from their log or a person they named. Do not invent a generic office calendar. Missed cadence is a flag, not a compliance finding. Keep their weekly or monthly wording. You do not fix a failed backup account. Starter Friday-sheet notes; they still teach this shop's lines and who owns each one.

**How to run:** Open or continue a Work Item under `work-items/<id>/`. Put source files in `in/`. Walk one ready YAML step (or the whole named job if requested): read the named tool doc, produce the file, run the check, then **journal-keeper**.

**Initial phase:** `role-job`

## Work map

```yaml
id: recurring-checklist
steps:
  - id: pull
    needs: []
    produces: checks
    produce_path: work/recurring.csv
    tool: docs/tools/checklist.md
    check: python docs/tools/checks/csv-has-columns.py work/recurring.csv task owner
    on_fail: retry
    next: [pack]
  - id: pack
    needs: [checks]
    produces: check-pack
    produce_path: out/recurring.md
    tool: docs/tools/checklist.md
    check: python docs/tools/checks/file-exists.py out/recurring.md
    on_fail: retry
    next: []
```

Starter work map. Replace tools and checks when they correct this shop.
