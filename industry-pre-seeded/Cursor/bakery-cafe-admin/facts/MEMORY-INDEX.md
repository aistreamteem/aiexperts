# Memory System Index

Quick navigation for the bakery / cafe production-office memory. Load only what this job needs.

---

## Two axes: browsing and triggers

1. **Workflow axis** (this file) — which files to load. This role loads **shared** then **operations**. Registered jobs (bake-list-day, wholesale-day, and the rest) all load both pairs; entries may still tag `**Workflows:**` with a job id.

2. **Trigger axis** ([TRIGGER-INDEX.md](TRIGGER-INDEX.md)) — action-time surfacing. The PreToolUse hook `.cursor/hooks/inject_rules_on_action.py` reads `trigger-index.json`. Most starter rules are tagged `none` (judgment / ask-don’t-invent). Regenerate with `python scripts/memory/build_trigger_index.py` after adding or retagging a rule.

---

## Pre-seeded role

**Role title:** Bakery / cafe production office

**Seed id:** `bakery-cafe-admin`

**Work-item method:** `docs/role/work-item-method.md`

Day-to-day memory:

- [facts-shared.md](facts-shared.md) / [rules-shared.md](rules-shared.md) — shop-wide (`Workflows: all`)
- [facts-operations.md](facts-operations.md) — bake list, case par, standing, cake tickets, receiving, allergen sheet, waste, formulas as their files
- [rules-operations.md](rules-operations.md) — never invent formula/qty/par/allergen; shorts and stales stay visible; no inspector/FDA/PAN/pay

### Shared (always)

**When to use:** Every Work Item.

**Load these files:**

- [facts-shared.md](facts-shared.md)
- [rules-shared.md](rules-shared.md)

### Operations (job memory)

**When to use:** Any bakery-cafe Work Item (bake list, case par, wholesale, cake board, holiday, receiving, ingredient par, waste, allergen index).

**Load these files:**

- [facts-operations.md](facts-operations.md)
- [rules-operations.md](rules-operations.md)

Do not load software-design or incident-bridge memory. Those are not this role.

---

## Quick navigation by job

| Job | Also look at |
| --- | --- |
| Bake list day | Bake list, mix count, formula from their file, yield, cafe vs wholesale, scale weights |
| Case par vs count | Case par, case count, pastry case, bread, 86-case |
| Wholesale day | Wholesale standing, wholesale day, standing-change, 86-wholesale, boxes, routes |
| Custom cake board | Cake order, custom cake, wedding cake, servings chart, flavor from menu |
| Holiday bake-up | Holiday, production calendar, preorder |
| Receiving shorts | Receiving, invoice PDF, vendor, credit (draft only) |
| Ingredient below par | Par ingredient, par min, flour, butter, dairy |
| Stale and waste | Waste, stales, donation (if they log it) |
| Allergen sheet index | Allergen from their sheet, nut, sesame, gluten as their process not a legal claim, labeling as their file |

---

## Entry format

### Fact

```markdown
### YYYY-MM-DD: Descriptive Title
**Scope:** expert-role
**Workflows:** all | bake-list-day | wholesale-day | ...
**Captured:** YYYY-MM-DD
**Source:** <where this came from>
**Status:** active

Descriptive content...
```

### Rule

```markdown
### YYYY-MM-DD: Prescriptive Title
**Scope:** expert-role
**Workflows:** all | bake-list-day | ...
**Triggers:** none | write:sheet | write:pack | file:intake
**Captured:** YYYY-MM-DD
**Source:** <where this came from>
**Status:** active

**Rule:** Clear statement of what MUST be done
```

Route `Workflows: all` into the shared pair; job-tagged entries into the operations pair (`promote-facts-rules` / `remember`). Tools stay under `docs/tools/`.
