---
name: journal-keeper
description: >-
  Use after every work-map step completes or when the user answers a question —
  updates the active journal (step completed, artifacts, Resolved Q&A, next
  action) and folds merged background-agent notes into the proper sections.
---

# Journal Keeper

Updates the Work Item progress journal after each school-office work-map step or when the operator answers a question.

## When to use

- After every ready YAML step (attendance list, missing-enrollment index, immunization present/missing, calendar pack, and so on)
- Whenever the operator answers a blocking or deferred question (record in the same response)
- At session end (write Last session summary)
- When facts/rules are loaded or proactively detected

## Where notes go

- Expert journal: `journals/expert/progress.md` (current work item line, future work that is not a work item yet)
- Work item journal: `journals/work-items/<id>/progress.md` (item-wide fields)
- Branch map: `journals/work-items/<id>/state.json` (`active` path and `history` only)
- Node notes: `journals/work-items/<id>/nodes/<node-id>.md` (step notes, questions, next action)
- Agent notes inbox: `journals/work-items/<id>/agent-notes/` (background agents; merged by `on_stop.py`)

`work-items/<id>/journal/progress.md` was the legacy pointer and is removed from the template. Do not recreate it.

Preserve the exact `Current work item:` line. Only `continue` and `switch-context` may change it.

`active` is the path from `work-item` to the leaf. A blocking question becomes the active leaf. Its id is unique and is not `work-item` or a phase name.

### 0. Work Item context

- Active work item: the line in `.cursor/active-context.txt`, formatted `work-item:<id>`.
- Artifacts (spec, docs, TODOS, STATUS, facts): `work-items/<id>/`.
- Journal: `journals/work-items/<id>/progress.md` for item-wide fields, `state.json` for the
  branch map, and `nodes/<active leaf>.md` for step notes, open questions, and the next action.
  Write through journal-keeper.

## Where each field lives

| File | Fields |
| --- | --- |
| `journals/work-items/<id>/progress.md` | Work item ID and description; Work item record; Workflow type and workflow-specific context; Spec file; Mode; Decisions and approvals that every branch inherits; Completion status |
| `journals/work-items/<id>/nodes/<node>.md` | Last completed; Next action; Open questions (blocking and deferred); Q&A resolved in this step; Blockers, pause reason, last failure; facts and rules loaded and applied; proactively detected facts and rules; step notes |
| `work-items/<id>/STATUS.md` | Last session summary; Artifacts list; links |
| Not stored as a journal field | Current phase — it is the phase node on the `active` path in `state.json` |

## Journal schema (school-office)

**Workflow type:** registry id (`attendance-day` | `calendar-pack` | `immunization-present-missing` | `missing-enrollment` | `pickup-list` | `records-request-completeness` | `transcript-request-log` | `tuition-from-file` | `waitlist`)

**Artifacts:** paths relative to the Work Item folder (`in/…`, `work/…`, `out/…`, `evidence/…`) — list them in `STATUS.md`

**Facts and rules:**
- Work Item facts/rules loaded from `work-items/<id>/facts/`
- Expert Role facts/rules applied from `facts/facts-shared.md` and `facts/rules-shared.md`
- Rule violations / conflicts
- Proactively detected facts/rules

**Blockers:** none | waiting on user | waiting on file | check failed
**Completion status:** not started | in progress | done

Do not keep a parallel top-level role machine-state file. Step progress lives here.

### Update procedures

**After each step:**
1. Write the step completed to **Last completed** on the active node
2. Add artifacts produced to `STATUS.md` (Work Item-relative paths)
3. Set **Next action** to the next YAML `next` step that has its `needs` on disk, or `pack` / `done`
4. Update facts/rules loaded if they were read
5. Do not mark a step complete if blocking questions remain or the check did not exit 0

**When the operator answers:** in the same response, move the Q&A to Resolved and remove it from Open questions.

**At session end:** write Last session summary on `STATUS.md`.

**Trigger audit snapshot:** after the journal update, run `py -3 .cursor/hooks/journal_snapshot.py` if that hook exists. If it fails, log and do not block the role job.

**Merge background-agent notes:** fold appended raw notes from `journals/work-items/<id>/agent-notes/` into Artifacts, Resolved Q&A, and Next action. Merged notes land on the active node file (not only `progress.md`). Hooks under `.cursor/hooks/` own the merge (`on_stop.py` / `merge_agent_notes.py`).

### Next actions (this role)

Follow the selected workflow file. Typical sequence: intake source files → first YAML step → later YAML steps → pack in `out/` → done. Human gates are “wait for file” or “wait for operator”, not design-doc approvals.

### Artifact paths

- `in/` — SIS exports, PDFs, logs, and sheets they dropped for this job
- `work/` — indexes and working CSVs
- `out/` — finished list or checklist pack
- `evidence/` — check logs
- `facts/` — Work Item facts and rules
- `TODOS.md` — remaining map steps if useful
- `STATUS.md` — status summary
