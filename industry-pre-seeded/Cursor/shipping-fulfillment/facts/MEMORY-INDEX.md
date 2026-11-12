# Memory System Index

Quick navigation for this **Shipping / fulfillment role** expert. Load shared + operations memory for role work. Do not load developer or incident-response files for this role — they are not used here.

---

## Two axes: Workflow (browsing) and Triggers (action)

1. **Workflow axis** (this file) — which entries apply to the current registered role job (`**Workflows:** all` or a registry id).

2. **Trigger axis** ([TRIGGER-INDEX.md](TRIGGER-INDEX.md)) — action-time surfacing. The PreToolUse hook `.cursor/hooks/inject_rules_on_action.py` reads `trigger-index.json`. Most shipping rules use `Triggers: none` (judgment / ask). Regenerate with `python scripts/memory/build_trigger_index.py` after retagging a rule.

---

## Quick navigation

### Shared (always)

**When to use:** Every shipping Work Item.

**Load these files:**

- [facts-shared.md](facts-shared.md) — cross-job shop facts (`Workflows: all`)
- [rules-shared.md](rules-shared.md) — cross-job shop rules (`Workflows: all`)

### Operations (registered jobs)

**When to use:** Any shipping / fulfillment Work Item (pick wave, pack exceptions, BOL pack, DIM vs scale, holds, shorts, EOD manifest, tracking exceptions, RMA, and the other registered jobs).

**Load these files:**

- [facts-operations.md](facts-operations.md) — pick, pack, carton, BOL, scale, DIM, NMFC, holds, shorts, manifest, tracking, RMA, starter shop notes
- [rules-operations.md](rules-operations.md) — never invent weight/class/DIM, no freight pay, no hazmat stamp, shorts stay visible, one Work Item one folder, label guesses

**Typical jobs:** see `.cursor/workflows/workflow-registry.json` and `docs/role/work-item-method.md`.

---

## Entry format reference

### Fact

```markdown
### YYYY-MM-DD: Descriptive Title
**Scope:** expert-role
**Workflows:** all | bol-pack | pick-wave | ...
**Captured:** YYYY-MM-DD
**Source:** <where this came from>
**Status:** active

Descriptive content...
```

### Rule

```markdown
### YYYY-MM-DD: Prescriptive Action Title
**Scope:** expert-role
**Workflows:** all | bol-pack | pick-wave | ...
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
3. Load `facts-operations.md` + `rules-operations.md`.
4. Load the active Work Item `facts/` and `rules/` if present.
5. Filter operations entries to `all` or the current registry id.

**Maintenance:** New cross-job knowledge goes in the shared pair. Job-tagged knowledge goes in the operations pair. If a new high-value scenario appears (5+ similar questions), add a line here.

---

## Pre-seeded role

**Role title:** Shipping / fulfillment role

**Seed id:** `shipping-fulfillment`

Day-to-day role memory is the **shared + operations** pairs above. Starter entries are typical US ship-from role practice until the operator corrects them.
