---
name: journal-keeper
description: >-
  Use after every work-map step completes or when the user answers a question —
  updates the active journal (step completed, artifacts, Resolved Q&A, next
  action) and folds merged background-agent notes into the proper sections.
---

# Journal Keeper

Updates the Work Item progress journal after each trade-coordinator work-map step or when the operator answers a question.

## When to use

- After every ready YAML step (pull schedule, packing-list gaps, permit rows, pack, and so on)
- Whenever the operator answers a blocking or deferred question (record in the same response)
- At session end (write Last session summary)
- When facts/rules are loaded or proactively detected

## Where notes go

- Expert journal: `journals/expert/progress.md` (current work item line, future work that is not a work item yet)
- Work item journal: `journals/work-items/<id>/progress.md` (premise, goal, workflow type, decisions every branch inherits, completion status)
- Branch map: `journals/work-items/<id>/state.json` (`active` path and `history` only)
- Node notes: `journals/work-items/<id>/nodes/<node-id>.md` (step notes, questions, next action)
- Background-agent notes: `journals/work-items/<id>/agent-notes/` (see that folder’s README). Merged notes land in the active leaf node file.

Preserve the exact `Current work item:` line. Only `continue` and `switch-context` may change it.

`active` is the path from `work-item` to the leaf. A blocking question becomes the active leaf. Its id is unique and is not `work-item` or a phase name.

### 0. Work Item context

- Active work item: the line in `.cursor/active-context.txt`, formatted `work-item:<id>`.
- Artifacts (spec, docs, TODOS, STATUS, facts): `work-items/<id>/`.
- Journal: `journals/work-items/<id>/progress.md` for item-wide fields, `state.json` for the
  branch map, and `nodes/<active leaf>.md` for step notes, open questions, and the next action.
  Write through journal-keeper.

## Journal Schema — which file holds each field

| File | Fields |
| --- | --- |
| `journals/work-items/<id>/progress.md` | Work item ID and description; Work item record; Workflow type and workflow-specific context; Spec file and version; Mode; Repo URL; Current branch; Commit strategy; PR URL; Decisions and approvals that every branch inherits; Completion status; Job id / Source files (this role) |
| `journals/work-items/<id>/nodes/<node>.md` | Last completed; Next action; Open questions (blocking and deferred); Q&A resolved in this step; Blockers, pause reason, last failure; facts and rules loaded and applied; proactively detected facts and rules; step notes; Checks run |
| `work-items/<id>/STATUS.md` | Last session summary; Artifacts list; links |
| Not stored | Current phase. It is the phase node on the `active` path in `state.json` |

## Work Item fields (this role)

Prefer the table above. For this trade-job-coordinator role specifically:

- **Work Item ID** / **Work Item description** — item-wide journal
- **Workflow type** — registry id; set once by workflow-selector — item-wide journal
- **Last completed** / **Next action** — active node
- **Job id** / **Source files** — item-wide journal
- **Artifacts** — `STATUS.md` (and note paths in the node)
- **Checks run** — active node
- Open questions / Resolved Q&A / Blockers — active node
- Completion status / Last session summary — item-wide journal / STATUS.md

Do not use software-design phase fields or outage-bridge fields.

### Update procedures

**After each step:**
1. Write the step completed to **Last completed** on the active node
2. Add artifacts produced (Work Item-relative paths) to STATUS.md
3. Set **Next action** on the active node to the next YAML `next` step that has its `needs` on disk, or `pack` / `done`
4. Update facts/rules loaded if they were read
5. Do not mark a step complete if blocking questions remain or the check did not exit 0

**When the operator answers:** in the same response, move the Q&A to Resolved and remove it from Open questions on the active node.

**At session end:** write Last session summary on STATUS.md; optionally refresh completion fields.

**Hooks:** After the journal update, the stop hook runs `py -3 .cursor/hooks/on_stop.py` (merge + audit). If it fails, log and continue. Fold merged agent-notes into the proper sections. Merge target is the active leaf node; pending notes live in `journals/work-items/<id>/agent-notes/`.

### Next actions (this role)

Follow the selected workflow file. Typical sequence: intake source files → first YAML step → later YAML steps → pack in `out/` → done. Human gates are “wait for file” or “wait for operator”, not design-doc approvals.

### Artifact paths

- `in/` — schedule exports, sold PDFs, packing lists they dropped for this job
- `work/` — indexes and working CSVs
- `out/` — finished board, packing list, permit pack, or photo checklist
- `evidence/` — check logs
- `facts/` — Work Item facts and rules
- `TODOS.md` — remaining map steps if useful
- `STATUS.md` — status summary
