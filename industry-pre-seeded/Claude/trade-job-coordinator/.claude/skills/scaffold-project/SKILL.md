---
name: scaffold-project
description: "Use when the journal says the next action is \"run scaffold-project\" (after task-breakdown and git-workflow setup). Creates the project skeleton per the approved DD."
disable-model-invocation: false
---

> **Not used by this trade-job-coordinator Expert.** Prefer **continue**, **workflow-selector**, and the registered jobs under .claude/workflows/. Do not invent developer HLD/DD/git phase skills or a production-incident workflow for this role.

# Scaffold Project

## Journal layer

### 0. Work Item context

- Active work item: the line in `.claude/active-context.txt`, formatted `work-item:<id>`.
- Artifacts (spec, docs, TODOS, STATUS, facts): `work-items/<id>/`.
- Journal: `journals/work-items/<id>/progress.md` for item-wide fields, `state.json` for the
  branch map, and `nodes/<active leaf>.md` for step notes, open questions, and the next action.
  Write through journal-keeper.

Use AskQuestion for a fixed choice.

Creates repo layout, config, tooling, and CI skeleton from the design. Use when task breakdown is done and before implementation.

## When to use

- Journal says next action is "run scaffold-project" (after task-breakdown)
- User asks to scaffold or set up the project structure

## Instructions

### 0. Work Item Context
- Read active Work Item ID from `.claude/active-context.txt` (`work-item:<id>`)
- Journal: `journals/work-items/<id>/progress.md`
- Use Work Item-scoped paths for all artifacts


1. Read the journal. If the scaffold phase is already complete and the expected artifacts (e.g. src/, config) exist, skip scaffolding: set next action to "implement-feature (task 1/N)" (using the total task count from TODOS.md) and update the journal.
2. Otherwise read `docs/design/dd.md` and `TODOS.md` and create the project structure: directory layout, config files, tooling, and CI skeleton as implied by the design.
3. **If the agent needs a library, package URL, or other resource**: Ask the user for the URL (e.g. GitHub repo or other download location) if not known or if the default fails. Do not skip the step.
4. **If scaffold fails or the agent needs anything to unblock** (e.g. package install fails, clone fails, download fails, missing URL): do **not** skip. Explain the situation to the user and ask for help. Describe what failed or what is needed, record in the journal (Blockers / Last failure), and ask the user for the URL or other input. Only continue when the user provides what is needed or agrees on next steps.
5. Update the journal: set phase to scaffold done, Artifacts to include the created paths, next action to "implement-feature (task 1/N)".
