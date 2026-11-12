---
name: workflow-selector
description: "Use when the continue skill finds the journal missing a workflow type, or when starting a new Work Item. Reads the workflow registry and prompts the user to select an enabled gym role job."
disable-model-invocation: false
---

# Workflow Selector

Presents the gym / fitness front role job menu and records selection in the Work Item journal.

## When to use

- Called by continue when the journal is missing "Workflow type"
- On new Work Item initialization

## Instructions

1. **Determine context type:**
 - Read `.claude/active-context.txt` to get `context_type` and `context_id`

2. **Read workflow registry:**
 - Read `.claude/workflows/workflow-registry.json`

3. **Present menu from the registry only:**

 List each workflow as a numbered line: name, then the description. Do not offer a workflow that is not in the registry. Do not offer software-build or incident-response jobs.

 Role jobs live under `.claude/workflows/` (one instruction file per job). Until the operator picks another job, the default is `check-in-day` (today’s scan list).

 Typical pairing:
 - Daily floor traffic → Check In Day
 - Denied or frozen scans → Access Flag Exceptions
 - Guests / day passes → Guest Pass Log
 - Unsigned forms → Missing Waivers
 - Holds and terminations → Freeze And Cancel List
 - NSF / declined dues → Failed Draft List
 - Group class headcount → Class Roster
 - Trainer session punches → Pt Session Counts
 - End of day retail / tender → Retail Close

4. **Accept user input:** a number, a registry key (`check-in-day`), or a display name (`Check In Day`).

5. **Validate selection:** Ensure the workflow exists in the registry. If invalid, re-prompt.

6. **Ask context-specific questions:**
 - "What is the Work Item ID or job folder? (e.g., WID-21411151, 2026-11-08-check-in, or a member/class label)"
 - "Any files to use? (membership export, scan CSV, waiver folder, freeze log, price sheet)"

7. **Record in journal:**
 - Write `Workflow type` on `journals/work-items/<id>/progress.md` when that field is missing. Do not replace `active`.
 - Set `Context ID: <context_id>`
 - Set **Current phase:** `intake`
 - Set **Next action:** first YAML step id from the selected workflow file (usually the first `id:` under `steps:`)
 - Put `Next action` on `nodes/work-item.md` only when `active` is still just `work-item`

8. **Write active context file:**
 - `.claude/active-context.txt` as `<context_type>:<context_id>`
 Do not write the legacy `.claude/active-work-item.txt`

9. **Confirm to user:**

 Work Item initialized with \<workflow-name>
 Initial phase: intake
 Next action: first ready step in the workflow file (read tool doc, produce artifact under the Work Item, run check) → journal-keeper

## Workflow-specific fields

**Role job:**
- Job id (registry key)
- Work Item folder `work-items/<id>/` (`in/`, `work/`, `out/`, `evidence/`)
- No software-build or production-incident fields

## Notes

- Called by continue when journal is missing workflow type
- Backward compatibility: If the journal has "Pipeline" but no "Workflow type", map `operations` and `developer` to `check-in-day` unless they name another registered job
