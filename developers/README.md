# Quick Start Guide

## What This Is

An expert system that turns a specification into design docs, diagrams, tasks, code, and tests. All work happens inside a Work Item (`WID-…`). The expert journal and that Work Item's active branch are the source of truth across sessions.

This folder is the Cursor expert. Workflow rules are in `AGENTS.md`. Skills are Cursor Agent Skills in `.cursor/skills/<name>/SKILL.md`. Hooks in `.cursor/hooks.json` load the journal and the rules that match the action about to run. Fixed choices use the AskQuestion tool.

All hooks run with `py -3` (standard library only).

## Structure

```
D:\CursorAIExpert\
|-- AGENTS.md                         Workflow rules
|-- MyRole.txt                        Role and pipeline definitions
|-- QUICK-START.md
|-- docs\
|   `-- spec-to-artifacts-agent-skills-system.md
|-- facts\
|   |-- MEMORY-INDEX.md               Expert memory navigation
|   `-- HOW-MEMORY-LOADING-WORKS.md
|-- scripts\
|   |-- memory\build_trigger_index.py Rebuilds the action-trigger index
|   |-- test_journal_hook.py
|   |-- test_stop_hooks.py
|   `-- test_rules_hook.py
|-- journals\
|   |-- expert\progress.md            Expert journal (current work item, future work)
|   `-- work-items\<WID>\             progress.md, state.json, nodes\ (from journals\work-items\_TEMPLATE\)
|-- work-items\_TEMPLATE\             Copied when a Work Item is created (artifacts only, no journal)
|-- qa-sessions\_TEMPLATE\            Copied when an operator Q&A session is created
`-- .cursor\
    |-- hooks.json                    Cursor hook events
    |-- CONTEXT-SYSTEM.md             Active Work Item pointer
    |-- active-context.txt            work-item:WID-...
    |-- workflows\
    |   |-- workflow-registry.json    developer pipeline
    |   |-- developer.md              Phase sequence and gates
    |   `-- README.md
    |-- hooks\
    |   |-- inject_journal_context.py Journal text for the turn and each tool
    |   |-- inject_rules_on_action.py Rules for the action about to run
    |   |-- journal_fields.py         Shared journal field helpers
    |   |-- merge_agent_notes.py      Merges agent-notes into the active node
    |   |-- journal_snapshot.py       Audit commit of journal paths
    |   `-- on_stop.py                stop and subagentStop entry point
    `-- skills\
        |-- define-role\SKILL.md      Define the developer role before work items
        |-- continue\SKILL.md         Resume from the journal
        |-- workflow-selector\SKILL.md Choose a pipeline for a new Work Item
        |-- switch-context\SKILL.md   Change the active Work Item
        |-- spec-parser\SKILL.md      Parse a spec and raise blocking questions
        |-- hld-writer\SKILL.md       Write the HLD and diagrams (Standard profile)
        |-- dd-writer\SKILL.md        Write the DD, diagrams, and run environment
        |-- diagram-generator\SKILL.md Rebuild diagrams from HLD/DD
        |-- task-breakdown\SKILL.md   Build the numbered TODOS list
        |-- git-workflow\SKILL.md     Branch, commit, and PR (setup, commit, commit/PR)
        |-- scaffold-project\SKILL.md Create the project skeleton
        |-- implement-feature\SKILL.md Implement one TODOS task
        |-- iterative-feature\SKILL.md Add or change a feature
        |-- refactor\SKILL.md         Reduce duplication and tech debt
        |-- journal-keeper\SKILL.md   Update the journal after a phase
        |-- remember\SKILL.md         Capture a fact or rule
        |-- operator-qa\SKILL.md      Journaled Q&A (AskQuestion and chat)
        |-- integrate-docs\SKILL.md   Fold docs into facts, rules, and MyRole.txt
        |-- promote-facts-rules\SKILL.md Elevate Work Item learnings
        |-- memory-optimize\SKILL.md  Check expert-memory health
        `-- visual-page\SKILL.md      Shared visual page beside chat
```


## Operator Q&A

Use **operator-qa** when clarifying requirements, building a spec with the user, verifying assumptions before work, or verifying notes before remember. Sessions live under `qa-sessions/`, keep a journal of questions and answers, and close into `conclusions.md`. Prefer AskQuestion for fixed choices; use chat for open-ended answers. The agent may start a session on its own when a human answer would change the plan.


A new Work Item starts from two templates. `work-items\_TEMPLATE\` gives the artifact folder (status, task list, and facts). `journals\work-items\_TEMPLATE\` gives the journal. Design docs, diagrams, and tests are added as the pipeline runs.

```
journals\work-items\<WID>\
├── progress.md                            # Item-wide fields and inherited decisions
├── state.json                             # Branch map (active path and history)
└── nodes\<node>.md                        # Step notes, open questions, next action

work-items\<WID>\
├── STATUS.md                              # Last session summary, artifacts, links

├── TODOS.md
├── spec.md                                # Optional; or a path you provide
├── facts\
│   ├── facts.md                           # Work Item facts
│   └── rules.md                           # Work Item rules
├── docs\
│   ├── design\                            # requirements-summary.md, hld.md, dd.md
│   ├── diagrams\                          # *.mmd and index.html
│   └── features\<feature-id>\             # Iterative feature spec, design, approval
└── tests\                                 # When this Work Item owns its tests
```

Active context is `.cursor\active-context.txt`, formatted `work-item:WID-…`. This is the only pointer file the skills write. `.cursor\active-work-item.txt` is a legacy file that is read as a fallback only.

## Getting Started

### 1. Start or resume

Open this folder and say **"start"**, **"continue"**, or **"resume"**.

The continue skill will:

1. Read `MyRole.txt`. If `Role status` is `pending`, run **define-role** and stop. It asks for the specific job, which workflows and skills apply, and any notes you already have (standards, architecture notes, runbooks, setup notes). "I have no notes" is a real answer. "Continue" does not answer those questions.
2. After "I approve the role" or "Skip role definition", read `.cursor\active-context.txt` (or, as a fallback, the legacy `.cursor\active-work-item.txt`).
3. If nothing is active, ask for a Work Item ID such as `WID-21411151`.
4. Create `work-items\<WID>\` from `work-items\_TEMPLATE\` and `journals\work-items\<WID>\` from `journals\work-items\_TEMPLATE\` when those folders do not exist.
5. If the journal has no workflow type, run **workflow-selector**. It reads `MyRole.txt` and offers only workflows still listed in `workflow-registry.json`.
6. Perform the single next action recorded in the active node note under `journals\work-items\<WID>\nodes\`.

To change Work Items later, say **"switch to work item WID-…"**.

### 2. The developer pipeline

From `.cursor\workflows\developer.md`:

`spec-parser → hld-writer → dd-writer → diagram-generator → task-breakdown → git-workflow (setup) → scaffold-project → implement-feature (loop) → test → git-workflow (commit/PR) → done`

**Iterative feature** (say "add a new feature" or "change an existing feature"): requirements → design → approval → branch → implement → test → commit/PR.

Every phase has its own skill folder: **spec-parser**, **hld-writer**, **dd-writer**, **diagram-generator**, **task-breakdown**, **git-workflow**, **scaffold-project**, and **implement-feature**. `.cursor\workflows\developer.md` holds the sequence and the gates.

### 3. Human gates

The pipeline pauses until you approve:

- **HLD and its diagrams** — "I approve the HLD" or "Skip HLD approval"
- **DD and its diagrams** — "I approve the DD" or "Skip DD approval"
- **Feature design** (iterative work) — "I approve the feature design" or an explicit waiver

"Continue" is not approval and not an answer to an open question. If the next action is a wait, continue only re-prompts.

### 4. What you can say

| What you say | What happens |
| --- | --- |
| "start" / "continue" / "resume" | Define the role if it is pending; otherwise read the journal and perform the next step |
| "define my role" | Run role onboarding, including any notes you already have |
| "I approve the role" | Save the role, workflows, and skills and allow Work Items |
| "switch to work item WID-…" | Point later steps at that Work Item |
| "I approve the HLD" | Clear the HLD gate and move to DD |
| "I approve the DD" | Clear the DD gate and move toward scaffold and implementation |
| "Skip HLD approval" | Waive that gate |
| "remember this …" | Store a fact or rule on the Work Item, or in Expert Role memory |
| "integrate this …" | Fold a document into facts, rules, and `MyRole.txt` |
| "promote facts/rules" | Review Work Item learnings for Expert Role memory |
| "add a new feature" | Start the iterative-feature workflow |
| "refactor" | Reduce tech debt and keep tests passing |

"Remember this" does not write `docs\facts\captured.md`. Work Item captures go to `work-items\<WID>\facts\`. Expert Role captures go to the workflow memory files under `facts\`, with a pointer in `facts\MEMORY-INDEX.md` when the topic is new.

### 5. Journal

The journal lives under `journals\work-items\<WID>\`. Each field has one home:

- `progress.md`: workflow type, spec file, mode, repo and branch, HLD profile, inherited decisions, completion status
- `nodes\<node>.md`: last completed, next action, open questions (blocking and deferred), Q&A resolved in the step, blockers, step notes
- `state.json`: the branch map. The current phase is the phase node on its `active` path
- `work-items\<WID>\STATUS.md`: last session summary, artifact list, links

### 6. Templates and HLD depth

Before HLD or DD, the system asks whether you have a template to follow.

The HLD uses the **Standard** profile (context and architecture).

### 7. What the pipeline produces

- Mermaid diagrams (architecture, sequence, ER, C4-style) and `docs\diagrams\index.html`
- Design docs under `work-items\<WID>\docs\design\`
- `TODOS.md`, including environment setup before package installs
- Unit and integration tests
- A feature branch `feature\WID-<id>` and, when you ask, a commit and pull request

Tests must pass before a push.

### 8. Safety

The system will:

- Ask blocking questions before moving past spec
- Ask about dependencies, downloads, and credentials instead of skipping them
- Refactor when a change would duplicate logic
- Run tests before push
- Install the environment the design calls for, before libraries

The system will not:

- Skip a phase the journal still has open
- Treat "continue" as approval
- Push while tests are failing
- Assume a workaround for a blocker

## Example

```
You: start
Agent: What are you working on? (work item WID-XXXXXXXX)
You: WID-21411151
Agent: [creates work-items\WID-21411151\ from the template]
       [asks you to select the developer pipeline]
       [reads work-items\WID-21411151\spec.md, or asks where the spec is]

       I have 3 blocking questions:
       1. What database should we use?
       2. Do you need authentication?
       3. Should this support multiple tenants?
You: 1. PostgreSQL, 2. Yes - OAuth2, 3. No, single tenant
Agent: [records the answers in Resolved Q&A]
       [sets next action to "run hld-writer"]

       Do you have an HLD template I should follow?
You: No, use Standard profile
Agent: [writes work-items\WID-21411151\docs\design\hld.md]
       [writes diagrams and updates docs\diagrams\index.html]
       [sets next action to "wait for HLD approval"]

       HLD is ready. Reply "I approve the HLD" to proceed.
You: I approve the HLD
Agent: [records approval and sets next action to "run dd-writer"]
```

## Troubleshooting

- **Continue is not advancing.** Read **Next action** in the active node note under `journals\work-items\<WID>\nodes\`. A wait for approval or an open blocking question needs a real answer, not another "continue".
- **A dependency or download failed.** The agent will stop and ask for a URL, credential, or other help. Answer before it proceeds.
- **You want a different next step.** Edit **Next action** in the active node note (`journals\work-items\<WID>\nodes\<active leaf>.md`), then say "continue".

## Learn more

- `AGENTS.md` — workflow rules
- `.cursor\CONTEXT-SYSTEM.md` — how the active Work Item is stored
- `.cursor\workflows\developer.md` — phase sequence, gates, and artifact paths
- `facts\MEMORY-INDEX.md` — how expert memory is organized
- `docs\spec-to-artifacts-agent-skills-system.md` — longer description of the system
