# Memory System Index

Quick navigation guide for the AI expert role memory system. Load only the workflow-specific files you need, plus the shared pair, to reduce context load.

---

## Two Axes: Workflow (browsing) and Triggers (action)

Rules are indexed on **two orthogonal axes**:

1. **Workflow axis** (this file, below) — *human browsing + context-budget loading*. You load `rules-<workflow>.md` by session type, plus `rules-shared.md` every time. Good for reading; but a rule filed under one workflow is invisible when a *different* workflow file is loaded (rules that apply everywhere belong in the shared pair).
2. **Trigger axis** ([TRIGGER-INDEX.md](TRIGGER-INDEX.md)) — *action-time surfacing, workflow-independent*. Every rule carries a `**Triggers:**` field naming the tool-action(s) that should surface it (`write:sql`, `pr:open`, ...). The preToolUse hook `.cursor/hooks/inject_rules_on_action.py` reads the generated `trigger-index.json` and injects the matching rule text at the moment of the action – in **any** workflow.

`TRIGGER-INDEX.md` and `trigger-index.json` are **generated** by `python scripts/memory/build_trigger_index.py` – never hand-edit them; regenerate after adding or retagging a rule (the `remember`/`promote-facts-rules`/`integrate-docs` skills prompt for this).

---

## Quick Navigation by Workflow

### Shared (always loaded)

**When to use**: Every session, in every workflow. Entries marked `Workflows: all` live here.

**Load these files**:

- [facts-shared.md](facts-shared.md) – Environments, team contacts, tool locations, and other context that applies to every workflow
- [rules-shared.md](rules-shared.md) – Communication protocols, safety checks, and standards that apply to every workflow

---

### Production Incident Response

**When to use**: Production incidents, urgent bugs, hotfixes

**Load these files** (created together with the incident-response workflow; they do not exist until that workflow is enabled):

- `facts-incident-response.md` – Incident context, monitoring locations, common failure modes
- `rules-incident-response.md` – Mitigation procedures, safety checks, communication protocols

---

### Developer

(Greenfield/Iterative Features)

**When to use**: New feature development, code changes, testing, local debugging

**Load these files**:

- [facts-developer.md](facts-developer.md) – Architecture, local setup, codebase structure, testing notes
- [rules-developer.md](rules-developer.md) – Code standards, deployment rules, testing patterns, git workflow

---

## Entry Format Reference

Every entry header is `### YYYY-MM-DD: Title`.

### Fact Entry Template

```markdown
### YYYY-MM-DD: Descriptive Title
**Scope:** expert-role
**Workflows:** developer | production-incident | all
**Captured:** YYYY-MM-DD
**Source:** <where this came from>

Descriptive content about what this is, how it works, what it means...
```

### Rule Entry Template

```markdown
### YYYY-MM-DD: Prescriptive Action Title
**Scope:** expert-role
**Workflows:** developer | production-incident | all
**Triggers:** write:sql | write:doc | pr:open | git:push | git:commit | sql:generate | none
**Captured:** YYYY-MM-DD
**Source:** <where this came from>

**Rule:** Clear statement of what MUST be done

**Why:** Rationale and context for why this rule exists

**How to apply:**
1. Step-by-step procedure
2. With specific commands/queries where applicable
3. Including what to check/verify
```

---

### Usage Tips

**For development work**:

1. Load `facts-shared.md` + `rules-shared.md` (always)
2. Load `facts-developer.md` + `rules-developer.md`
3. Pull in reference files as needed

**Cross-workflow needs**:

- Load multiple workflow files as needed (incident + developer, etc.)
- `facts-shared.md` and `rules-shared.md` contain knowledge that applies across all workflows

---

**Maintenance Note**: When adding new facts/rules, classify by primary workflow and add to the appropriate file. Anything that applies to every workflow (`Workflows: all`) goes in the shared pair. For how loading works, see [HOW-MEMORY-LOADING-WORKS.md](HOW-MEMORY-LOADING-WORKS.md).
