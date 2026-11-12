---
name: continue
description: "Use when the operator says continue, start, or resume. Runs define-role while the role is pending, then performs the next journal step. Continue is not an answer and not an approval."
trigger: User says "continue", "start", or "resume"
---

# Continue

## When to use

The operator says "continue", "start", or "resume", or asks to pick up the work.

## Role gate

1. Read `MyRole.txt`.
2. If the operator said "define my role", run define-role and stop.
3. If `Role status` is `pending` or missing, run define-role and stop. Do not ask for a work item.
4. If status is `defined` or `skipped`, continue below.

## Context

5. Read `.cursor/active-context.txt` (`work-item:WID-...`). If missing, read `.cursor/active-work-item.txt` as a legacy fallback only.
6. If nothing is active, ask: "What are you working on? (work item WID-XXXXXXXX)". Write `.cursor/active-context.txt` only.
7. Paths: `work-items/<id>/` for the work product. The flat journal is `journals/work-items/<id>/progress.md`. The map is `journals/work-items/<id>/state.json`. Step notes live in `journals/work-items/<id>/nodes/`.
8. If `work-items/<id>/` does not exist, copy `work-items/_TEMPLATE/`. If `journals/work-items/<id>/` does not exist, copy `journals/work-items/_TEMPLATE/` and set **Work item record** to `work-items/<id>/`. If `journals/expert/progress.md` is missing, copy `journals/_TEMPLATE/expert/progress.md`. Write `Current work item: <id>` in the expert journal.
9. If the flat journal has no `Workflow type`, run workflow-selector. Do not replace `active`. Use the hook journal text when this turn already has it. If it does not, read the expert journal, the flat journal, the map, and only the note files on `active`. A longer path under the same phase stays. When the next phase lies outside the current path, save `history` on the current phase unless `active` is only `work-item`, then set `active` to `work-item`, the phase, and that phase's `history`. After that write, read the new note files once.
10. Load `facts/MEMORY-INDEX.md`, the shared pair (`facts/facts-shared.md`, `facts/rules-shared.md`), then the pair for that workflow: `facts/facts-program-delivery.md` and `facts/rules-program-delivery.md`, or `facts/facts-program-escalation.md` and `facts/rules-program-escalation.md`. Then load the work-item facts and rules. Follow the rules. Log the counts.

## This step only

11. If a blocking question is open, ask it again. Continue is not an answer. When a real answer arrives, record it in the same turn.
12. If a blocker is set, describe it and wait for agreement on how to proceed.
13. If the next action is a wait, re-prompt with the file path and the exact phrase. Do not advance. Phrases: "I approve the charter" or "Skip charter approval"; "I approve the plan" or "Skip plan approval"; "I approve the change" or "Skip change approval"; "I approve the response" or "Skip response approval"; "I approve the role" or "Skip role definition".
14. If the next action is empty or "done", stop and ask what to do next.
15. Otherwise run the single next step:

**Program Delivery (`program-delivery`):**

- "run intake" → `docs/charter/brief.md`, then "run charter-writer"
- "run charter-writer" → `docs/charter/charter.md` titled Charter, diagrams, then "wait for charter approval"
- "run plan-writer" → `docs/plan/operating-plan.md` titled Operating Plan, then "wait for plan approval"
- "run diagram-generator" → `docs/diagrams/`, then "run action-breakdown"
- "run action-breakdown" → `TODOS.md`, then "run kickoff"
- "run kickoff" → cadence, tracker, decision log, stakeholder list, then "execute-action (task 1/N)"
- "execute-action (task K/N)" → one TODO, then the next task or "run verify"
- "run verify" → `docs/verification/verification.md`, then "run close-out"
- "run close-out" → status narrative, decision log, handoff, then "done"
- "run change-request" → `docs/changes/<change-id>/`, then "wait for change approval"
- "run improve-ways-of-working" → clean cadence or trackers without changing the outcome

**Program Escalation (`program-escalation`):**

- "run assess-situation" → `docs/escalations/assessment.md`
- "run analyze-impact" → `docs/escalations/impact.md`, then "wait for response approval"
- "run respond" → `docs/escalations/response.md`
- "run monitor-situation" → `docs/escalations/monitor.md`
- "run resolve-and-document" → `docs/escalations/resolution.md`, then "done"

16. Update the journal (journal-keeper): phase, artifacts, next action, facts and rules loaded.
17. At session end, write Last session summary and refresh STATUS.md.
18. When the work item is done, ask whether to promote facts and rules.

Do not skip a phase the journal still has open. Do not run a skill marked not used in `.cursor/role-skills.md` when that file exists.
