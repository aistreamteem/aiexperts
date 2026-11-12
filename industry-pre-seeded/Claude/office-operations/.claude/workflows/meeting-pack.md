# Meeting Pack

**When to use:** Agenda plus open actions from last minutes. They send anything to people. Keep their meeting label; a staff huddle is not a board book. Do not invent decisions or assign owners to punish. Unclear owner: ask. Attachments are files they already named. Public or leftover printouts omit personal phones if they said a guest might see them. Draft stays in work/ and out/. Starter pack shape until they teach this shop's template.

**How to run:** Open or continue a Work Item under `work-items/<id>/`. Put source files in `in/`. Walk one ready YAML step (or the whole named job if requested): read the named tool doc, produce the file, run the check, then **journal-keeper**.

**Initial phase:** `role-job`

## Work map

```yaml
id: meeting-pack
steps:
  - id: agenda
    needs: []
    produces: agenda
    produce_path: work/agenda.csv
    tool: docs/tools/meeting-agenda.md
    check: python docs/tools/checks/csv-has-columns.py work/agenda.csv topic owner
    on_fail: retry
    next: [actions]
  - id: actions
    needs: [agenda]
    produces: actions
    produce_path: work/actions.csv
    tool: docs/tools/meeting-agenda.md
    check: python docs/tools/checks/csv-has-columns.py work/actions.csv action owner
    on_fail: retry
    next: [pack]
  - id: pack
    needs: [actions]
    produces: meet-pack
    produce_path: out/meeting-pack.md
    tool: docs/tools/meeting-agenda.md
    check: python docs/tools/checks/file-exists.py out/meeting-pack.md
    on_fail: retry
    next: []
```

Starter work map. Replace tools and checks when they correct this shop.
