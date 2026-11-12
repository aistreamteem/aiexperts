# Memory System Index

Quick navigation for the real-estate transaction-coordinator role. Load the operations pair; do not look for developer or incident memory files on this seed.

---

## Two Axes: Workflow (browsing) and Triggers (action)

Rules are indexed on **two orthogonal axes**:

1. **Workflow axis** (this file) — *human browsing + context-budget loading*. This role loads `facts-operations.md` / `rules-operations.md` for every registered TC job.

2. **Trigger axis** ([TRIGGER-INDEX.md](TRIGGER-INDEX.md)) — *action-time surfacing*. A rule may carry `**Triggers:**` such as `write:doc`, `write:checklist`, or `none`. The PreToolUse hook `.claude/hooks/inject_rules_on_action.py` reads `trigger-index.json`.

`TRIGGER-INDEX.md` and `trigger-index.json` are **generated** by `python scripts/memory/build_trigger_index.py` — never hand-edit them; regenerate after adding or retagging a rule.

---

## Pre-seeded role

**Role title:** Real estate transaction coordinator

**Seed id:** `real-estate-transaction-coordinator`

**Work Item method:** `docs/role/work-item-method.md`

Day-to-day role memory lives in the **operations** pair:

- [facts-operations.md](facts-operations.md) — contract file, dates, option, disclosures, HOA, inspection/repair, title as routing, closing as completeness, wire-fraud process, and related starter notes
- [rules-operations.md](rules-operations.md) — dates from executed file, never invent deadlines, never hold earnest, never send wires, completeness only, label guesses

### Operations (this role)

**When to use:** Any registered workflow (`dates-calendar`, `missing-docs`, `disclosure-completeness`, `option-period-pack`, `inspection-to-repair-amendment-log`, `amendment-log-pack`, `hoa-packet-completeness`, `closing-checklist`, `wire-fraud-checklist-as-their-process`).

**Load these files:**

- [facts-operations.md](facts-operations.md)
- [rules-operations.md](rules-operations.md)

**Typical context:** operations pair only. This seed does not keep a separate software-build or incident-response memory pair.

---

## Entry Format Reference

### Fact Entry Template

```markdown
### YYYY-MM-DD: Descriptive Title

**Scope:** expert-role

**Workflows:** all | dates-calendar | missing-docs | ...

**Captured:** YYYY-MM-DD

**Source:** <where this came from>

Descriptive content...
```

### Rule Entry Template

```markdown
### YYYY-MM-DD: Prescriptive Action Title

**Scope:** expert-role

**Workflows:** all | dates-calendar | missing-docs | ...

**Triggers:** write:doc | write:checklist | none

**Captured:** YYYY-MM-DD

**Source:** <where this came from>

**Rule:** Clear statement of what MUST be done
```

---

### Usage Tips

**For a transaction Work Item:**

1. Load MEMORY-INDEX.md
2. Load facts-operations.md + rules-operations.md
3. Load `work-items/<id>/facts/` when present
4. Follow the selected `.claude/workflows/<job>.md`

**Maintenance:** When adding facts/rules, append to the operations files and update this index only if a new topic cluster appears. For health metrics see [HOW-MEMORY-LOADING-WORKS.md](HOW-MEMORY-LOADING-WORKS.md).
