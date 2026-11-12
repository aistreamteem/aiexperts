# Memory System Index

Quick navigation for the Auto shop service advisor Expert. Load the shared pair, then the operations pair, unless a Work Item has its own facts/rules.

---

## Two Axes: Workflow (browsing) and Triggers (action)

Rules are indexed on **two orthogonal axes**:

1. **Workflow axis** (this file, below) — *human browsing + context-budget loading*. Always load **shared**, then **operations** for every RO pack.

2. **Trigger axis** ([TRIGGER-INDEX.md](TRIGGER-INDEX.md)) — *action-time surfacing*. Every rule carries a `**Triggers:**` field. Pre-seeded shop rules currently use `none` (judgment/background). The PreToolUse hook `.claude/hooks/inject_rules_on_action.py` reads `trigger-index.json` when a non-`none` trigger is added.

`TRIGGER-INDEX.md` and `trigger-index.json` are **generated** by `python scripts/memory/build_trigger_index.py` – never hand-edit them; regenerate after adding or retagging a rule.

---

## Pre-seeded role

**Role title:** Auto shop service advisor

**Seed id:** `auto-service-advisor`

Day-to-day role memory:

- [facts-shared.md](facts-shared.md) / [rules-shared.md](rules-shared.md) — cross-cutting entries (`Workflows: all`)
- [facts-operations.md](facts-operations.md) — RO, concern, three C's, MPI, estimate, auth, parts, comeback, pickup
- [rules-operations.md](rules-operations.md) — never invent diagnosis/VIN/book time; auth before sold; MPI from their form; invoice matches last auth

**When to use:** Any Work Item under `work-items/` for this role (write-up, board, MPI, estimate, auth gap, findings, parts, comeback, pickup).

Work Item memory (this RO only): `work-items/<id>/facts/facts.md` and `work-items/<id>/facts/rules.md`.

Registered jobs: see `.claude/workflows/workflow-registry.json` and `docs/role/work-item-method.md`.

Trigger vocabulary this hook can produce: `write:doc` (and `none` for background rules).

---

## Entry Format Reference

### Fact Entry Template

```markdown
### YYYY-MM-DD: Descriptive Title

**Scope:** expert-role

**Workflows:** all

**Captured:** YYYY-MM-DD

**Source:** <where this came from>

Descriptive content about what this is, how it works, what it means...
```

### Rule Entry Template

```markdown
### YYYY-MM-DD: Prescriptive Action Title

**Scope:** expert-role

**Workflows:** all

**Triggers:** none

**Captured:** YYYY-MM-DD

**Source:** <where this came from>

**Rule:** Clear statement of what MUST be done

**Why:** Rationale and context for why this rule exists

**How to apply:**

1. Step-by-step procedure
```

Use `**Workflows:** all` for shared files. Do not file new shop knowledge into developer or incident files.

---

### Usage Tips

1. Always load this index first, then shared, then operations.
2. Add Work Item facts only when they are true for this RO, not the whole shop.
3. After promoting learnings, keep pointers here if a new browse topic appears.

**Maintenance Note:** When adding facts/rules, append to shared or operations as above. For system health, see [HOW-MEMORY-LOADING-WORKS.md](HOW-MEMORY-LOADING-WORKS.md).
