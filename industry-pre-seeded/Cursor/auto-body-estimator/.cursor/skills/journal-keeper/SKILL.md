---
name: journal-keeper
description: >-
  Update journals/expert/progress.md and the active Work Item journal after
  work, decisions, or session end. Use whenever next action or the claim
  story changes.
disable-model-invocation: false
---

# Journal keeper

Keep a readable progress file and a small state file so **continue** works.

## When

After define-role, after a workflow step, after a decision, at session end, when next action changes, when the operator answers a blocking question.

## Where each field lives

| File | Fields |
| --- | --- |
| `journals/work-items/<id>/progress.md` | Work item ID and description; Work item record; Workflow type and workflow-specific context; Spec file and version; Mode; Repo URL; Current branch; Commit strategy; PR URL; HLD profile, intake links, compliance review; Decisions and approvals that every branch inherits; Completion status; Last session summary (may also mirror to STATUS) |
| `journals/work-items/<id>/nodes/<node>.md` | Last completed; Next action; Open questions (blocking and deferred); Q&A resolved in this step; Blockers, pause reason, last failure; facts and rules loaded and applied; proactively detected facts and rules; step notes |
| `work-items/<id>/STATUS.md` | Last session summary; Artifacts list; links |
| Not stored | Current phase. It is the phase node on the `active` path in `state.json` |

## Do

1. Read `.cursor/active-context.txt` (legacy fallback: `.cursor/active-work-item.txt`) to find the Work Item id.

2. Update `journals/work-items/<id>/progress.md` for item-wide fields (workflow type, decisions every branch inherits, completion status, work item record).

3. Update `journals/work-items/<id>/state.json` so `active` matches the current node. Write step notes, open questions, blockers, and **Next action** on `nodes/<active leaf>.md`.

4. Update `journals/expert/progress.md`: **Current work item** line. Add future work that is not a Work Item yet.

5. Background agents write loose notes under `journals/work-items/<id>/agent-notes/` (see that folder's README). The stop hook (`py -3 .cursor/hooks/on_stop.py`) merges them into the active node file; they do not land only in `progress.md`.

6. Long Q&A: one line in progress.md or the node; details in a `qa-sessions/` session when needed.

7. Do not mark the job complete if blocking questions remain, or if the selected workflow still has steps whose artifacts/checks are missing.

8. Extra workers must not edit the journal. Only this chat, using this skill.

`next_action` examples: `define-role`, `wait for operator`, `walk assignment-intake step assign`, `wait for authorization`, `done`.
