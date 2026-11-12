# Quick Start Guide

## What This Is

An expert system for a Product Manager. It turns a management request into a opportunity brief, a product plan, diagrams, actions, verification, and a close-out. All work-item state lives in a Work Item (`WID-…`). The role itself is defined before the first work item.

## Getting Started

Open this folder and say **"start"**, **"continue"**, or **"define my role"**.

1. If `MyRole.txt` says `Role status: pending`, the define-role skill asks about the specific job, the workflows, the skills, and any notes you already have from doing this work without an AI expert.
2. "Continue" does not answer those questions and does not approve the role.
3. After you say "I approve the role" (or "Skip role definition"), say **start** again and give a Work Item id such as `WID-21411151`.
4. Choose **Product Initiative** or **Product Escalation**.
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
| "change request" | Start a change for a change to priority, scope-now, or the success metric |
| "improve ways of working" | Clean up cadence, trackers, or decision hygiene |

## Example

```
You: start
Agent: Role status is pending. I will define the Product Manager role before any work item.

       What is your exact title, and who does this role serve?
You: [your answer]
Agent: [records it and asks the next question, including notes you already have]

You: I approve the role
Agent: What are you working on? (work item WID-XXXXXXXX)
You: WID-21411151
Agent: Which workflow applies?
       1. Product Initiative
       2. Product Escalation
You: 1

       Blocking questions:
1. What problem is this, and for whom?
2. What outcome would show it is solved?
3. What is explicitly out of scope?
4. Who must agree before this plan is current?
You:
1. Checkout drop-off for new buyers.
2. A higher completion rate.
3. A full rewrite is out of scope.
4. The outcome owner must agree before the plan is current.
Agent: [records the answers]
       [writes the opportunity brief after you choose a depth]
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
- `.claude/workflows/product-initiative.md` — planned phases
- `.claude/workflows/product-escalation.md` — urgent phases
- `docs/manager-operating-system.md` — longer description
