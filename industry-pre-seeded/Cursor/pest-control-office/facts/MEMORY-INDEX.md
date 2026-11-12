# Memory System Index

Quick navigation for this **Pest control office** expert. Load operations memory for role work. Do not load developer or incident-response files for this role — they are not the live memory.

---

## Two axes: Workflow (browsing) and Triggers (action)

1. **Workflow axis** (this file) — which operations entries apply to the current registered role job (`**Workflows:** all` or a registry id).

2. **Trigger axis** ([TRIGGER-INDEX.md](TRIGGER-INDEX.md)) — action-time surfacing. The PreToolUse hook `.cursor/hooks/inject_rules_on_action.py` reads `trigger-index.json`. Most pest-office rules use `Triggers: none` (judgment / ask). Regenerate with `python scripts/memory/build_trigger_index.py` after retagging a rule.

---

## Quick navigation

### Operations (this role)

**When to use:** Any pest-control-office Work Item (route day, skip list, callbacks, chemical-log completeness, inventory vs log, bait maps, device counts, estimates, WDO packs).

**Load these files:**

- [facts-operations.md](facts-operations.md) — routes, tickets, chemical logs, bait maps, callbacks, skips, WDO forms, starter shop notes
- [rules-operations.md](rules-operations.md) — never invent mix/EPA, never diagnose, no gate codes, skip list wins, one Work Item one folder, label guesses

**Typical jobs:** see `.cursor/workflows/workflow-registry.json` and `docs/role/work-item-method.md`.

---

## Entry format reference

### Fact

```markdown
### YYYY-MM-DD: Descriptive Title
**Scope:** expert-role
**Workflows:** all | route-day | chemical-log-completeness | ...
**Captured:** YYYY-MM-DD
**Source:** <where this came from>
**Status:** active

Descriptive content...
```

### Rule

```markdown
### YYYY-MM-DD: Prescriptive Action Title
**Scope:** expert-role
**Workflows:** all | route-day | chemical-log-completeness | ...
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

**Role title:** Pest control office

**Seed id:** `pest-control-office`

Day-to-day role memory is the **operations** pair above. Starter entries are typical US pest-office practice until the operator corrects them.
