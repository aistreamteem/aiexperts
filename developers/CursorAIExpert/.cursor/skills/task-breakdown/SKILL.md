---
name: task-breakdown
description: "Use when the journal says the next action is \"run task-breakdown\" (after the DD is approved and diagrams are current). Fills work-items/<id>/TODOS.md from the DD, with environment set-up before package installs and numbered tasks."
disable-model-invocation: false
---

# Task Breakdown

## Journal layer

Step notes and the next action go on the active node through journal-keeper, in `journals/work-items/<id>/nodes/`. Use AskQuestion for a fixed choice.

Turns the approved design into an ordered, numbered task list. Use after dd-writer and diagram-generator, before git-workflow (setup).

## When to use

- Journal says next action is "run task-breakdown"
- User asks to break the design into tasks or rebuild the task list

## Instructions

### 0. Work Item context

- Active work item: the line in `.cursor/active-context.txt`, formatted `work-item:<id>`.
- Artifacts (spec, docs, TODOS, STATUS, facts): `work-items/<id>/`.
- Journal: `journals/work-items/<id>/progress.md` for item-wide fields, `state.json` for the
  branch map, and `nodes/<active leaf>.md` for step notes, open questions, and the next action.
  Write through journal-keeper.

1. Read the journal. If `TODOS.md` is already filled and the journal says the task-breakdown phase is complete, skip: set next action to "run git-workflow (setup)" and update the journal.
2. Read `docs/design/dd.md` (especially its run environment and set-up section), `docs/design/hld.md`, and the loaded rules. Read `work-items/_TEMPLATE/TODOS.md` for the structure.
3. **Fill `work-items/<id>/TODOS.md` section by section, in the template's order:**
   1. **Setup / Environment Tasks**: portable Python, venv, Node/npm, Visual Studio solution, or any other runtime or dev environment from the DD. **These come first.**
   2. **Library / Dependency Installation**: pip, NuGet, npm, and other installs, run inside or against the environment from the previous section. **No package install may precede the environment task it depends on.**
   3. **Scaffold Tasks**: project structure, config files, CI skeleton.
   4. **Implementation Tasks**: ordered tasks from the design, each small enough to implement and test in one step.
   5. **Testing Tasks**: unit, integration, and e2e tests (rule 14); keep tests next to the tasks they cover where the rules require it.
   6. **Documentation Tasks**: README, API docs, deployment guides.
4. **Add tasks to obtain anything the design needs**: clone or download each repository, library, or model file named in the DD, or document the URL for the user to provide. These tasks go in the Setup section, before the installs that need them. The agent does these tasks; they are not left to the user. If a URL is unknown, ask the user now.
5. **Number the tasks 1 to N** continuously across all sections, so "implement-feature (task K/N)" has an N. Set the `Work Item`, `Pipeline`, and `Status` header fields (for example `Status: Not started`).
6. Raise any blocking question about scope or environment with the user; do not guess. Record blockers in the journal.
7. Update the journal: Last completed = task-breakdown, Artifacts = `TODOS.md`, total task count N, and open questions. Set next action to **"run git-workflow (setup)"**.
