---
name: journal-keeper
description: >-
  Use after every HOA role-job step completes or when the operator answers a
  question. Updates the expert journal and the active Work Item journal
  (phase, artifacts, Resolved Q&A, next action).
---

# Journal Keeper

Updates the Work Item progress journal after each ready workflow step or when the operator answers a question. Use after every phase completion and whenever a decision is recorded.

## When to use

- After every ready step in a registered HOA workflow (intake, completeness check, produce pack, human gate, close)
- Whenever the operator answers a blocking or deferred question (record in the same response)
- At session end (write Last session summary)
- When facts/rules are loaded or proactively detected

## Instructions

### Where notes go

Three stores. Do not put step notes in the flat pointer file.

- Expert journal: `journals/expert/progress.md` (current work item line, future work that is not a work item yet)
- Work item journal: `journals/work-items/<id>/progress.md` (premise, goal, workflow type, decisions every branch inherits, completion status)
- Branch map: `journals/work-items/<id>/state.json` (`active` path and `history` only)
- Node notes: `journals/work-items/<id>/nodes/<node-id>.md` (step notes, questions, next action)

Preserve the exact `Current work item:` line. Only `continue` and `switch-context` may change it.

`active` is the path from `work-item` to the leaf. `history` is the descendant path below a node, not including that node. A load reads `active` only. A closed question must not stay in `history`.

A blocking question becomes the active leaf. Its id is unique and is not `work-item` or a phase name. Answering or deferring it: if another open blocking question remains, move `active` there; otherwise return `active` to the parent, update that parent's next action, and clear `history`. Use **AskUserQuestion** for a fixed choice. Use chat for an open answer.

### Work Item Context

1. **Read active Work Item ID** from `work-item:<id>` in `.claude/active-context.txt` (legacy fallback: `.claude/active-work-item.txt`)
2. **Flat journal:** `journals/work-items/<work-item-id>/progress.md`
3. **Active note:** the last id in `state.json` `active`, file `nodes/<id>.md`
4. **STATUS path:** `work-items/<work-item-id>/STATUS.md`

### Where each field lives

| File | Fields |
| --- | --- |
| `journals/work-items/<id>/progress.md` | Work item ID and description; Work item record; Workflow type and workflow-specific context (association, as-of/meeting/project date); Mode; Decisions and approvals that every branch inherits; Completion status |
| `journals/work-items/<id>/nodes/<node>.md` | Last completed; Next action; Open questions (blocking and deferred); Q&A resolved in this step; Blockers, pause reason, last failure; facts and rules loaded and applied; proactively detected facts and rules; step notes |
| `work-items/<id>/STATUS.md` | Last session summary; Artifacts list; links |
| Not stored as a journal field | Current phase — it is the phase node on the `active` path in `state.json` |

Background-agent notes land in `journals/work-items/<id>/agent-notes/` (see that folder's README). The stop hook merges them into the active leaf node file, not into `progress.md`.

### Journal Schema (HOA Work Items)

Maintain these fields:

**Work Item Context:**
- **Work Item ID:** `WID-XXXXXXXXX`
- **Work Item description:** [community + job, e.g. June board files / lot 12 ACC]
- **Workflow type:** a key from `.claude/workflows/workflow-registry.json` (set by workflow-selector; never invent a software-build or incident-bridge type)
- **Association / community:** [name as on their file]
- **As-of / meeting / project date:** [if the job has one]

**Standard Fields:**
- **Current phase:** identify | intake | completeness | produce-pack | human-gate | close | done (see `docs/role/work-item-method.md`)
- **Last completed:** [Last step id / phase]
- **Next action:** [Exact next YAML step, wait for operator, or done]

**Artifacts:**
- List of created files under the Work Item (`in/`, `work/`, `out/`, `evidence/`)

**Facts and Rules Context:**
- **Work Item facts loaded:** from `work-items/<id>/facts/facts.md`
- **Work Item rules loaded:** from `work-items/<id>/facts/rules.md`
- **Expert Role facts applied:** from `facts/facts-operations.md`
- **Expert Role rules applied:** from `facts/rules-operations.md`
- **Rule violations / conflicts:** [Any conflicts]
- **Proactively detected facts/rules:** [Proposed to operator, with date and outcome]

**Questions and Decisions:**
- **Open questions (blocking):** [MUST be empty to pass a human gate]
- **Open questions (deferred):** [Resolve when reaching the step that needs the answer]
- **Resolved Q&A / Decisions:** [Every operator answer with question, answer, date]

**Blockers:**
- **Status:** none | waiting on operator | waiting on file | check failed | blocking question
- **Pause reason:** [e.g. "Waiting for association name and as-of date", "Missing ACC sketch"]
- **Last failure / Retry state:** [For recovery on continue]

**Completion:**
- **Completion status:** not started | in progress | done
- **Last session summary:** [One paragraph: what was done, next step, what's needed from the operator]

### Update Procedures

After a workflow step:

1. Record the step id, produced paths, and check result (exit code + log path under `evidence/`).
2. Set Next action to the next YAML step whose `needs` exist, or to wait for operator if a gate or missing file blocks.
3. Do not mark the job complete if blocking questions remain or if later YAML steps have not passed.

After an operator answer: move the item from Open questions to Resolved Q&A in the same response, then set Next action to the unblocked step.

At session end: write Last session summary on both the Work Item journal and `STATUS.md`.

Extra workers must not edit the journal. Only this chat, using this skill.

`next_action` examples: `define-role`, `wait for operator`, `continue`, a workflow step id (`list`, `columns`, `write`), `promote-facts-rules`.
