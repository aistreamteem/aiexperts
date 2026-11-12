# Manager AI Experts

Each folder is a separate expert. Open the folder as the workspace so its `CLAUDE.md` is the agent contract. Each expert uses the same journal layout as `D:\ClaudeAIExpert`: an expert journal, a flat journal for the work item, and branch notes loaded by a Claude PreToolUse hook.

| Folder | Manager type | Planned workflow | Urgent workflow |
| --- | --- | --- | --- |
| [engineering-manager](engineering-manager) | Engineering manager | Team Delivery | Team Escalation |
| [program-manager](program-manager) | Program manager | Program Delivery | Program Escalation |
| [product-manager](product-manager) | Product manager | Product Initiative | Product Escalation |
| [general-manager](general-manager) | General manager | Management Initiative | Management Escalation |

On the first start, the expert asks you to define the specific role, including notes you already have from doing the job. "Continue" does not answer those questions. After you approve the role, work items use the expert journal and the active branch, the charter and plan gates, and the facts and rules for that workflow. Fixed choices use AskUserQuestion.

Each expert also supports **operator-qa** sessions under `qa-sessions/` for journaled clarification (AskUserQuestion for closed choices, chat for open-ended).
