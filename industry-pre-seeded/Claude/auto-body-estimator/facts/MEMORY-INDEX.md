# Memory System Index

Quick navigation for this Auto body estimator / office Expert. Load shared memory plus the active Work Item facts/rules — not a developer or incident pair.

---

## Two Axes: Workflow (browsing) and Triggers (action)

Rules are indexed on **two orthogonal axes**:

1. **Workflow axis** (this file) — human browsing + context-budget loading. This role’s live pair is `facts-shared.md` / `rules-shared.md`. Registered jobs are listed in `.claude/workflows/workflow-registry.json`.

2. **Trigger axis** ([TRIGGER-INDEX.md](TRIGGER-INDEX.md)) — action-time surfacing. Every rule may carry a `**Triggers:**` field. The PreToolUse hook `.claude/hooks/inject_rules_on_action.py` reads `trigger-index.json`. Most shop rules here are judgment rules (`Triggers: none`) until the operator tags an action.

`TRIGGER-INDEX.md` and `trigger-index.json` are **generated** by `python scripts/memory/build_trigger_index.py` — never hand-edit them; regenerate after adding or retagging a rule.

---

## Quick Navigation by Role

**Role title:** Auto body estimator / office  
**Seed id:** `auto-body-estimator`

### Shared (this role)

**When to use:** Assignment, claim, photo index, estimate pack, OEM procedure completeness, authorization, supplement, parts vs estimate, pay-type split, cycle time.

**Load these files:**

- [facts-shared.md](facts-shared.md) — shop vocabulary and typical US collision practice (starter until they confirm)
- [rules-shared.md](rules-shared.md) — must-never and how-to-act rules (hours from matrix, no invented prices, no total-loss verdict, one Work Item per folder, …)

**Work Item extras (when a claim is active):**

- `work-items/<id>/facts/facts.md`
- `work-items/<id>/facts/rules.md`

**Method:** [docs/role/work-item-method.md](../docs/role/work-item-method.md)

### Registered jobs → when to load extra context

| Job | Load extra if the step needs |
| --- | --- |
| `assignment-intake` | assignment, VIN, DOL, insurer, mileage facts |
| `photo-index` | photo-set, photo-naming, prior-damage |
| `estimate-from-files` | labor-matrix, parts-file, estimate, repair-vs-replace |
| `oem-procedure-present` | procedure-pages, ADAS/weld as their op |
| `authorization-missing` | authorization, teardown-auth |
| `supplement-log` | supplement, supplement-days |
| `parts-order-vs-estimate` | parts-order, backorder |
| `customer-pay-vs-insurer` | customer-pay, deductible, betterment |
| `cycle-time-list` | cycle-time-from-file, rental-if-any |

This role does not load a separate coding or incident-response memory pair.

---

## Entry Format Reference

### Fact Entry Template

```markdown
### YYYY-MM-DD: Descriptive Title
**Scope:** expert-role
**Workflows:** all
**Captured:** YYYY-MM-DD
**Source:** <where this came from>
**Status:** active

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
**Status:** active

**Rule:** Clear statement of what MUST be done
```

Role-appropriate trigger tokens (if tagged later): `write:doc`, `write:csv`, `write:estimate`, `write:photo-index`, `write:supplement`, plus generic `write:sql`, `sql:generate`, `pr:open`, `git:push`, `git:commit` when relevant. Do not use `config:change`. Use `none` for judgment-only rules.

---

### Usage Tips

1. Always load this index first.
2. Then load the shared pair.
3. Then load the active Work Item facts/rules.
4. Follow `docs/role/work-item-method.md` for which registered job matches the ask.

**Maintenance Note:** New Expert Role facts/rules go in the shared files. If a new topic appears, add a pointer here. For health metrics see [HOW-MEMORY-LOADING-WORKS.md](HOW-MEMORY-LOADING-WORKS.md).
