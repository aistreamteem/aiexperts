---
name: journal-keeper
description: >-
  Use after every work-map step completes or when the user answers a question —
  updates the active journal (step completed, artifacts, Resolved Q&A, next
  action) and folds merged background-agent notes into the proper sections.
---

# Journal Keeper

Updates the Work Item progress journal after each CSR work-map step or when the operator answers a question.

## When to use

- After every ready YAML step (index PDFs, missing-forms CSV, holder list, pack, and so on)
- Whenever the operator answers a blocking or deferred question (record in the same response)
- At session end (write Last session summary)
- When facts/rules are loaded or proactively detected

## Where notes go

### 0. Work Item context

- Active work item: the line in `.claude/active-context.txt`, formatted `work-item:<id>`.
- Artifacts (spec, docs, TODOS, STATUS, facts): `work-items/<id>/`.
- Journal: `journals/work-items/<id>/progress.md` for item-wide fields, `state.json` for the
  branch map, and `nodes/<active leaf>.md` for step notes, open questions, and the next action.
  Write through journal-keeper.

Also:

- Expert journal: `journals/expert/progress.md` (current work item line, future work that is not a work item yet)

Preserve the exact `Current work item:` line. Only `continue` and `switch-context` may change it.

`active` is the path from `work-item` to the leaf. A blocking question becomes the active leaf. Its id is unique and is not `work-item` or a phase name.

## Work Item context (paths)

1. Read active Work Item ID from `.claude/active-context.txt` (`work-item:<id>`; legacy `.claude/active-work-item.txt` read fallback only)
2. Flat journal: `journals/work-items/<work-item-id>/progress.md`
3. Active note: last id in `state.json` `active`, file `nodes/<id>.md`
4. STATUS path: `work-items/<work-item-id>/STATUS.md`
5. Background-agent notes: `journals/work-items/<id>/agent-notes/` (see that folder’s README). Merged notes land in the active node file, not only in `progress.md`.

## Journal schema — which file holds each field

| File | Fields |
| --- | --- |
| `journals/work-items/<id>/progress.md` | Work item ID and description; Work item record; Workflow type and workflow-specific context; Spec file and version; Mode; Repo URL; Current branch; Commit strategy; PR URL; Decisions and approvals that every branch inherits; Completion status |
| `journals/work-items/<id>/nodes/<node>.md` | Last completed; Next action; Open questions (blocking and deferred); Q&A resolved in this step; Blockers, pause reason, last failure; facts and rules loaded and applied; proactively detected facts and rules; step notes |
| `work-items/<id>/STATUS.md` | Last session summary; Artifacts list; links |
| Not stored as a free field | Current phase — it is the phase node on the `active` path in `state.json` |

**Facts and rules references (for node notes):**
- Work Item facts/rules loaded from `work-items/<id>/facts/`
- Expert Role facts/rules applied from `facts/facts-operations.md` and `facts/rules-operations.md`

**Completion status values:** not started | in progress | done

Do not keep a parallel top-level role machine-state file. Step progress lives here.

### Update procedures

**After each step:**
1. Write the step completed to **Last completed** on the active node
2. Add artifacts produced (Work Item-relative paths) on STATUS or the node
3. Set **Next action** to the next YAML `next` step that has its `needs` on disk, or `pack` / `done`
4. Update facts/rules loaded if they were read
5. Do not mark a step complete if blocking questions remain or the check did not exit 0

**When the operator answers:** in the same response, move the Q&A to Resolved and remove it from Open questions.

**At session end:** write Last session summary on `STATUS.md`; optionally refresh completion status on the flat journal.

**Trigger audit snapshot:** after the journal update, run `py -3 .claude/hooks/journal_snapshot.py` if that hook exists. If it fails, log and do not block the role job.

**Merge background-agent notes:** fold appended raw notes into Artifacts, Resolved Q&A, and Next action. Hooks under `.claude/hooks/` own the merge (`merge_agent_notes.py` / `on_stop.py`).

### Next actions (this role)

Follow the selected workflow file. Typical sequence: intake source files → first YAML step → later YAML steps → pack in `out/` → done. Human gates are “wait for file” or “wait for operator”, not design-doc approvals.

### Artifact paths

- `in/` — AMS exports and PDFs they dropped for this job
- `work/` — indexes and working CSVs
- `out/` — finished list or request pack
- `evidence/` — check logs
- `facts/` — Work Item facts and rules
- `TODOS.md` — remaining map steps if useful
- `STATUS.md` — status summary
