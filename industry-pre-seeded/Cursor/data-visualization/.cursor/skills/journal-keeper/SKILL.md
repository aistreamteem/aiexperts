---
name: journal-keeper
description: >-
  Update journals/expert/progress.md and the active Work Item journal after
  chart-pack work, decisions, or session end. Use whenever next action or
  the pack’s story changes.
---

# Journal keeper

Keep a readable progress file so **continue** works. Expert-level notes go in `journals/expert/progress.md`. Pack-level notes go in `journals/work-items/<id>/`.

### 0. Work Item context

- Active work item: the line in `.cursor/active-context.txt`, formatted `work-item:<id>`.
- Artifacts (spec, docs, TODOS, STATUS, facts): `work-items/<id>/`.
- Journal: `journals/work-items/<id>/progress.md` for item-wide fields, `state.json` for the
  branch map, and `nodes/<active leaf>.md` for step notes, open questions, and the next action.
  Write through journal-keeper.

## When

After define-role, after a workflow step, after a decision, at session end, when Next action changes, when a check fails, when the operator answers a blocking question.

## Where each field lives

| File | Fields |
| --- | --- |
| `journals/work-items/<id>/progress.md` | Work item ID and description; Work item record; Workflow type and workflow-specific context; Spec file and version; Mode; Repo URL; Current branch; Commit strategy; PR URL; HLD profile, intake links, compliance review; Decisions and approvals that every branch inherits; Completion status |
| `journals/work-items/<id>/nodes/<node>.md` | Last completed; Next action; Open questions (blocking and deferred); Q&A resolved in this step; Blockers, pause reason, last failure; facts and rules loaded and applied; proactively detected facts and rules; step notes |
| `work-items/<id>/STATUS.md` | Last session summary; Artifacts list; links |
| Not stored | Current phase. It is the phase node on the `active` path in `state.json` |

## Do

1. Read `.cursor/active-context.txt` (legacy read fallback: `.cursor/active-work-item.txt`) for the active Work Item id.
2. Update `journals/work-items/<id>/progress.md` with item-wide fields only (workflow type, completion status, decisions, work item record).
3. Update `journals/work-items/<id>/state.json` only as a branch map (`active`, node status). Do not keep a parallel role-machine field set as a second source of truth.
4. Write step notes, open questions, next action, blockers, and loaded facts/rules under `journals/work-items/<id>/nodes/<active leaf>.md`.
5. Update `work-items/<id>/STATUS.md` Last session summary, Artifacts, and Next action.
6. If the active Work Item changed because the operator asked, set **Current work item** on `journals/expert/progress.md`.
7. Do not mark the pack complete if blocking questions remain or a required produce_path is missing.
8. Extra workers must not edit the journal. Only this chat, using this skill.

Background agents write loose notes or shared-task notes under `journals/work-items/<id>/agent-notes/` (see that folder’s README). The stop hook `on_stop.py` merges them into the active node file; merged notes do not land in the flat `progress.md`.

`next_action` examples: `workflow-selector`, `wait for operator`, `continue`, a workflow step id (`load`, `summary`, `chart`, `pack`), `promote-facts-rules`, `done`.
