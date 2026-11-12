---
name: journal-keeper
description: >-
  Update journals/expert and the active Work Item journal after role work,
  decisions, or session end. Use whenever the next action or the day's story changes.
---

# Journal keeper

Keep a readable expert journal and Work Item journal so **continue** works.

## When to use

- After every veterinary-role map step, operator answer, or completed artifact
- After define-role, workflow-selector, or remember
- At session end (Last session summary)
- When facts/rules are loaded or proposed

## Where notes go

- Expert journal: `journals/expert/progress.md` (current work item line, future work that is not a work item yet)
- Work item journal: `journals/work-items/<id>/progress.md` (premise, goal, workflow type, decisions every branch inherits, completion status)
- Branch map: `journals/work-items/<id>/state.json` (`active` path and `history` only)
- Node notes: `journals/work-items/<id>/nodes/<node-id>.md` (step notes, questions, next action)
- Background-agent notes: `journals/work-items/<id>/agent-notes/` (see that folder’s README). Merged notes land in the active leaf node, not in `progress.md`.

Preserve the exact `Current work item:` line. Only **continue** and **switch-context** may change it.

`active` is the path from `work-item` to the leaf. A blocking question becomes the active leaf. Its id is unique and is not `work-item` or a phase name.

### 0. Work Item context

- Active work item: the line in `.cursor/active-context.txt`, formatted `work-item:<id>` (legacy `.cursor/active-work-item.txt` as read fallback only).
- Artifacts (spec, docs, TODOS, STATUS, facts): `work-items/<id>/`.
- Journal: `journals/work-items/<id>/progress.md` for item-wide fields, `state.json` for the
  branch map, and `nodes/<active leaf>.md` for step notes, open questions, and the next action.
  Write through journal-keeper.

## Where each field lives

| File | Fields |
| --- | --- |
| `journals/work-items/<id>/progress.md` | Work item ID and description; Work item record; Workflow type and workflow-specific context; Mode; Decisions and approvals that every branch inherits; Completion status |
| `journals/work-items/<id>/nodes/<node>.md` | Last completed; Next action; Open questions (blocking and deferred); Q&A resolved in this step; Blockers, pause reason, last failure; facts and rules loaded and applied; proactively detected facts and rules; step notes |
| `work-items/<id>/STATUS.md` | Last session summary; Artifacts list; links |
| Not stored | Current phase. It is the phase node on the `active` path in `state.json` |

## Journal schema (values)

- **Work Item ID:** `WID-XXXXXXXX` or pack name
- **Work Item description:** clinic date, patient/client pack, records request, estimate, or boarding drop-off
- **Workflow type:** registry id (`day-appointments` | `emergency-flag` | `new-client-forms` | `records-in` | `records-out` | `reminder-list` | `estimate-from-prices` | `checkout-list` | `board-dropoff`)
- **Last completed:** YAML step id or pack
- **Next action:** next YAML step id, wait for file, wait for operator, pack, done
- **Artifacts:** paths relative to the Work Item folder (`in/…`, `work/…`, `out/…`, `evidence/…`) — list in STATUS
- **Facts and rules:** Work Item `facts/`; Expert Role from `facts/facts-shared.md` and `facts/rules-shared.md`
- **Completion status:** not started | in progress | done

### Update procedures

**After each step:**
1. Write the step completed to **Last completed** on the active node
2. Add artifacts produced (Work Item-relative paths) in STATUS
3. Set **Next action** to the next YAML `next` step that has its `needs` on disk, or `pack` / `done`
4. Update facts/rules loaded if they were read
5. Do not mark a step complete if blocking questions remain or the check did not exit 0

**When the operator answers:** in the same response, move the Q&A to Resolved and remove it from Open questions.

**At session end:** write Last session summary; optionally refresh `STATUS.md`.

**Trigger audit snapshot:** after the journal update, run `py -3 .cursor/hooks/journal_snapshot.py` if that hook exists. If it fails, log and do not block the role job.

**Merge background-agent notes:** fold appended raw notes into Artifacts, Resolved Q&A, and Next action. `merge_agent_notes.py` / `on_stop.py` own the merge into the active node.

### Next actions (this role)

Follow the selected workflow file. Typical sequence: intake source files → first YAML step → later YAML steps → pack in `out/` → done. Human gates are “wait for file” or “wait for operator”, not design-doc approvals.

### Artifact paths

- `in/` — PIMS exports, PDFs, forms they dropped for this job
- `work/` — indexes and working CSVs
- `out/` — finished list or checklist pack
- `evidence/` — check logs
- `facts/` — Work Item facts and rules
- `TODOS.md` — remaining map steps if useful
- `STATUS.md` — status summary
