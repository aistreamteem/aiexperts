---
name: journal-keeper
description: >-
  Update expert and Work Item journals after a workflow step, operator
  answer, approval, failure, or session end.
---

# Journal keeper

Keep a readable progress file so **continue** can resume the current transaction file.

## When

After a workflow step, after a write-up file is saved to `out/`, after a decision, at session end, when `next_action` changes, when facts/rules are loaded or proposed.

## Where notes go

### 0. Work Item context

- Active work item: the line in `.cursor/active-context.txt`, formatted `work-item:<id>`.
- Artifacts (spec, docs, TODOS, STATUS, facts): `work-items/<id>/`.
- Journal: `journals/work-items/<id>/progress.md` for item-wide fields, `state.json` for the
  branch map, and `nodes/<active leaf>.md` for step notes, open questions, and the next action.
  Write through journal-keeper.

- Expert journal: `journals/expert/progress.md` (current work item line; future work that is not a Work Item yet)

Preserve the exact `Current work item:` line. Only **continue** and **switch-context** may change it.

A blocking question becomes the active leaf. Answering or deferring it returns `active` to the parent when no other blocking question remains. Use **AskQuestion** for a fixed choice. Use chat for an open answer.

## Journal Schema (where each field lives)

| File | Fields |
| --- | --- |
| `journals/work-items/<id>/progress.md` | Work item ID and description; Work item record; Workflow type and workflow-specific context (transaction file); Spec file and version; Mode; Repo URL; Current branch; Commit strategy; PR URL; HLD profile, intake links, compliance review; Decisions and approvals that every branch inherits; Completion status |
| `journals/work-items/<id>/nodes/<node>.md` | Last completed; Next action; Open questions (blocking and deferred); Q&A resolved in this step; Blockers, pause reason, last failure; facts and rules loaded and applied; proactively detected facts and rules; step notes |
| `work-items/<id>/STATUS.md` | Last session summary; Artifacts list; links |
| Not stored | Current phase. It is the phase node on the `active` path in `state.json` |

Transaction packs typically fill Workflow type, Transaction file, Decisions, Completion status, Next action, Artifacts, Open questions, and Last session summary. Leave unused software-build fields blank.

## Background agent notes

Background agents write loose notes or shared-task notes under
`journals/work-items/<id>/agent-notes/` (see that folder’s `README.md` in the template).
The stop hook merges them into the active leaf node file via
`.cursor/hooks/merge_agent_notes.py`. Merged notes land in the node file, not in
`progress.md`. After a merge, `.cursor/hooks/journal_snapshot.py` commits the
audit paths when git tracks them.

## Update procedures

**After each workflow step:**
1. Last completed = step id (on the active node)
2. Add produced files to Artifacts on `STATUS.md` (Work Item-relative)
3. Next action = next ready step, or wait for operator if a gate/check failed
4. Do not mark complete if blocking questions remain or a required check failed
5. Preserve workflow type on the flat journal

**When the operator answers:** same response, move to Resolved Q&A with date, remove from Open questions.

**At session end:** one-paragraph Last session summary on `STATUS.md` (what was indexed or listed, what is next, what file or answer is needed).

**After journal update:** the stop hook runs `on_stop.py` (merge + optional audit commit). Do not block on hook failure.

**Next actions** follow the selected TC workflow file and `docs/role/work-item-method.md` (intake → index → dates / missing docs / checklists → pack). Not HLD/DD/implement.
