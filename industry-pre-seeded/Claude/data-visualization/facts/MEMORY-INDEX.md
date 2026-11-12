# Memory System Index

Quick navigation for this role: **Data visualization from their files**. Load the shared pair, then the operations pair. Other-role memory files are not this role.

---

## Two Axes: Workflow (browsing) and Triggers (action)

Rules are indexed on **two orthogonal axes**:

1. **Workflow axis** (this file) — load shared + operations memory for chart packs. Registered jobs (`describe-csv`, `time-series-line`, …) share these files; filter by `**Workflows:**` when a job-specific entry exists.

2. **Trigger axis** ([TRIGGER-INDEX.md](TRIGGER-INDEX.md)) — action-time surfacing. Every rule carries a `**Triggers:**` field (`write:python`, `write:csv`, `write:chart`, `write:doc`, or `none`). The PreToolUse hook `.claude/hooks/inject_rules_on_action.py` reads `trigger-index.json`.

`TRIGGER-INDEX.md` and `trigger-index.json` are **generated** by `python scripts/memory/build_trigger_index.py` — never hand-edit them.

---

## Pre-seeded role

**Role title:** Data visualization from their files

**Seed id:** `data-visualization`

**Work Item method:** `docs/role/work-item-method.md`

Day-to-day role memory:

- [facts-shared.md](facts-shared.md) / [rules-shared.md](rules-shared.md) — `Workflows: all`
- [facts-operations.md](facts-operations.md) / [rules-operations.md](rules-operations.md) — chart-job specific or pre-seeded pack knowledge

### When to load

**When to use:** Any chart pack, describe, histogram, bars, line, scatter, small multiples, missing/outliers, or refresh.

**Load these files:**

1. This index
2. `facts-shared.md` and `rules-shared.md`
3. `facts-operations.md` and `rules-operations.md`
4. Active Work Item `work-items/<id>/facts/facts.md` and `rules.md` when present

---

## Quick Navigation by chart job

| Job | Registry id | Memory |
| --- | --- | --- |
| Describe a CSV | `describe-csv` | shared + operations |
| Group-compare bars | `group-compare-bars` | shared + operations |
| Histogram pack | `histogram-pack` | shared + operations |
| Missing and outliers | `missing-and-outliers` | shared + operations |
| Refresh from new export | `refresh-from-new-export` | shared + operations |
| Scatter and correlation | `scatter-and-corr` | shared + operations |
| Small multiples | `small-multiples` | shared + operations |
| Time-series line | `time-series-line` | shared + operations |

Default job: `describe-csv`.

---

## Entry Format Reference

### Fact Entry Template

```markdown
### YYYY-MM-DD: Descriptive Title
**Scope:** expert-role
**Workflows:** all | describe-csv | time-series-line | …
**Captured:** YYYY-MM-DD
**Source:** <where this came from>
**Status:** active

Descriptive content...
```

### Rule Entry Template

```markdown
### YYYY-MM-DD: Prescriptive Action Title
**Scope:** expert-role
**Workflows:** all | registered workflow id
**Triggers:** write:python | write:csv | write:chart | write:doc | none
**Captured:** YYYY-MM-DD
**Source:** <where this came from>
**Status:** active

**Rule:** Clear statement of what MUST be done
```

Work Item-level entries omit `**Workflows:**` and live under `work-items/<id>/facts/`.

---

### Usage Tips

1. Always load this index first, then shared, then operations.
2. Registered chart jobs share this memory; do not look for other-role memory files.
3. For system health, see [HOW-MEMORY-LOADING-WORKS.md](HOW-MEMORY-LOADING-WORKS.md) and **memory-optimize**.

**Maintenance:** `Workflows: all` entries go in the shared files; job-specific entries go in operations. Add a pointer here only when a new topic or reference doc appears.
