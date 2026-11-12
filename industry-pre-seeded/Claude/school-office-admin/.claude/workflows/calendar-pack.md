# Calendar Pack

**When to use:** Copy instructional days, holidays, and early dismissals from their calendar file. Attach bell-schedule versions if they stored them. Do not invent a snow-day makeup or a state hour rule. If two calendars disagree, quote both. Handbook dates that conflict with the calendar stay flagged. They publish. You pack the dated list and a write-up. Exam windows and conference days belong on the pack if the file has them. Do not promise a closure from a nearby district rumor. They publish revisions. You quote the dated file.

**How to run:** Open or switch to a Work Item under `work-items/<id>/`. Walk this YAML one ready step (or the whole named job if requested): read the named `docs/tools/` file, write `produce_path` inside this Work Item, run `check` against those paths, then **journal-keeper**.

**Initial phase:** `role-job`

## Work map

```yaml
id: calendar-pack
steps:
  - id: cal
    needs: []
    produces: calendar
    produce_path: work/calendar.csv
    tool: docs/tools/calendar-file.md
    check: python docs/tools/checks/file-exists.py work/calendar.csv
    on_fail: retry
    next: [pack]
  - id: pack
    needs: [calendar]
    produces: calendar-pack
    produce_path: out/calendar-pack.md
    tool: docs/tools/spreadsheet.md
    check: python docs/tools/checks/file-exists.py out/calendar-pack.md
    on_fail: retry
    next: []
```

Starter work map. Replace tools and checks when they correct this office (use **remember**).
