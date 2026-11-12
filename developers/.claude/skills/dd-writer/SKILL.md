---
name: dd-writer
description: "Use when the journal says the next action is \"run dd-writer\" (after the HLD is approved or the gate is waived). Writes the detailed design (APIs, data models, interfaces, sequencing, run environment) and its diagrams, then waits for DD approval."
trigger: Journal says next action is "run dd-writer"
---

# DD Writer

## Journal layer

Step notes and the next action go on the active node through journal-keeper, in `journals/work-items/<id>/nodes/`. Use AskUserQuestion for a fixed choice.

Produces the Detailed Design from the approved HLD: concrete enough that task-breakdown can list every setup, install, scaffold, and implementation task from it.

## When to use

- Journal says next action is "run dd-writer"
- User asks to write, redo, or extend the DD for the active Work Item

## Instructions

### 0. Work Item context

- Active work item: the line in `.claude/active-context.txt`, formatted `work-item:<id>`.
- Artifacts (spec, docs, TODOS, STATUS, facts): `work-items/<id>/`.
- Journal: `journals/work-items/<id>/progress.md` for item-wide fields, `state.json` for the
  branch map, and `nodes/<active leaf>.md` for step notes, open questions, and the next action.
  Write through journal-keeper.

### 1. Load context and check the gate

1. Read `MyRole.txt`. If `Role status` is `pending`, stop and run define-role.
2. Read the journal for this turn (hook text, or the expert journal, work item journal, `state.json`, and the active node note).
3. Confirm the journal records "HLD approved on <date>" or an explicit waiver. If not, do not write the DD: re-prompt the user for approval ("I approve the HLD" or "Skip HLD approval"). "Continue" is not approval.
4. Read `work-items/<id>/docs/design/hld.md`, the requirements summary, and the HLD's open questions and likely blockers.
5. Load the developer workflow memory: `facts/facts-developer.md`, `facts/rules-developer.md`, plus `facts/facts-shared.md` and `facts/rules-shared.md` (start from `facts/MEMORY-INDEX.md`), and the Work Item pair `work-items/<id>/facts/facts.md` and `work-items/<id>/facts/rules.md`. Rules **MUST be followed** (design patterns, coding standards, testing requirements).

### 2. Skip check

If `work-items/<id>/docs/design/dd.md` exists **and** the journal says the DD phase is complete, do not rewrite it. Set the next action to "wait for DD approval" (or "run diagram-generator" / "run task-breakdown" if approval is already recorded) through journal-keeper. Stop.

### 3. Resolve blocking questions

If any HLD question marked **blocking** is still open and affects the design, ask the user now. Do not design around an unanswered high-risk question.

### 4. Template

If the user gave a team template or example for the HLD, ask whether the same one applies to the DD. If none was given, ask once. Record the answer in the journal.

### 5. Write the DD

Write `work-items/<id>/docs/design/dd.md`. Cover:

1. **Module / package layout**: directories, modules, responsibilities.
2. **APIs and interfaces**: endpoints, CLI commands, function and class signatures, request/response and error contracts, versioning.
3. **Data models**: entities, fields, types, constraints, storage schema, migrations.
4. **Sequencing**: runtime flows and call order for the main scenarios, including error and retry paths.
5. **Configuration and secrets**: settings, environment variables, where secrets come from.
6. **Error handling, logging, and observability.**
7. **Test strategy**: unit, integration, and e2e scope, test data, and the commands that run each (`tests/unit/`, `tests/integration/`, `tests/e2e/`).
8. **Run environment and setup requirements** (see step 6).
9. **Traceability**: map each HLD component to its DD section.
10. **Open questions** marked **blocking** or **deferred**, and assumptions.

Apply the loaded design rules and note where each shaped the design.

### 6. Run environment and setup requirements (explicit)

task-breakdown depends on this section, so state it fully, in install order:

- Runtime and language versions (e.g. portable Python, Node, .NET, Visual Studio solution).
- Environment to create first (venv, portable Python folder, node project, solution) and its location.
- Libraries and packages with versions, and the installer for each (pip, npm, NuGet), noting that each runs inside the environment above.
- Repositories or files to obtain (GitHub repos, model files, SDKs) with the **URL** for each. If a URL is unknown, ask the user. Do not skip it.
- Credentials, API keys, ports, services, OS or hardware needs.
- The exact commands to **run the app locally** and **run the full test suite**.

The agent performs this setup; do not leave it to the user. Name likely blockers and ask the user about them now.

### 7. Diagrams

Create or update professional Mermaid diagrams in `work-items/<id>/docs/diagrams/*.mmd`: component/class diagrams, sequence diagrams for the main flows, ER diagram for the data model, state diagrams where behaviour is stateful, and a deployment/run-environment diagram. Update `work-items/<id>/docs/diagrams/index.html` and reference each diagram from `dd.md`. The DD is not complete until its diagrams exist. (diagram-generator can later regenerate or sync them.)

### 8. Proactive detection

If the user corrects a design choice or states a constraint, use the remember skill to propose capturing it as a fact or rule.

### 9. Update the journal and stop at the gate

Through journal-keeper: phase = DD written, Artifacts = `dd.md` and diagram paths, run environment summary, open questions, likely blockers. Set the next action to **"wait for DD approval"**. Ask the user for explicit approval ("I approve the DD") or waiver ("Skip DD approval"). "Continue" is not approval. Do not run task-breakdown, scaffold, or implement until approval or waiver is recorded ("DD approved on <date>").
