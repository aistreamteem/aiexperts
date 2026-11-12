---
name: hld-writer
description: "Use when the journal says the next action is \"run hld-writer\" (after spec-parser). Writes the high-level design and its diagrams, lists assumptions and open questions, and stops at the HLD approval gate."
disable-model-invocation: false
---

# HLD Writer

## Journal layer

Step notes and the next action go on the active node through journal-keeper, in `journals/work-items/<id>/nodes/`. Use AskQuestion for a fixed choice.

Produces the high-level design (HLD) and its diagrams from the requirements summary. Use after spec-parser and before dd-writer. The HLD uses the **Standard** profile (context and architecture).

## When to use

- Journal says next action is "run hld-writer"
- User asks to write or redo the high-level design

## Instructions

### 0. Work Item context

- Active work item: the line in `.cursor/active-context.txt`, formatted `work-item:<id>`.
- Artifacts (spec, docs, TODOS, STATUS, facts): `work-items/<id>/`.
- Journal: `journals/work-items/<id>/progress.md` for item-wide fields, `state.json` for the
  branch map, and `nodes/<active leaf>.md` for step notes, open questions, and the next action.
  Write through journal-keeper.

1. Read the journal. If `docs/design/hld.md` exists and the journal says the HLD phase is complete, skip writing: set next action to "wait for HLD approval" (or, if approval is already recorded, "run dd-writer") and update the journal.
2. Read `docs/design/requirements-summary.md`. Load the Expert Role rules (`facts/rules-developer.md`, `facts/rules-shared.md`) and the Work Item rules (`work-items/<id>/facts/rules.md`). Rules **MUST be followed**; apply architecture rules to the design and log them in the journal.
3. **Ask for a team template or example first.** Before writing, ask whether the user has a team HLD template, best practices, or an existing document to follow for style and structure. Use AskQuestion for a fixed choice (template / example document / none). Wait for the answer; do not write generic documents when a template exists.
4. **Choose the HLD profile.** Only **Standard** exists (context and architecture). Record `HLD profile: standard` in `progress.md` through journal-keeper.
5. **Write `docs/design/hld.md`**, following the template if one was supplied. Cover context, scope, architecture, major components and their responsibilities, key data and control flows, external dependencies, and constraints from the rules.
6. **Write the diagrams** to `docs/diagrams/*.mmd` using Mermaid, as a senior architect would: system context, architecture or C4-style container view, key sequences, and an ER or data view when entities matter. Update `docs/diagrams/index.html` so each diagram renders in a browser, and reference the diagrams from `hld.md`. Use **diagram-generator** only to rebuild or resynchronize them later.
7. **List assumptions and open questions** in `hld.md` and in the node note. Mark each question **blocking** (high-risk or high-priority; work that depends on it cannot proceed) or **deferred** (can wait for the phase or task that needs it). Do not mark the phase complete while a blocking question is unanswered; ask the user.
8. **Name likely blockers**: downloads, credentials, API keys, network or system access, libraries or repos that need a URL. Ask the user for help now, agree on how to proceed, and record them in the journal (Blockers). Do not assume a workaround.
9. Update the journal: Last completed = hld-writer, Artifacts = `docs/design/hld.md`, the diagram files, and `docs/diagrams/index.html`, HLD profile, and open questions. Set next action to **"wait for HLD approval"**.
10. Tell the user to review the HLD and its diagrams and reply "I approve the HLD" or "Skip HLD approval". Do not start dd-writer until they do. "Continue" is not approval; if the next action is still the wait, only re-prompt. When approval comes, record "HLD approved on <date>" in the journal in the same response and set next action to "run dd-writer".
