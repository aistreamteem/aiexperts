---
name: journal-keeper
description: >-
  Update the expert journal and the active Work Item journal after work,
  decisions, or session end. Use whenever next action or the transaction
  file’s story changes.
---

# Journal keeper

Keep a readable progress file so **continue** works. This role uses the expert architecture: `journals/expert/progress.md` plus `journals/work-items/<id>/`.

## When

After define-role, after a workflow step, after a decision, at session end, when next action changes, when the operator answers a blocking question.

## Where notes go

Three stores. Do not put step notes in a legacy pointer under `work-items/<id>/journal/`.

- Expert journal: `journals/expert/progress.md` (current work item line, future work that is not a work item yet)
- Work item journal: `journals/work-items/<id>/progress.md` (premise, goal, workflow type, decisions every branch inherits, completion status)
- Branch map: `journals/work-items/<id>/state.json` (`active` path and `history` only)
- Node notes: `journals/work-items/<id>/nodes/<node-id>.md` (step notes, questions, next action)

Preserve the exact `Current work item:` line. Only `continue` and `switch-context` may change it.

`active` is the path from `work-item` to the leaf. `history` is the descendant path below a node, not including that node. A load reads `active` only. A closed question must not stay in `history`.

### 0. Work Item context

- Active work item: the line in `.claude/active-context.txt`, formatted `work-item:<id>` (legacy read fallback: `.claude/active-work-item.txt`).
- Artifacts (spec, docs, TODOS, STATUS, facts): `work-items/<id>/`.
- Journal: `journals/work-items/<id>/progress.md` for item-wide fields, `state.json` for the
  branch map, and `nodes/<active leaf>.md` for step notes, open questions, and the next action.
  Write through journal-keeper.

### Where each field lives

| File | Fields |
| --- | --- |
| `journals/work-items/<id>/progress.md` | Work item ID and description; Work item record; Workflow type and workflow-specific context (address, side, escrow); Mode; Decisions and approvals that every branch inherits; Completion status |
| `journals/work-items/<id>/nodes/<node>.md` | Last completed; Next action; Open questions (blocking and deferred); Q&A resolved in this step; Blockers, pause reason, last failure; facts and rules loaded and applied; proactively detected facts and rules; step notes |
| `work-items/<id>/STATUS.md` | Last session summary; Artifacts list; links |
| Not stored as a journal field | Current phase — it is the phase node on the `active` path in `state.json` |

Background-agent notes land in `journals/work-items/<id>/agent-notes/` (see that folder's README). The stop hook (`on_stop.py` via the thin shell wrappers) merges them into the active leaf node file, not into `progress.md`.

## Do

1. **Read active Work Item ID** from `work-item:<id>` in `.claude/active-context.txt` (legacy fallback: `.claude/active-work-item.txt`)
2. Update `journals/work-items/<id>/progress.md` for item-wide fields only.
3. Update `journals/work-items/<id>/nodes/<active leaf>.md` for Last completed, Next action, Open questions, Resolved Q&A, blockers, facts/rules loaded, and step notes.
4. Update `journals/work-items/<id>/state.json` if the branch map needs it (`active` node, history).
5. Update `journals/expert/progress.md` **Current work item** when the active transaction file changes. Put future work that is not a Work Item yet under **Future work**.
6. Optionally refresh `work-items/<id>/STATUS.md`.
7. Do not mark the job complete if blocking questions remain, or if workflow steps are still unfinished.
8. Extra workers must not edit the journal. Only this chat, using this skill.

### Journal Schema (TC Work Items)

**Work Item Context:**
- **Work Item ID:** `WID-XXXXXXXX`
- **Work Item description:** [address + buy/list side + job]
- **Workflow type:** a key from `.claude/workflows/workflow-registry.json`
- **Property / file label:** [as on their folder]
- **Effective / option / closing dates:** [only when quoted from executed contract or amendment]

**Standard Fields (on the active node):**
- **Last completed:** [Last step id / phase]
- **Next action:** [Exact next YAML step, wait for operator, or done]

**Artifacts (STATUS.md):**
- List of created files under the Work Item (`in/`, `work/`, `out/`, `evidence/`)

**Facts and Rules Context:**
- **Work Item facts loaded:** from `work-items/<id>/facts/facts.md`
- **Work Item rules loaded:** from `work-items/<id>/facts/rules.md`
- **Expert Role facts applied:** from `facts/facts-operations.md`
- **Expert Role rules applied:** from `facts/rules-operations.md`

`next_action` examples: `define-role`, a workflow step id from the selected `.claude/workflows/<job>.md`, `wait for operator`, `done`.
