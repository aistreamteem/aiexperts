# Memory System Index

Quick navigation for the Fleet / delivery dispatcher expert. Load the shared pair, the operations pair, and this index.

---

## Two Axes: Workflow (browsing) and Triggers (action)

Rules are indexed on **two orthogonal axes**:

1. **Workflow axis** (this file) — *human browsing + context-budget loading*. This role always loads `facts-shared.md` / `rules-shared.md`, then `facts-operations.md` / `rules-operations.md`. Registered job ids (`assignment-pack`, `todays-routes`, and the rest) filter entries via `**Workflows:**`. Route `Workflows: all` to the shared pair.

2. **Trigger axis** ([TRIGGER-INDEX.md](TRIGGER-INDEX.md)) — *action-time surfacing*. Every rule may carry a `**Triggers:**` field (`write:doc`, `write:csv`, `none`). The PreToolUse hook `.cursor/hooks/inject_rules_on_action.py` reads `trigger-index.json` and injects matching rule text.

`TRIGGER-INDEX.md` and `trigger-index.json` are **generated** by `python scripts/memory/build_trigger_index.py` – never hand-edit them; regenerate after adding or retagging a rule.

---

## Quick Navigation

### Shared + Operations (this role)

**When to use:** Any Work Item for this fleet dispatcher — assignment, routes, DVIR, exceptions, breakdown, detention, POD, HOS questions, fuel outliers.

**Load these files:**

- [facts-shared.md](facts-shared.md) / [rules-shared.md](rules-shared.md) – cross-job shop knowledge (`Workflows: all`)
- [facts-operations.md](facts-operations.md) – roster, routes, DVIR, POD, ELD/GPS, fuel, exceptions, how we file packs
- [rules-operations.md](rules-operations.md) – do not invent GPS/ETA/POD/DVIR; ask when missing; one day / one unit / one folder; flag don’t accuse; secrets stay out

**Typical context load:** shared pair + operations pair.

Work Item facts/rules (not split): `work-items/<id>/facts/facts.md` and `.../rules.md`.

---

## Entry Format Reference

### Fact Entry Template

```markdown
### YYYY-MM-DD: Descriptive Title
**Scope:** expert-role
**Workflows:** all | assignment-pack | todays-routes | dvir-gap | exceptions | breakdown | detention | pod-check | hos-questions | fuel-outliers
**Captured:** YYYY-MM-DD
**Source:** <where this came from>

Descriptive content about what this is, how it works, what it means...
```

### Rule Entry Template

```markdown
### YYYY-MM-DD: Prescriptive Action Title
**Scope:** expert-role
**Workflows:** all | assignment-pack | todays-routes | dvir-gap | exceptions | breakdown | detention | pod-check | hos-questions | fuel-outliers
**Triggers:** write:doc | write:csv | none
**Captured:** YYYY-MM-DD
**Source:** <where this came from>

**Rule:** Clear statement of what MUST be done
```

---

### Usage Tips

**For a dispatch pack:**

1. Load `facts-shared.md` + `rules-shared.md`, then `facts-operations.md` + `rules-operations.md`
2. Load the active Work Item facts/rules
3. Open the registered workflow file under `.cursor/workflows/`

**Maintenance Note**: Route `Workflows: all` to the shared pair; role-job ids to the operations pair. For system health, see [HOW-MEMORY-LOADING-WORKS.md](HOW-MEMORY-LOADING-WORKS.md).

---

## Pre-seeded role

**Role title:** Fleet / delivery dispatcher

**Seed id:** `fleet-dispatcher`

This expert’s day-to-day role memory lives in the **shared** and **operations** pairs:

- [facts-shared.md](facts-shared.md) / [rules-shared.md](rules-shared.md)
- [facts-operations.md](facts-operations.md) / [rules-operations.md](rules-operations.md)

See also `docs/role/work-item-method.md` for phases and human gates.
