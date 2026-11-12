# Memory System Index

Quick navigation for the **Hotel / inn front role** Expert. Load only the files you need.

---

## Two Axes: Workflow (browsing) and Triggers (action)

Rules are indexed on **two orthogonal axes**:

1. **Workflow axis** (this file, below) — *human browsing + context-budget loading*. This role’s live memory is the **operations** pair.

2. **Trigger axis** ([TRIGGER-INDEX.md](TRIGGER-INDEX.md)) — *action-time surfacing*. Every rule may carry a `**Triggers:**` field (`write:doc`, `write:csv`, `none`, …). The PreToolUse hook `.cursor/hooks/inject_rules_on_action.py` reads `trigger-index.json` and injects matching rule text at the moment of the action.

`TRIGGER-INDEX.md` and `trigger-index.json` are **generated** by `python scripts/memory/build_trigger_index.py` – never hand-edit them; regenerate after adding or retagging a rule (the `remember`/`promote-facts-rules` skills prompt for this).

---

## Pre-seeded role

**Role title:** Hotel / inn front role

**Seed id:** `hotel-front-role`

**Work-item method:** `docs/role/work-item-method.md`

Day-to-day role memory lives in the **operations** pair:

- [facts-operations.md](facts-operations.md)
- [rules-operations.md](rules-operations.md)

This role does not keep a separate coding or incident-response memory pair. Use operations only.

### Operations (hotel role)

**When to use:** Any Work Item for this role (arrivals, due-outs, house count, folio exceptions, groups, night-audit packet, no-shows, OOO, tax-exempt).

**Load these files:**

- [facts-operations.md](facts-operations.md) — arrivals, in-house, departures, room status, house count, folios, groups, tax, night audit as files, and related role vocabulary
- [rules-operations.md](rules-operations.md) — rates/taxes from file, no PAN, no ADA legal, ask when export missing, one Work Item one folder, label guesses


---

## Quick Navigation by registered job

| Job | What to recall first in operations memory |
| --- | --- |
| arrivals-day | arrivals, room status, DNR, early check-in ask, ADA as inventory |
| departures-due-out | departures, due-out, in-house, late checkout ask, folio |
| house-count | house count, occupancy percent from their math, ADR from their report, OOO |
| ooo-and-status | out of order, room status |
| group-block-vs-pickup | group block, cutoff, wash, BEO if any |
| folio-exceptions | folio, posting from POS, tax file, comp as their code |
| tax-exempt-completeness | tax-exempt cert present, tax file |
| no-show-list | no-show, cancellation policy file, night audit as file |
| night-audit-file-check | night audit as file, house count, folio exceptions |

---

## Entry Format Reference

### Fact Entry Template

```markdown
### YYYY-MM-DD: Descriptive Title

**Scope:** expert-role

**Workflows:** all

**Captured:** YYYY-MM-DD

**Source:** <where this came from>

Descriptive content about what this is, how it works, what it means...
```

### Rule Entry Template

```markdown
### YYYY-MM-DD: Prescriptive Action Title

**Scope:** expert-role

**Workflows:** all

**Triggers:** write:doc | write:csv | none

**Captured:** YYYY-MM-DD

**Source:** <where this came from>

**Rule:** Clear statement of what MUST be done

**Why:** Rationale and context for why this rule exists

**How to apply:**

1. Step-by-step procedure
```

---

### Usage Tips

**For a role Work Item:**

1. Load MEMORY-INDEX.md
2. Load `facts-operations.md` + `rules-operations.md`
3. Load `work-items/<id>/facts/` if present
4. Open the registered workflow file

**Maintenance Note:** When adding new facts/rules, append to the operations pair. If useful as a large reference, add a pointer here. For system health metrics, see [HOW-MEMORY-LOADING-WORKS.md](HOW-MEMORY-LOADING-WORKS.md).
