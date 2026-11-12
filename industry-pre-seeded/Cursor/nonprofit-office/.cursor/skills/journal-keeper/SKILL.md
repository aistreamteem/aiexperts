---
name: journal-keeper
description: >-
  Use after every work-map step completes or when the user answers a question —
  updates the active journal (step completed, artifacts, Resolved Q&A, next
  action) and folds merged background-agent notes into the proper sections.
---

# Journal Keeper

Updates the Work Item progress journal after each nonprofit-office work-map step or when the operator answers a question.

## When to use

- After every ready YAML step (board file list, minutes index, grant deadlines, ack drafts, and so on)
- Whenever the operator answers a blocking or deferred question (record in the same response)
- At session end (write Last session summary)
- When facts/rules are loaded or proactively detected

## Where notes go

- Expert journal: `journals/expert/progress.md` (current work item line, future work that is not a work item yet)
- Work item journal: `journals/work-items/<id>/progress.md` (item-wide fields; keep short)
- Branch map: `journals/work-items/<id>/state.json` (`active` path and `history` only)
- Node notes: `journals/work-items/<id>/nodes/<node-id>.md` (step notes, questions, next action)
- Agent notes inbox: `journals/work-items/<id>/agent-notes/` (background agents; see that folder’s README)

Do not create a legacy `work-items/<id>/journal/` folder.

Preserve the exact `Current work item:` line in the expert journal. Only `continue` and `switch-context` may change it.

`active` is the path from `work-item` to the leaf. A blocking question becomes the active leaf. Its id is unique and is not `work-item` or a phase name.

### 0. Work Item context

- Active work item: the line in `.cursor/active-context.txt`, formatted `work-item:<id>` (legacy `.cursor/active-work-item.txt` is read-only fallback).
- Artifacts (spec, docs, TODOS, STATUS, facts): `work-items/<id>/`.
- Journal: `journals/work-items/<id>/progress.md` for item-wide fields, `state.json` for the
  branch map, and `nodes/<active leaf>.md` for step notes, open questions, and the next action.
  Write through journal-keeper.

## Where each field lives

| File | Fields |
| --- | --- |
| `journals/work-items/<id>/progress.md` | Work item ID and description; Work item record; Workflow type and workflow-specific context; Spec file and version; Mode; Repo URL; Current branch; Commit strategy; PR URL; Decisions and approvals that every branch inherits; Completion status |
| `journals/work-items/<id>/nodes/<node>.md` | Last completed; Next action; Open questions (blocking and deferred); Q&A resolved in this step; Blockers, pause reason, last failure; facts and rules loaded and applied; proactively detected facts and rules; step notes |
| `work-items/<id>/STATUS.md` | Last session summary; Artifacts list; links |
| Not stored | Current phase. It is the phase node on the `active` path in `state.json` |

## Journal schema (values)

**Work Item context (flat journal):**
- **Work Item ID:** `WID-XXXXXXXX`
- **Work Item description:** [e.g. 2026-11-08 board pack, grant deadlines, gift ack draft]
- **Workflow type:** registry id (`board-pack` | `donor-list` | `funder-gap` | `gift-ack-draft` | `grant-deadlines` | `grant-report` | `in-kind-list` | `minutes-index` | `restricted-ask`)
- **Completion status:** not started | in progress | done

**Node note:**
- **Last completed:** [YAML step id or pack]
- **Next action:** [next YAML step id, wait for file, wait for operator, pack, done]
- Open questions (blocking / deferred); Resolved Q&A; Blockers; facts/rules loaded

**STATUS.md:** Last session summary; Artifacts (paths relative to the Work Item folder: `in/…`, `work/…`, `out/…`, `evidence/…`)

**Facts and rules:**
- Work Item facts/rules loaded from `work-items/<id>/facts/`
- Expert Role facts/rules applied from `facts/facts-shared.md` and `facts/rules-shared.md`

Do not keep a parallel top-level role machine-state file. Step progress lives here.

### Update procedures

**After each step:**
1. Write the step completed to **Last completed** on the active node
2. Add artifacts produced to `STATUS.md` (Work Item-relative paths)
3. Set **Next action** on the active node to the next YAML `next` step that has its `needs` on disk, or `pack` / `done`
4. Update facts/rules loaded if they were read
5. Do not mark a step complete if blocking questions remain or the check did not exit 0

**When the operator answers:** in the same response, move the Q&A to Resolved and remove it from Open questions.

**At session end:** write Last session summary on `STATUS.md`; optionally refresh other STATUS fields.

**Trigger audit snapshot:** after the journal update, run `py -3 .cursor/hooks/journal_snapshot.py` if that hook exists. If it fails, log and do not block the role job.

**Merge background-agent notes:** fold appended raw notes from the active node (after `merge_agent_notes.py` runs) into Artifacts, Resolved Q&A, and Next action. Notes land in the active leaf node file, not in `progress.md`.

### Next actions (this role)

Follow the selected workflow file. Typical sequence: intake source files → first YAML step → later YAML steps → pack in `out/` → done. Human gates are “wait for file” or “wait for operator”, not design-doc approvals.

### Artifact paths

- `in/` — board folders, grant PDFs, donor CSVs, minutes, and templates they dropped for this job
- `work/` — indexes and working CSVs
- `out/` — finished list, drafts, or ASK-list pack
- `evidence/` — check logs
- `facts/` — Work Item facts and rules
- `TODOS.md` — remaining map steps if useful
- `STATUS.md` — status summary
