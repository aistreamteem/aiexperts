# Memory System Index

Quick navigation for the Pest control office expert. Load only the operations files unless a Work Item has its own facts/rules.

---

## Two Axes: Workflow (browsing) and Triggers (action)

Rules are indexed on **two orthogonal axes**:

1. **Workflow axis** (this file, below) — *human browsing + context-budget loading*. This role loads the operations pair for every pest-office job.

2. **Trigger axis** ([TRIGGER-INDEX.md](TRIGGER-INDEX.md)) — *action-time surfacing*. Every rule carries a `**Triggers:**` field. The PreToolUse hook `.claude/hooks/inject_rules_on_action.py` reads `trigger-index.json` and injects matching rule text. Most pest-office rules use `none` (judgment / ask) until a write token is assigned.

`TRIGGER-INDEX.md` and `trigger-index.json` are **generated** by `python scripts/memory/build_trigger_index.py` – never hand-edit them; regenerate after adding or retagging a rule.

---

## Quick Navigation

### Pest control office (this role)

**When to use:** Route days, skip lists, callbacks, chemical-log completeness, inventory vs log, bait-map indexes, device counts, estimates from their price file, WDO/termite form packs.

**Load these files:**

- [facts-operations.md](facts-operations.md) – Account, ticket, route, skip, callback, chemical log, EPA-from-file, bait map, WDO form
- [rules-operations.md](rules-operations.md) – Ask-if-missing, never invent mix/EPA/rate, skip wins, no gate codes, label guesses

**Typical jobs:** see `.claude/workflows/` and `docs/role/work-item-method.md`

Do not load developer or production-incident memory files for this role. Those pairs are not this role’s live memory.

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
**Triggers:** write:doc | write:csv | write:pack | none
**Captured:** YYYY-MM-DD
**Source:** <where this came from>
**Status:** active

**Rule:** Clear statement of what MUST be done
```

---

### Usage Tips

**For a pest-office Work Item:**

1. Load this index
2. Load `facts-operations.md` + `rules-operations.md`
3. Load `work-items/<id>/facts/` if present
4. Open the selected `.claude/workflows/<job>.md`

**Maintenance:** When adding new facts/rules, append to the operations pair. If a new high-value topic appears, add a line here. For system health, see [HOW-MEMORY-LOADING-WORKS.md](HOW-MEMORY-LOADING-WORKS.md).

---

## Pre-seeded role

**Role title:** Pest control office

**Seed id:** `pest-control-office`

This expert’s day-to-day role memory lives in the **operations** pair:

- [facts-operations.md](facts-operations.md)
- [rules-operations.md](rules-operations.md)
