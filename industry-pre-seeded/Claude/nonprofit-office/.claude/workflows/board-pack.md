# Board Pack

**When to use:** List files for the meeting date they name: agenda, exhibits, treasurer attachments, staff reports, committee items. Label minutes draft versus adopted from the minutes folder. Do not add outcome claims that are not in the staff files. Do not recast restricted totals as unrestricted on the cover. Consent items still need their attachments. Missing exhibits stay on the list as holes. They circulate and they run the meeting. A draft agenda or draft minutes you assemble is not adopted action. Output is the file list, the minutes index, and the packet note in out/.

**How to run:** Follow this file with **continue**. Paths `work/` and `out/` mean inside `work-items/<id>/`. Load `facts/MEMORY-INDEX.md` then shared facts/rules. If no Work Item exists, use **workflow-selector** for this job and copy `work-items/_TEMPLATE/`. Put operator files in `in/`. For each ready YAML step: read its tool doc; do not start if `needs` files are missing; write `produce_path`; run `check` against this Work Item’s paths (retry at most three times, then ask). Pass produced files to later steps. Missing shop knowledge → **operator-qa** or ask; do not invent. After the last check passes, the pack is `out/` plus `STATUS.md` (sources, artifacts, check results). They circulate, sign, send, submit, or talk to donors — you do not. **journal-keeper** after the step (or after the whole named job if they asked for the whole job).

**Initial phase:** `role-job`

## Steps

1. List agenda, exhibits, treasurer attachments, and staff/committee files for the named meeting date (docs/tools/board-folder.md) → `work/board-files.csv`.
2. Index minutes draft versus adopted (docs/tools/minutes-folder.md) → `work/minutes-index.csv`.
3. Assemble the packet cover and hole list → `out/board-pack.md`. They circulate and run the meeting.

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

Starter work map. Replace tools and checks when this shop corrects them.
