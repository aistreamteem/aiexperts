# Memory System Index

Quick navigation for this **Wholesale / inventory role** Expert. Load only what the current job needs.

---

## Two axes

1. **Workflow axis** (this file) — which memory files to load for an inventory job.
2. **Trigger axis** ([TRIGGER-INDEX.md](TRIGGER-INDEX.md)) — action-time surfacing. The PreToolUse hook `.cursor/hooks/inject_rules_on_action.py` reads `trigger-index.json`. Regenerate with `python scripts/memory/build_trigger_index.py` after adding or retagging a rule.

---

## This role’s memory

**Role title:** Wholesale / inventory role  
**Seed id:** `wholesale-inventory`

### Shared (always)

- [facts-shared.md](facts-shared.md) — cross-job shop facts (`Workflows: all`)
- [rules-shared.md](rules-shared.md) — cross-job shop rules (`Workflows: all`)

### Operations (registered jobs)

- [facts-operations.md](facts-operations.md) — SKU/master, on-hand, receiving, putaway, counts, lots, reorder, RMA, transfers, starter shop notes
- [rules-operations.md](rules-operations.md) — never invent qty/SKU/PO/lot, no silent adjust, blind means blind, one Work Item one folder, no customs, no money

**When to load:** every Work Item — shared first, then operations (filter by job or `all`).

**Typical jobs:** see `.cursor/workflows/` and `docs/role/work-item-method.md`.

There is no software-developer or incident-response memory on this Expert.

### Work Item memory

- `work-items/<id>/facts/facts.md`
- `work-items/<id>/facts/rules.md`

Job-specific (this receipt, this count date). Promote into shared or operations when the operator agrees.

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
2. Load `facts-shared.md` + `rules-shared.md`.
3. Load `facts-operations.md` + `rules-operations.md`.
4. Load the active Work Item facts/rules if present.
5. Follow the selected workflow file under `.cursor/workflows/`.

**Maintenance:** when adding a new topic, add a pointer here if operators would not find it from the headings alone. Run **memory-optimize** when files grow quickly.
