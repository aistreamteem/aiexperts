# Volunteer roster pack

**When to use:** Build the team list from their volunteer export for the ministries they named. Keep their roles. Flag blank assignments on dates that are on the calendar if they also dropped one. Do not add a volunteer. Do not recruit by SMS. Do not decide a person is cleared. Min necessary on any print. Write-up is the roster plus gaps. They schedule.

**How to run:** Open `work-items/<id>/`. Read this file. For one ready step (or the whole job if they asked): follow the `tool` doc, write `produce_path` inside that Work Item, run `check` from there. Then journal-keeper. See `.claude/workflows/README.md`.

**Initial phase:** `intake`

## Work map

```yaml
id: volunteer-roster
steps:
  - id: roster
    needs: []
    produces: roster
    produce_path: work/volunteer-roster.csv
    tool: docs/tools/volunteer-roster.md
    check: python docs/tools/checks/csv-has-columns.py work/volunteer-roster.csv volunteer ministry
    on_fail: retry
    next: [pack]
  - id: pack
    needs: [roster]
    produces: roster-pack
    produce_path: out/volunteer-roster.md
    tool: docs/tools/spreadsheet.md
    check: python docs/tools/checks/file-exists.py out/volunteer-roster.md
    on_fail: retry
    next: []
```

Starter work map. Replace tools and checks when the operator corrects how this office works.
