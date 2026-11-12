# Memory System Index

Quick navigation for this **Event venue coordinator** expert. Load shared memory for role work. Do not load developer or incident-response files for this role — they are not the live memory.

---

## Two axes: Workflow (browsing) and Triggers (action)

1. **Workflow axis** (this file) — which shared entries apply to the current registered role job (`**Workflows:** all` or a registry id).

2. **Trigger axis** ([TRIGGER-INDEX.md](TRIGGER-INDEX.md)) — action-time surfacing. The PreToolUse hook `.claude/hooks/inject_rules_on_action.py` reads `trigger-index.json`. Most venue rules use `Triggers: none` (judgment / ask). Regenerate with `python scripts/memory/build_trigger_index.py` after retagging a rule.

---

## Quick navigation

### Shared (this role)

**When to use:** Any event-venue-coordinator Work Item (BEO pack, holds vs definite, COI missing, banquet check, load-in, and the other registered jobs).

**Load these files:**

- [facts-shared.md](facts-shared.md) — BEO, hold, definite, guarantee, COI, diagram, load-in, banquet check, group rooms, starter shop notes
- [rules-shared.md](rules-shared.md) — never invent rates/minimums, no liquor license, no fire stamp, no PAN, ask missing COI, counts from guarantee, one Work Item one folder, label guesses

**Typical jobs:** see `.claude/workflows/workflow-registry.json` and `docs/role/work-item-method.md`.

---

## Entry format reference

### Fact

```markdown
### YYYY-MM-DD: Descriptive Title
**Scope:** expert-role
**Workflows:** all | beo-pack | banquet-check-file | ...
**Captured:** YYYY-MM-DD
**Source:** <where this came from>
**Status:** active

Descriptive content...
```

### Rule

```markdown
### YYYY-MM-DD: Prescriptive Action Title
**Scope:** expert-role
**Workflows:** all | beo-pack | banquet-check-file | ...
**Triggers:** none | write:doc | write:csv
**Captured:** YYYY-MM-DD
**Source:** <where this came from>
**Status:** active

**Rule:** Clear statement of what MUST be done
```

---

## Usage

1. Always load this index first.
2. Load `facts-shared.md` + `rules-shared.md`.
3. Load the active Work Item `facts/` and `rules/` if present.
4. Filter Expert Role entries to `all` or the current registry id.

**Maintenance:** New shop knowledge goes in the shared pair. If a new high-value scenario appears (5+ similar questions), add a line here.

---

## Pre-seeded role

**Role title:** Event venue coordinator

**Seed id:** `event-venue-coordinator`

Day-to-day role memory is the **shared** pair above. Starter entries are typical US banquet / venue-coordinator practice until the operator corrects them.
