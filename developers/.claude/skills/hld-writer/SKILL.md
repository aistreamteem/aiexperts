---
name: hld-writer
description: "Use when the journal says the next action is \"run hld-writer\" (after spec-parser and blocking requirement questions are answered). Writes the high-level design and its diagrams for the active Work Item, then waits for HLD approval."
trigger: Journal says next action is "run hld-writer"
---

# HLD Writer

## Journal layer

Step notes and the next action go on the active node through journal-keeper, in `journals/work-items/<id>/nodes/`. Use AskUserQuestion for a fixed choice.

Produces the High-Level Design (architecture, components, data flow, external dependencies, risks) and its diagrams. Part of the developer pipeline: spec-parser -> **hld-writer** -> dd-writer -> diagram-generator -> task-breakdown -> ...

## When to use

- Journal says next action is "run hld-writer"
- User asks to write, redo, or extend the HLD for the active Work Item

## Instructions

### 0. Work Item context

- Active work item: the line in `.claude/active-context.txt`, formatted `work-item:<id>`.
- Artifacts (spec, docs, TODOS, STATUS, facts): `work-items/<id>/`.
- Journal: `journals/work-items/<id>/progress.md` for item-wide fields, `state.json` for the
  branch map, and `nodes/<active leaf>.md` for step notes, open questions, and the next action.
  Write through journal-keeper.

### 1. Load context

1. Read `MyRole.txt`. If `Role status` is `pending`, stop and run define-role.
2. Read the journal for this turn (hook text, or the expert journal, work item journal, `state.json`, and the active node note).
3. Read `work-items/<id>/docs/design/requirements-summary.md`.
4. Load the developer workflow memory: `facts/facts-developer.md`, `facts/rules-developer.md`, plus the shared pair `facts/facts-shared.md` and `facts/rules-shared.md` (start from `facts/MEMORY-INDEX.md`), and the Work Item pair `work-items/<id>/facts/facts.md` and `work-items/<id>/facts/rules.md`. Rules **MUST be followed** (architecture rules, patterns, constraints). Log any rule conflict to the journal.

### 2. Skip check

If `work-items/<id>/docs/design/hld.md` exists **and** the journal says the HLD phase is complete, do not rewrite it. Set the next action to "wait for HLD approval" (or to "run dd-writer" if approval is already recorded) and update the journal through journal-keeper. Stop.

### 3. Blocking questions

If the requirements summary still has blocking (high-risk) questions that affect the architecture, stop and ask the user before writing (use operator-qa when a session is warranted). Do not guess at answers that change the design.

### 4. Ask for a template first

Before writing, ask the user whether they have a team HLD template, best practices, or an existing document to follow for style and structure. If they supply one, follow it. If they do not, use the default structure below. Record the answer in the journal.

### 5. Choose the HLD profile

Only the **Standard** profile exists in this scaffold. Use Standard. Do not offer or invent Part 1 or Extended profiles, and do not create profile documents. Record "HLD profile: Standard" in the journal.

### 6. Write the HLD

Write `work-items/<id>/docs/design/hld.md`. Default Standard structure:

1. Purpose, scope, and out of scope
2. Requirements summary and constraints (link to `requirements-summary.md`)
3. Architecture overview (components, responsibilities, boundaries)
4. Data flow and key interactions
5. Technology choices and rationale (record significant decisions under `docs/decisions/`)
6. External dependencies and integrations (APIs, libraries, downloads, repos)
7. Non-functional considerations (security, performance, reliability, observability)
8. Risks
9. Assumptions
10. Open questions, each marked **blocking** or **deferred**
11. Likely blockers (see step 8)

Apply the loaded architecture rules and note where each one shaped the design.

### 7. Diagrams

Create professional Mermaid diagrams as `work-items/<id>/docs/diagrams/*.mmd`: at minimum a system/context (C4-style) diagram and a component or data-flow diagram; add a sequence diagram for the main flows and an ER diagram if there is a persistent data model. Create or update `work-items/<id>/docs/diagrams/index.html` so every diagram is listed and viewable, and reference the diagrams from `hld.md`. Not oversimplified sketches. The HLD is not complete until its diagrams exist.

### 8. Name likely blockers

List, in the HLD and in the journal, anything that could stop later work: downloads (libraries, model files, repos), credentials or API keys, network or system access, licences, external approvals. For each, say what is needed and who provides it. Anticipate; ask the user follow-up questions now rather than at implementation time. If a library or repo is needed and its URL is unknown, ask the user for it. Do not skip or assume a workaround.

### 9. Proactive detection

If the user corrects the design or gives a constraint, use the remember skill to propose capturing it as a fact or rule (ask Work Item vs Expert Role scope).

### 10. Update the journal and stop at the gate

Through journal-keeper: phase = HLD written, Artifacts = `hld.md` and the diagram paths, assumptions, open questions (blocking / deferred), likely blockers, template choice, HLD profile. Set the next action to **"wait for HLD approval"**. Tell the user the HLD and diagrams are ready and ask for explicit approval ("I approve the HLD") or waiver ("Skip HLD approval"). "Continue" is not approval. Do not start dd-writer until approval or waiver is recorded ("HLD approved on <date>").
