# Memory System Index

Quick navigation for the janitorial / contract-cleaning office Expert. Load only what the current role job needs.

---

## Two axes: workflow (browsing) and triggers (action)

1. **Workflow axis** (this file) — load operations memory for this role. Registered jobs are listed in `.cursor/workflows/workflow-registry.json`.
2. **Trigger axis** ([TRIGGER-INDEX.md](TRIGGER-INDEX.md)) — action-time surfacing. The PreToolUse hook `.cursor/hooks/inject_rules_on_action.py` reads `trigger-index.json`. Regenerate with `python scripts/memory/build_trigger_index.py` after adding or retagging a rule.

This role does **not** use software-build or incident-response memory files.

---

## Pre-seeded role

**Role title:** Janitorial / contract-cleaning office

**Seed id:** `janitorial-office`

**Method:** `docs/role/work-item-method.md`

Day-to-day role memory:

- [facts-shared.md](facts-shared.md) / [rules-shared.md](rules-shared.md) — `Workflows: all`
- [facts-operations.md](facts-operations.md) / [rules-operations.md](rules-operations.md) — job-scoped

**When to use:** Any Work Item on this role (night board, quality pack, complaints, missed service, supply par, SDS gaps, extra-work auth, holiday coverage, key log).

**Load these files:**

1. This index
2. `facts-shared.md` + `rules-shared.md`
3. `facts-operations.md` + `rules-operations.md`
4. Work Item `work-items/<id>/facts/facts.md` and `rules.md` when present
5. Tool docs named by the selected workflow

---

## Quick navigation by role job

| Job | Typical facts/rules to keep in mind |
| --- | --- |
| Night board | site, crew, hours-from-file, holiday calendar, night vs day, area split, no alarm codes |
| Quality checklist pack | quality checklist, inspection score as their form, photo, punch list, no invented score |
| Complaint callback | complaint, callback, photos, extra-work-auth if billable |
| Missed service list | missed service, keep misses visible, holiday skip is not a miss |
| Supply below par | supply par, par min, consumable brand, do not invent min |
| SDS index missing | SDS present, chemical from SDS index, no invented mix |
| Extra work auth list | extra-work-auth, add-on, extra-day, invoice from contract |
| Holiday coverage | holiday calendar, crew from roster |
| Key log completeness | key log, keys returned, badges, never copy keys |

---

## Entry format

### Fact

```markdown
### YYYY-MM-DD: Descriptive Title
**Scope:** expert-role
**Workflows:** all | night-board | complaint-callback | …
**Captured:** YYYY-MM-DD
**Source:** <where this came from>
**Status:** active
```

### Rule

```markdown
### YYYY-MM-DD: Prescriptive Title
**Scope:** expert-role
**Workflows:** all | night-board | …
**Triggers:** write:file | write:sheet | write:csv | write:doc | none
**Captured:** YYYY-MM-DD
**Source:** <where this came from>
**Status:** active
**Rule:** …
```

---

## Usage

1. Load this index, then the shared pair, then the operations pair.
2. Filter entries by `**Workflows:**` when a specific role job is active (`all` always included).
3. Route new `Workflows: all` entries to the shared pair; job-scoped entries to operations.

**Maintenance:** When adding facts/rules, append to the matching pair and update this index if a new topic appears. For health metrics see [HOW-MEMORY-LOADING-WORKS.md](HOW-MEMORY-LOADING-WORKS.md).
