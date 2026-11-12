---
name: scaffold-project
description: "Use when the journal says the next action is \"run scaffold-project\" (after task-breakdown and git-workflow setup). Creates the project skeleton per the approved DD."
trigger: Journal says next action is "run scaffold-project" (after task-breakdown)
---
> **Not used by this mortgage-processor Expert.** Prefer **continue**, **workflow-selector**, and the registered jobs under `.claude/workflows/`. Do not invent developer HLD/DD/git phase skills or a production-incident workflow for this role.

# Scaffold Project

## Journal layer

Step notes and the next action go on the active node through journal-keeper, in `journals/work-items/<id>/nodes/`. Do not write them to `journals/work-items/<id>/progress.md`. Use AskUserQuestion for a fixed choice.

Creates repo layout, config, tooling, and CI skeleton from the design. Use when task breakdown is done and before implementation.

## When to use

- Journal says next action is "run scaffold-project" (after task-breakdown)
- User asks to scaffold or set up the project structure

## Instructions

### 0. Work Item context

- Active work item: the line in `.claude/active-context.txt`, formatted `work-item:<id>`.
- Artifacts (spec, docs, TODOS, STATUS, facts): `work-items/<id>/`.
- Journal: `journals/work-items/<id>/progress.md` for item-wide fields, `state.json` for the
  branch map, and `nodes/<active leaf>.md` for step notes, open questions, and the next action.
  Write through journal-keeper.

