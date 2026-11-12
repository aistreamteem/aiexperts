# Memory System Index

Quick navigation for the equipment-rental role memory. Load only what this job needs.

---

## Two axes: browsing and triggers

1. **Workflow axis** (this file) — which memory files to load for this role.
2. **Trigger axis** ([TRIGGER-INDEX.md](TRIGGER-INDEX.md)) — action-time surfacing via `.cursor/hooks/inject_rules_on_action.py` and `trigger-index.json`.

`TRIGGER-INDEX.md` and `trigger-index.json` are **generated** by `python scripts/memory/build_trigger_index.py`. Regenerate after adding or retagging a rule.

---

## Pre-seeded role

**Role title:** Equipment rental role

**Seed id:** `equipment-rental`

Day-to-day role memory is the **operations** pair:

- [facts-operations.md](facts-operations.md)
- [rules-operations.md](rules-operations.md)

Work Item method: `docs/role/work-item-method.md`. Registered jobs: `.cursor/workflows/workflow-registry.json`.

### Operations (this role)

**When to use:** Any Work Item for this rental role (reservation day, contract completeness, COI, inspections, delivery tickets, meters, PM due, return damage, utilization).

**Load these files:**

- [facts-operations.md](facts-operations.md)
- [rules-operations.md](rules-operations.md)

**Typical topics:** fleet item, serial, hour meter, reservation vs available vs on-rent, contract fields, rate-from-file, COI completeness, outgoing/return inspection, damage notes and photos, delivery zone, fuel and cleaning policy, utilization formula, maintenance-due as their file.

There is no developer or production-incident memory for this Expert. Do not look for those files.

---

## Entry format

### Fact

```markdown
### YYYY-MM-DD: Descriptive Title
**Scope:** expert-role
**Workflows:** all | <job-id>
**Captured:** YYYY-MM-DD
**Source:** <where this came from>
**Status:** active

Descriptive content...
```

### Rule

```markdown
### YYYY-MM-DD: Prescriptive Action Title
**Scope:** expert-role
**Workflows:** all | <job-id>
**Triggers:** write:doc | write:csv | none
**Captured:** YYYY-MM-DD
**Source:** <where this came from>
**Status:** active

**Rule:** Clear statement of what MUST be done
```

---

## Usage

1. Always load this index first.
2. Load `facts-operations.md` + `rules-operations.md`.
3. If a Work Item is active, also load `work-items/<id>/facts/facts.md` and `rules.md`.
4. Follow rules. Facts inform the pack. Label starter notes as guesses until the operator confirms this yard.

**Maintenance:** When adding facts/rules, put them in the operations files. After retagging a rule trigger, regenerate the trigger index. For health checks, see [HOW-MEMORY-LOADING-WORKS.md](HOW-MEMORY-LOADING-WORKS.md).
