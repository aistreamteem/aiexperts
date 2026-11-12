# Memory System Index

Quick navigation for this **Staffing agency office admin** expert. Load shared Expert Role memory for role work. Do not load developer or incident-response files for this role — they are not used here.

---

## Two axes: Workflow (browsing) and Triggers (action)

1. **Workflow axis** (this file) — which shared entries apply to the current registered role job (`**Workflows:** all` or a registry id).

2. **Trigger axis** ([TRIGGER-INDEX.md](TRIGGER-INDEX.md)) — action-time surfacing. The PreToolUse hook `.cursor/hooks/inject_rules_on_action.py` reads `trigger-index.json`. Most staffing-office rules use `Triggers: none` (judgment / ask). Vocabulary: `none` | `write:doc` | `write:csv` (no `config:change`). Regenerate with `python scripts/memory/build_trigger_index.py` after retagging a rule.

---

## Quick navigation

### Shared (this role)

**When to use:** Any staffing-office Work Item (assignment board, credentials, timesheets, open orders, orientation, DNS, holidays, incidents, and the other registered jobs).

**Load these files:**

- [facts-shared.md](facts-shared.md) — assignments, job orders, rates from file, timesheets, credentials, orientation, DNS/DNR, holidays, incidents, starter shop notes
- [rules-shared.md](rules-shared.md) — never fire, no employment-law, rates from file, timesheet completeness only, credential dates from their log, one Work Item one folder, label guesses, ask when shop knowledge is missing

**Typical jobs:** see `.cursor/workflows/workflow-registry.json` and `docs/role/work-item-method.md`.

Entry format: see below and [HOW-MEMORY-LOADING-WORKS.md](HOW-MEMORY-LOADING-WORKS.md).

---

## Entry format reference

### Fact

```markdown
### YYYY-MM-DD: Descriptive Title
**Scope:** expert-role
**Workflows:** all | assignment-board | timesheet-completeness | ...
**Captured:** YYYY-MM-DD
**Source:** <where this came from>
**Status:** active

Descriptive content...
```

### Rule

```markdown
### YYYY-MM-DD: Prescriptive Action Title
**Scope:** expert-role
**Workflows:** all | assignment-board | timesheet-completeness | ...
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
3. Load the active Work Item `facts/` and `rules/` if present.
4. Filter Expert Role entries to `all` or the current registry id.

**Maintenance:** New shop knowledge goes in the shared pair. If a new high-value scenario appears (5+ similar questions), add a line here.

---

## Pre-seeded role

**Role title:** Staffing agency office admin

**Seed id:** `staffing-agency-admin`

Day-to-day role memory is the **shared** pair above. Starter entries are typical US staffing-office practice until the operator corrects them.
