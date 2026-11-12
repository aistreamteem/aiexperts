# Board or session pack

**When to use:** Index the board-or-session folder against the packet list they stored: agenda, prior approved minutes, treasurer file, and ministry reports they dropped. Do not invent a motion. Do not treat draft minutes as adopted. Giving pages stay min necessary, not a donor CRM list. This is not a grant board pack. Write-up is present versus missing. They meet. You do not vote.

**How to run:** Open `work-items/<id>/`. Read this file. For one ready step (or the whole job if they asked): follow the `tool` doc, write `produce_path` inside that Work Item, run `check` from there. Then journal-keeper. See `.claude/workflows/README.md`.

**Initial phase:** `intake`

## Work map

```yaml
id: board-pack
steps:
  - id: folder
    needs: []
    produces: folder
    produce_path: work/board-index.csv
    tool: docs/tools/board-pack-folder.md
    check: python docs/tools/checks/file-exists.py work/board-index.csv
    on_fail: retry
    next: [pack]
  - id: pack
    needs: [folder]
    produces: board-pack
    produce_path: out/board-pack.md
    tool: docs/tools/spreadsheet.md
    check: python docs/tools/checks/file-exists.py out/board-pack.md
    on_fail: retry
    next: []
```

Starter work map. Replace tools and checks when the operator corrects how this office works.
