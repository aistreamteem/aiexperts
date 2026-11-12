# Memory System Index

Navigation guide for the expert role memory. Load only the files you need: the shared pair, plus the pair for the current workflow.

---

## Two Axes: Workflow (browsing) and Triggers (action)

Rules are indexed on **two orthogonal axes**:

1. **Workflow axis** (this file, below) — human browsing and context-budget loading. You load the shared pair and `rules-<workflow>.md` by session type. A rule filed under one workflow is invisible when a *different* workflow file is loaded, which is why cross-workflow rules go in the shared pair.

2. **Trigger axis** ([TRIGGER-INDEX.md](TRIGGER-INDEX.md)) — action-time surfacing, workflow-independent. Every rule carries a `**Triggers:**` field naming the tool-action(s) that should surface it (`write:sql`, `pr:open`, `git:push`, ...). The PreToolUse hook `.claude/hooks/inject_rules_on_action.py` reads the generated `trigger-index.json` and injects the matching rule text at the moment of the action, in **any** workflow.

`TRIGGER-INDEX.md` and `trigger-index.json` are **generated** by `python scripts/memory/build_trigger_index.py`. Never hand-edit them; regenerate after adding or retagging a rule (the `remember`, `promote-facts-rules`, and `integrate-docs` skills do this).

---

## Quick Navigation by Workflow

### Always load: Shared

**When to use**: every workflow, every session.

- [facts-shared.md](facts-shared.md) – context that applies to all workflows
- [rules-shared.md](rules-shared.md) – constraints that apply to all workflows

Entries here carry `**Workflows:** all`.

### Developer (Greenfield / Iterative Features)

**When to use**: new feature development, code changes, testing, local debugging.

- [facts-developer.md](facts-developer.md) – architecture, codebase structure, local dev setup, test tooling
- [rules-developer.md](rules-developer.md) – code standards, design patterns, testing requirements, git and deployment rules

### Production Incident Response

Not enabled by default. When the workflow is enabled, its pair is `facts-incident-response.md` and `rules-incident-response.md`, created at that time. See `.claude/workflows/production-incident.md`.

---

## Entry Format Reference

Use `### YYYY-MM-DD: Title` headers for every entry, in every facts and rules file.

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

The trigger vocabulary is the `KNOWN_TOKENS` table in `.claude/hooks/inject_rules_on_action.py`. A rule tagged with any other token is listed as unreachable in `TRIGGER-INDEX.md`.

---

## Usage Tips

**For development work**:
1. Load `facts-shared.md` + `rules-shared.md`
2. Load `facts-developer.md` + `rules-developer.md`

**Cross-workflow needs**:
- Load another workflow's files only when the task crosses into it.

---

**Maintenance Note**: When adding facts or rules, file them by their `**Workflows:**` value: `all` goes to the shared pair, a single workflow goes to that workflow's pair. For how the loading works, see [HOW-MEMORY-LOADING-WORKS.md](HOW-MEMORY-LOADING-WORKS.md).
