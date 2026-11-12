---
name: dd-writer
description: "Use when the journal says the next action is \"run dd-writer\" (after the HLD is approved). Writes the detailed design (APIs, data models, interfaces, sequencing, run environment) and its diagrams, and stops at the DD approval gate."
disable-model-invocation: false
---

# DD Writer

## Journal layer

Step notes and the next action go on the active node through journal-keeper, in `journals/work-items/<id>/nodes/`. Use AskQuestion for a fixed choice.

Produces the detailed design (DD) from the approved HLD. Use after the HLD gate clears and before diagram-generator and task-breakdown.

## When to use

- Journal says next action is "run dd-writer" (HLD approved or waived)
- User asks to write or redo the detailed design

## Instructions

### 0. Work Item context

- Active work item: the line in `.cursor/active-context.txt`, formatted `work-item:<id>`.
- Artifacts (spec, docs, TODOS, STATUS, facts): `work-items/<id>/`.
- Journal: `journals/work-items/<id>/progress.md` for item-wide fields, `state.json` for the
  branch map, and `nodes/<active leaf>.md` for step notes, open questions, and the next action.
  Write through journal-keeper.

1. Read the journal. Confirm the HLD approval (or waiver) is recorded; if not, stop and re-prompt for it. If `docs/design/dd.md` exists and the journal says the DD phase is complete, skip writing: set next action to "wait for DD approval" (or, if approval is already recorded, "run diagram-generator") and update the journal.
2. Read `docs/design/hld.md`, `docs/design/requirements-summary.md`, and the loaded rules (`facts/rules-developer.md`, `facts/rules-shared.md`, `work-items/<id>/facts/rules.md`). Rules **MUST be followed**; apply design patterns and coding standards, and log them in the journal.
3. Ask whether the user has a team DD template or example to follow, if the HLD step did not already settle it. Follow the template when one exists.
4. **Write `docs/design/dd.md`** covering:
   - **APIs and interfaces**: endpoints, function or class contracts, inputs, outputs, errors.
   - **Data models**: entities, fields, relationships, storage, migrations.
   - **Component design**: module and class responsibilities, dependencies between them.
   - **Sequencing**: key runtime flows, error and retry paths.
   - **Testing approach**: unit, integration, and e2e scope, informed by the loaded rules.
5. **State the run environment and set-up requirements explicitly** in a dedicated DD section. task-breakdown depends on it. List, in install order: runtimes (portable Python, Node, .NET, Visual Studio solution), virtual environments, packages and libraries with versions, repositories or downloads to obtain (with URLs), model files, credentials or config, and the commands to run the app locally. Do not assume anything is already installed.
6. **Write the detailed diagrams** to `docs/diagrams/*.mmd` using Mermaid (component or class, sequence, ER, state where useful). Update `docs/diagrams/index.html` and reference the diagrams from `dd.md`.
7. **List assumptions and open questions** as **blocking** or **deferred**, and name likely blockers (downloads, credentials, access, missing URLs). Ask the user; do not skip a blocked item or assume a workaround. Record blockers in the journal.
8. Update the journal: Last completed = dd-writer, Artifacts = `docs/design/dd.md`, new diagram files, `index.html`, and open questions. Set next action to **"wait for DD approval"**.
9. Tell the user to review the DD and its diagrams and reply "I approve the DD" or "Skip DD approval". Do not start task-breakdown, scaffold, or implementation until they do. "Continue" is not approval. When approval comes, record "DD approved on <date>" in the journal in the same response and set next action to "run diagram-generator" (per `.cursor/workflows/developer.md`) or, if diagrams are already current, "run task-breakdown".
