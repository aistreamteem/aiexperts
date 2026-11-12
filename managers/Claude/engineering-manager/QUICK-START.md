# Quick Start Guide

## What This Is

An expert system for an Engineering Manager. It turns a management request into a charter, an operating plan, diagrams, actions, verification, and a close-out. All work-item state lives in a Work Item (`WID-…`). The role itself is defined before the first work item.

## Getting Started

Open this folder and say **"start"**, **"continue"**, or **"define my role"**.

1. If `MyRole.txt` says `Role status: pending`, the define-role skill asks about the specific job, the workflows, the skills, and any notes you already have from doing this work without an AI expert.
2. "Continue" does not answer those questions and does not approve the role.
3. After you say "I approve the role" (or "Skip role definition"), say **start** again and give a Work Item id such as `WID-21411151`.
4. Choose **Team Delivery** or **Team Escalation**.
5. The journal's next action is the only step that runs.

## Planned pipeline

`intake → charter-writer → plan-writer → diagram-generator → action-breakdown → kickoff → execute-action → verify → close-out → done`

## Urgent pipeline

`assess-situation → analyze-impact → respond → monitor-situation → resolve-and-document → done`

## Human gates

- Charter: "I approve the charter" or "Skip charter approval"
- Plan: "I approve the plan" or "Skip plan approval"
- Change: "I approve the change" or "Skip change approval"
- Escalation response: "I approve the response" or "Skip response approval"
- Role: "I approve the role" or "Skip role definition"

## What you can say

| What you say | What happens |
| --- | --- |
| "start" / "continue" / "resume" | Next step in the journal, or role definition if the role is pending |
| "define my role" | Run role onboarding again |
| "switch to work item WID-…" | Point later steps at that work item |
| "I approve the charter" | Clear the charter gate |
| "I approve the plan" | Clear the plan gate |
| "remember this …" | Store a fact or a rule |
| "integrate this …" | Fold a document into facts, rules, and MyRole.txt |
| "promote facts/rules" | Review work-item learnings for expert-role memory |
| "ask me" / "clarify" / "Q&A" / "verify this with me" | Open an **operator-qa** session under `qa-sessions/`; AskUserQuestion for closed choices, chat for open-ended |
| "change request" | Start a change for a change to scope, date, or staffing |
| "improve ways of working" | Clean up cadence, trackers, or decision hygiene |

## Example

```
You: start
Agent: Role status is pending. I will define the Engineering Manager role before any work item.

       What is your exact title, and who does this role serve?
You: [your answer]
Agent: [records it and asks the next question, including notes you already have]

You: I approve the role
Agent: What are you working on? (work item WID-XXXXXXXX)
You: WID-21411151
Agent: Which workflow applies?
       1. Team Delivery
       2. Team Escalation
You: 1

       Blocking questions:
1. What outcome is this team accountable for?
2. Who is on the team and who decides?
3. What does success look like this period?
4. What staffing or dependency constraint is already known?
You:
1. Lower incident load for the payments squad.
2. The payments squad. I decide day-to-day work. Headcount is not mine to approve.
3. Fewer severe incidents this quarter.
4. One open role is not approved to fill yet.
Agent: [records the answers]
       [writes the charter after you choose a depth]
       Charter is ready. Reply "I approve the charter" to proceed.
```

## Journal locations

| What | Where |
| --- | --- |
| Active work item | `.claude/active-context.txt` |
| Expert journal | `journals/expert/progress.md` |
| Work-item journal | `journals/work-items/<id>/progress.md` |
| Artifacts | `work-items/<id>/` |

## Learn more

- `CLAUDE.md` — operating rules
- `MyRole.txt` — role and pipelines
- `.claude/workflows/team-delivery.md` — planned phases
- `.claude/workflows/team-escalation.md` — urgent phases
- `docs/manager-operating-system.md` — longer description
