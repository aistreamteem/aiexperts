# Memory System Index

Quick navigation for the restaurant kitchen / BOH admin memory. Load only what this job needs.

---

## Two axes: browsing and triggers

1. **Workflow axis** (this file) — which operations file to load. This role has **one live pair**: `facts-operations.md` + `rules-operations.md`. Registered jobs (prep, count-walk-in, and the rest) all load that pair; entries may still tag `**Workflows:**` with a job id.

2. **Trigger axis** ([TRIGGER-INDEX.md](TRIGGER-INDEX.md)) — action-time surfacing. The PreToolUse hook `.cursor/hooks/inject_rules_on_action.py` reads `trigger-index.json`. Most starter rules are tagged `none` (judgment / ask rather than invent). Regenerate with `python scripts/memory/build_trigger_index.py` after adding or retagging a rule. Vocabulary: `write:sheet`, `write:pack`, `file:intake`, or `none`.

---

## Pre-seeded role

**Role title:** Restaurant kitchen / BOH admin

**Seed id:** `restaurant-kitchen-admin`

**Work-item method:** `docs/role/work-item-method.md`

Day-to-day memory:

- [facts-operations.md](facts-operations.md) — prep, par, walk-in count, 86, order guide, receiving, invoice, catering, allergen file, waste
- [rules-operations.md](rules-operations.md) — never invent on-hand/par/allergen/holding time; shorts and 86s stay visible; no inspector/pay/PAN

### Operations (this role)

**When to use:** Any Work Item for this role (prep, count, order guide, receiving, invoice, 86, par review, waste, catering, allergen quote).

**Load these files:**

- [facts-operations.md](facts-operations.md)
- [rules-operations.md](rules-operations.md)

**Typical context:** the operations pair plus the active Work Item `facts/` files.

Do not load software-design or incident-bridge memory. Those are not this role.

---

## Quick navigation by job

| Job | Also look at |
| --- | --- |
| Prep | Prep list, prep math, shift, 86 on top, recipe yield |
| Count walk-in | Count, walk-in map, freezer, lowboy, open vs close |
| Order guide | Par, vendor, delivery day, one-day order, split case |
| Receiving | Receiving notes, catch-weight, produce spec, credit memo |
| Invoice match | Food invoices, invoice vs order, vendor credit |
| Eighty-six | 86, 86 board vs POS, 86 first |
| Par review | Par, menu mix, waste, covers forecast, weekend par |
| Waste week | Waste log, waste reasons, donation file |
| Catering pull | Catering pull, special order, recipe yield |
| Allergen quote | Allergen file, quote the matrix, sesame from file |

---

## Entry format

### Fact

```markdown
### YYYY-MM-DD: Descriptive Title
**Scope:** expert-role
**Workflows:** all | prep | count-walk-in | ...
**Captured:** YYYY-MM-DD
**Source:** <where this came from>
**Status:** active

Descriptive content...
```

### Rule

```markdown
### YYYY-MM-DD: Prescriptive Title
**Scope:** expert-role
**Workflows:** all | prep | ...
**Triggers:** none | write:sheet | write:pack | file:intake
**Captured:** YYYY-MM-DD
**Source:** <where this came from>
**Status:** active

**Rule:** Clear statement of what MUST be done
```

Promote Work Item entries into this operations pair (`promote-facts-rules`). Tools stay under `docs/tools/`.
