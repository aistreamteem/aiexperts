---
name: journal-keeper
description: >-
  Use after every work-map step completes or when the user answers a question —
  updates the active journal (step completed, artifacts, Resolved Q&A, next
  action) and folds merged background-agent notes into the proper sections.
---

# Journal Keeper

Updates the Work Item progress journal after each shipping work-map step or when the operator answers a question.

## When to use

- After every ready YAML step (pick CSV, scale export copy, BOL pack, exception list, and so on)
- Whenever the operator answers a blocking or deferred question (record in the same response)
- At session end (write Last session summary)
- When facts/rules are loaded or proactively detected

## Where notes go

Three stores. Do not invent a fourth journal path.

- Expert journal: `journals/expert/progress.md` (current work item line, future work that is not a work item yet)
- Work item journal: `journals/work-items/<id>/progress.md` (item-wide fields)
- Branch map: `journals/work-items/<id>/state.json` (`active` path and `history` only)
- Node notes: `journals/work-items/<id>/nodes/<node-id>.md` (step notes, questions, next action)
- Background notes: `journals/work-items/<id>/agent-notes/` (see that folder’s README; stop hook merges into the active node)

Preserve the exact `Current work item:` line. Only **continue** and **switch-context** may change it.

`active` is the path from `work-item` to the leaf. A blocking question becomes the active leaf. Its id is unique and is not `work-item` or a phase name.

### Field locations

| File | Fields |
| --- | --- |
| `journals/work-items/<id>/progress.md` | Work item ID and description; Work item record; Workflow type and workflow-specific context; Mode; Wave / order / truck / day / RMA; Decisions and approvals that every branch inherits; Completion status |
| `journals/work-items/<id>/nodes/<node>.md` | Last completed; Next action; Open questions (blocking and deferred); Q&A resolved in this step; Blockers, pause reason, last failure; facts and rules loaded and applied; proactively detected facts and rules; step notes |
| `work-items/<id>/STATUS.md` | Last session summary; Artifacts list; links |
| Not stored | Current phase. It is the phase node on the `active` path in `state.json` |

### 0. Work Item context

- Active work item: the line in `.claude/active-context.txt`, formatted `work-item:<id>`.
- Artifacts (spec, docs, TODOS, STATUS, facts): `work-items/<id>/`.
- Journal: `journals/work-items/<id>/progress.md` for item-wide fields, `state.json` for the
  branch map, and `nodes/<active leaf>.md` for step notes, open questions, and the next action.
  Write through journal-keeper.

## Do

1. Read `.claude/active-context.txt` for the Work Item id (legacy read fallback: `.claude/active-work-item.txt`).
2. Update the active node note: what happened, artifacts under `work-items/<id>/{in,work,out,evidence}`, check command and exit, open questions, next action.
3. Update `journals/work-items/<id>/progress.md` with item-wide fields only (workflow type, decisions, completion status, work item record).
4. Refresh `work-items/<id>/STATUS.md` when the session ends or the pack completes (last session summary, artifacts, links).
5. Do not mark the job complete if blocking questions remain or a map step has not passed its check (unless a documented exception is recorded).
6. Extra workers must not edit the journal. Only this chat, using this skill. Background agents write loose notes under `journals/work-items/<id>/agent-notes/`; `on_stop.py` merges them into the active node (not into `progress.md`).

### Next actions (this role)

Follow the selected workflow file. Typical sequence: intake source files → first YAML step → later YAML steps → pack in `out/` → done. Human gates are “wait for file” or “wait for operator”, not design-doc approvals.

### Artifact paths

- `in/` — WMS exports, BOL PDFs, scale exports, label folders, RMA sheets they dropped for this job
- `work/` — indexes and working CSVs/PDFs
- `out/` — finished list or completeness pack
- `evidence/` — check logs
- `facts/` — Work Item facts and rules
- `TODOS.md` — remaining map steps if useful
- `STATUS.md` — status summary

**Facts and rules:** Expert Role memory from `facts/facts-shared.md` / `facts/rules-shared.md` (always) and `facts/facts-operations.md` / `facts/rules-operations.md` (job or `all`); Work Item files under `work-items/<id>/facts/`.
