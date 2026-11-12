# Memory System Index

Quick navigation for this **Wholesale / inventory role** Expert. Load only what the current job needs.

---

## Two axes

1. **Workflow axis** (this file) — which memory files to load for an inventory job.
2. **Trigger axis** ([TRIGGER-INDEX.md](TRIGGER-INDEX.md)) — action-time surfacing. The PreToolUse hook `.claude/hooks/inject_rules_on_action.py` reads `trigger-index.json`. Most inventory rules use `Triggers: none` (judgment / ask). Regenerate with `python scripts/memory/build_trigger_index.py` after adding or retagging a rule.

---

## This role’s memory

**Role title:** Wholesale / inventory role  
**Seed id:** `wholesale-inventory`

Always load the **shared** pair, then the **operations** pair:

- [facts-shared.md](facts-shared.md) / [rules-shared.md](rules-shared.md) — `Workflows: all` entries
- [facts-operations.md](facts-operations.md) — SKU/master, on-hand, receiving, putaway, counts, lots, reorder, RMA, transfers, starter shop notes
- [rules-operations.md](rules-operations.md) — never invent qty/SKU/PO/lot, no silent adjust, blind means blind, one Work Item one folder, no customs, no money

**When to load:** every Work Item for this role.

**Typical jobs:** see `.claude/workflows/` and `docs/role/work-item-method.md`.

There is no software-developer or incident-response memory on this Expert.

### Work Item memory

- `work-items/<id>/facts/facts.md`
- `work-items/<id>/facts/rules.md`

Job-specific (this receipt’s extras, this count date’s variance notes). Promote into shared or operations when the operator agrees.

---

## Entry format

### Fact

```markdown
### YYYY-MM-DD: Descriptive Title
**Scope:** expert-role
**Workflows:** all | receiving-match | cycle-count | …
**Captured:** YYYY-MM-DD
**Source:** <where this came from>
**Status:** active

Descriptive content...
```

### Rule

```markdown
### YYYY-MM-DD: Prescriptive Title
**Scope:** expert-role
**Workflows:** all | receiving-match | …
**Triggers:** write:csv | write:pack | write:doc | none
**Captured:** YYYY-MM-DD
**Source:** <where this came from>
**Status:** active

**Rule:** what MUST be done
```

---

## Usage

1. Always load this index first.
2. Load `facts-shared.md` + `rules-shared.md`, then `facts-operations.md` + `rules-operations.md`.
3. Load the active Work Item facts/rules if present.
4. Follow the selected workflow file under `.claude/workflows/`.

**Maintenance:** when adding a new topic, add a pointer here if operators would not find it from the headings alone. Run the memory-optimize analyze script when files grow quickly.
