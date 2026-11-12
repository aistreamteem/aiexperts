# Memory System Index

Quick navigation for this **small-plant production scheduler**. Load only what the current pack needs.

---

## Two Axes: Workflow (browsing) and Triggers (action)

1. **Workflow axis** (this file) — which memory files to load for this role.
2. **Trigger axis** ([TRIGGER-INDEX.md](TRIGGER-INDEX.md)) — action-time surfacing via `.cursor/hooks/inject_rules_on_action.py` and `trigger-index.json`.

`TRIGGER-INDEX.md` and `trigger-index.json` are **generated** by `py -3 scripts/memory/build_trigger_index.py` — never hand-edit them; regenerate after adding or retagging a rule.

---

## Quick Navigation by Workflow

### Shared (always)

**When to use:** Every session. Entries marked `Workflows: all` live here.

- [facts-shared.md](facts-shared.md) — cross-job shop facts
- [rules-shared.md](rules-shared.md) — cross-job shop rules

### Operations (registered jobs)

**When to use:** Any production-scheduler pack (dispatch, kit, shortage, traveler, WIP, due-date, outside process, machine-down, pending ECO).

- [facts-operations.md](facts-operations.md) — work orders, travelers, routers, calendar, shortages, kits, WIP, outside process, ECO-as-file, filing
- [rules-operations.md](rules-operations.md) — do not invent cycle/yield/setup/ATP; do not approve ECO; shortages and WIP stay visible; calendar wins; label guesses

**Registered jobs** (instruction files under `.cursor/workflows/`):

| Job | Load extra context from operations entries about |
| --- | --- |
| dispatch-list | work order, work center, calendar, hot list, priority, machine down |
| kit-list / shortage-vs-inventory | BOM, job qty, inventory, shortage, kit |
| traveler-completeness | traveler, drawing rev, outside process, sign-off |
| wip-by-center | WIP, queue, complete qty, machine down |
| due-date-list | due date, calendar, start date |
| outside-process-due | outside process, PO-to-op, subcontract lead |
| machine-down-vs-wip | machine down, work center, WIP |
| eco-pending-as-file | ECO as file, revision, drawing rev |

**Method:** [docs/role/work-item-method.md](../docs/role/work-item-method.md)

This role does not use developer or incident-response memory pairs.

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

Hook vocabulary for this role: `write:doc`, `write:csv` (plus `none` for browse-only). Use `**Workflows:** all` for shared; use a registry key for job-only operations entries.

---

## Usage Tips

1. Always load this index first, then the shared pair, then the operations pair.
2. Then load `work-items/<id>/facts/facts.md` and `.../rules.md` when they exist.
3. Starter notes are guesses until the operator corrects this shop.

**Maintenance:** Route new `Workflows: all` captures to the shared pair; job-specific captures to operations. For health checks see [HOW-MEMORY-LOADING-WORKS.md](HOW-MEMORY-LOADING-WORKS.md).
