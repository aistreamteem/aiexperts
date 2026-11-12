---
name: journal-keeper
description: "Use after every pipeline phase or when the operator answers a question. Updates the work-item journal and STATUS."
trigger: After every phase or when the operator answers
---

# Journal keeper

Expert journal: `journals/expert/progress.md`.
Work item journal: `journals/work-items/<id>/progress.md`.
Branch map: `journals/work-items/<id>/state.json`.
Node notes: `journals/work-items/<id>/nodes/<node-id>.md`.
Status: `work-items/<id>/STATUS.md`.
Active id: `.cursor/active-context.txt` (`work-item:<id>`).

Background agents write under `journals/work-items/<id>/agent-notes/` (see that folder's README). The stop hook merges them into the active leaf node, then archives them.

Overarching fields stay on the work item journal: workflow type, charter depth, completion status, and decisions every branch inherits. Step notes, questions, and the next action go on the active node's note file.

`active` is the path from `work-item` to the leaf. `history` is the descendant path below a node, not including that node. A load reads `active` only. A closed question must not stay in `history`. Preserve the `Current work item:` line. Only continue and switch-context may change it.

A blocking question becomes the active leaf. Its id is unique and is not `work-item` or a phase name. Use AskQuestion for a fixed choice and chat for an open answer. If another open blocking question remains, move `active` to it. When none remains, return `active` to the parent, update that parent's next action, and clear `history`.

## Where each field lives

| File | Fields |
| --- | --- |
| `journals/work-items/<id>/progress.md` | Work item ID and description; Work item record; Workflow type and workflow-specific context; Mode; Charter depth; Intake links; Decisions and approvals that every branch inherits; Completion status |
| `journals/work-items/<id>/nodes/<node>.md` | Last completed; Next action; Open questions (blocking and deferred); Q&A resolved in this step; Blockers, pause reason, last failure; facts and rules loaded and applied; proactively detected facts and rules; step notes |
| `work-items/<id>/STATUS.md` | Last session summary; Artifacts list; quick links |
| Not stored | Current phase. It is the phase node on the `active` path in `state.json` |

Do not store a repo URL, a branch name, or a commit strategy. Close-out stores the status narrative, the decision-log path, and the handoff note instead.

## After each phase

1. Set Last completed.
2. Append artifacts.
3. Set Next action from the workflow file.
4. Update the facts and rules counts.
5. Leave the phase incomplete while a blocking question is open.
6. Do not change Workflow type.

## When the operator answers

In the same response, append the date, the question, and the answer under Resolved Q&A and remove the question from the open list.

## Session end

Write Last session summary: what finished, what is next, what you need. Refresh STATUS.md quick links: Journal, Charter, Plan, Diagrams, Decisions, Verification, TODOS, Facts, Rules.
