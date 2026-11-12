# Memory System Index

Quick navigation for this **Office and operations** expert. Load operations memory for role work. Do not load developer or incident-response files for this role — they are not the live memory.

---

## Two axes: Workflow (browsing) and Triggers (action)

1. **Workflow axis** (this file) — which operations entries apply to the current registered role job (`**Workflows:** all` or a registry id).

2. **Trigger axis** ([TRIGGER-INDEX.md](TRIGGER-INDEX.md)) — action-time surfacing. The PreToolUse hook `.claude/hooks/inject_rules_on_action.py` reads `trigger-index.json`. Most office-operations rules use `Triggers: none` (judgment / ask). Regenerate with `python scripts/memory/build_trigger_index.py` after retagging a rule.

---

## Quick navigation

### Operations (this role)

**When to use:** Any office-operations Work Item (weekly pack, meeting pack, mail log, supplies, visitor week, recurring checklist, license watch, key audit, vendor contacts, retention boxes).

**Load these files:**

- [facts-operations.md](facts-operations.md) — calendars, supplies, meetings, licenses, mail, visitors, keys, vendors, retention, starter shop notes
- [rules-operations.md](rules-operations.md) — never invent shop practice, no money movement, no HR/legal/payroll opinions, calendar from their file, one Work Item one folder

**Typical jobs:** see `.claude/workflows/workflow-registry.json` and `docs/role/work-item-method.md`.

---

## Entry format reference

### Fact

```markdown
### YYYY-MM-DD: Descriptive Title
**Scope:** expert-role
**Workflows:** all | weekly-pack | meeting-pack | ...
**Captured:** YYYY-MM-DD
**Source:** <where this came from>
**Status:** active

Descriptive content...
```

### Rule

```markdown
### YYYY-MM-DD: Prescriptive Action Title
**Scope:** expert-role
**Workflows:** all | weekly-pack | meeting-pack | ...
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

**Role title:** Office and operations

**Seed id:** `office-operations`

Day-to-day role memory is the **operations** pair above. Starter entries are typical US small-office practice until the operator corrects them.
