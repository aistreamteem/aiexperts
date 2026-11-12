# Memory System Index

Quick navigation for this **Purchasing / buyer** Expert. Load only what the current pack needs.

---

## Two Axes: Workflow (browsing) and Triggers (action)

1. **Workflow axis** (this file) — which memory files to load for this role.
2. **Trigger axis** ([TRIGGER-INDEX.md](TRIGGER-INDEX.md)) — action-time surfacing via `.claude/hooks/inject_rules_on_action.py` and `trigger-index.json`.

`TRIGGER-INDEX.md` and `trigger-index.json` are **generated** by `py -3 scripts/memory/build_trigger_index.py` — never hand-edit them; regenerate after adding or retagging a rule.

---

## Quick Navigation by Workflow

### Shared (always)

**When to use:** Every session. Entries marked `Workflows: all` live here.

- [facts-shared.md](facts-shared.md) — cross-job shop facts
- [rules-shared.md](rules-shared.md) — cross-job shop rules

### Operations (registered jobs)

**When to use:** Any purchasing pack (AVL, RFQ, quote/lead/MOQ, open POs, backorder, blanket, change order, receiving shorts, match).

- [facts-operations.md](facts-operations.md) — PO, AVL, quote, receiving, match, starter shop notes
- [rules-operations.md](rules-operations.md) — must-nevers, no pay, no AVL add, no price guess, one PO per folder

**Registered jobs** (instruction files under `.claude/workflows/`):

| Job | Load extra context from operations entries about |
| --- | --- |
| avl-check | approved vendor, AVL export, requisition vendor |
| rfq-from-files | requisition, item list, need-by, drawings |
| quote-lead-moq | quote PDF, MOQ, lead time, validity |
| open-pos | open PO, need-by, past due |
| backorder-list | backorder, acknowledgment, past need-by |
| blanket-release | blanket, NTE, release qty |
| change-order-pack | change order, original line, vendor note |
| receiving-shorts | receiving, short, partial |
| match | PO, receiving, invoice, three-way |

**Method:** [docs/role/work-item-method.md](../docs/role/work-item-method.md)

This role does not use developer or incident-response memory pairs.

### Work Item memory

- `work-items/<id>/facts/facts.md`
- `work-items/<id>/facts/rules.md`

Job-specific (this PO’s revision, this vendor’s late promise). Promote into shared or operations when the operator agrees.

---

## Entry Format Reference

### Fact Entry Template

```markdown
### YYYY-MM-DD: Descriptive Title
**Scope:** expert-role
**Workflows:** all
**Captured:** YYYY-MM-DD
**Source:** <where this came from>
**Status:** active

Descriptive content...
```

### Rule Entry Template

```markdown
### YYYY-MM-DD: Prescriptive Action Title
**Scope:** expert-role
**Workflows:** all
**Triggers:** none
**Captured:** YYYY-MM-DD
**Source:** <where this came from>
**Status:** active

**Rule:** Clear statement of what MUST be done
```

Hook vocabulary for this role: `write:doc`, `write:csv`, `write:pack` (plus `none` for browse-only). Use `**Workflows:** all` for shared; use a registry key for job-only operations entries.

---

## Usage Tips

1. Always load this index first, then the shared pair, then the operations pair.
2. Then load `work-items/<id>/facts/facts.md` and `.../rules.md` when they exist.
3. Starter notes are guesses until the operator corrects this shop.

**Maintenance:** Route new `Workflows: all` captures to the shared pair; job-specific captures to operations. For health checks see [HOW-MEMORY-LOADING-WORKS.md](HOW-MEMORY-LOADING-WORKS.md).
