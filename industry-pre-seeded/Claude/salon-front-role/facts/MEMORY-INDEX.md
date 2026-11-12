# Memory System Index

Quick navigation for this **Salon / spa front role** expert. Load operations memory for role work. Do not load developer or incident-response files for this role — they are not the live memory.

---

## Two axes: Workflow (browsing) and Triggers (action)

1. **Workflow axis** (this file) — which operations entries apply to the current registered role job (`**Workflows:** all` or a registry id).

2. **Trigger axis** ([TRIGGER-INDEX.md](TRIGGER-INDEX.md)) — action-time surfacing. The PreToolUse hook `.claude/hooks/inject_rules_on_action.py` reads `trigger-index.json`. Most salon-role rules use `Triggers: none` (judgment / ask). Regenerate with `python scripts/memory/build_trigger_index.py` after retagging a rule.

---

## Quick navigation

### Operations (this role)

**When to use:** Any salon-role Work Item (day’s book, reminders, waitlist gaps, menu vs book, no-shows, closeout, gift cards, retail count, booth split).

**Load these files:**

- [facts-operations.md](facts-operations.md) — book, menu, retail vs backbar, POS close, booth vs employee, waitlist, gift cards, starter shop notes
- [rules-operations.md](rules-operations.md) — never invent fees/prices/cash, never blast, never medspa advice, hours file wins, one Work Item one folder, booth vs employee ask

**Typical jobs:** see `.claude/workflows/workflow-registry.json` and `docs/role/work-item-method.md`.

---

## Entry format reference

### Fact

```markdown
### YYYY-MM-DD: Descriptive Title
**Scope:** expert-role
**Workflows:** all | days-book | closeout | ...
**Captured:** YYYY-MM-DD
**Source:** <where this came from>
**Status:** active

Descriptive content...
```

### Rule

```markdown
### YYYY-MM-DD: Prescriptive Action Title
**Scope:** expert-role
**Workflows:** all | days-book | closeout | ...
**Triggers:** none | write:doc | write:csv
**Captured:** YYYY-MM-DD
**Source:** <where this came from>
**Status:** active

**Rule:** Clear statement of what MUST be done
```

---

## Usage

1. Always load this index first.
2. Load `facts-operations.md` + `rules-operations.md`.
3. Load the active Work Item `facts/` and `rules/` if present.
4. Filter Expert Role entries to `all` or the current registry id.

**Maintenance:** New shop knowledge goes in the operations pair. If a new high-value scenario appears (5+ similar questions), add a line here.

---

## Pre-seeded role

**Role title:** Salon / spa front role

**Seed id:** `salon-front-role`

Day-to-day role memory is the **operations** pair above. Starter entries are typical US salon-role practice until the operator corrects them.
