# Board pack

**When to use:** List files for the meeting date they name: agenda, exhibits, treasurer attachments, staff reports, committee items. Label minutes draft versus adopted from the minutes folder. Do not add outcome claims that are not in the staff files. Do not recast restricted totals as unrestricted on the cover. Consent items still need their attachments. Missing exhibits stay on the list as holes. They circulate and they run the meeting. A draft agenda or draft minutes you assemble is not adopted action. Output is the file list, the minutes index, and the packet pack in out/.

**How to run:** Open or continue the Work Item under `work-items/<id>/`. Walk one ready YAML step (or the whole named job if requested): produce the file, run the check, then journal-keeper.

**Initial phase:** `role-job`

## Work map

```yaml
id: board-pack
steps:
  - id: list
    needs: []
    produces: board
    produce_path: work/board-files.csv
    tool: docs/tools/board-folder.md
    check: python docs/tools/checks/file-exists.py work/board-files.csv
    on_fail: retry
    next: [minutes]
  - id: minutes
    needs: [board]
    produces: minutes
    produce_path: work/minutes-index.csv
    tool: docs/tools/minutes-folder.md
    check: python docs/tools/checks/file-exists.py work/minutes-index.csv
    on_fail: retry
    next: [pack]
  - id: pack
    needs: [board, minutes]
    produces: board-out
    produce_path: out/board-pack.md
    tool: docs/tools/board-folder.md
    check: python docs/tools/checks/file-exists.py out/board-pack.md
    on_fail: retry
    next: []
```

Starter work map. Replace tools and checks when they correct how this shop works (**remember**).
