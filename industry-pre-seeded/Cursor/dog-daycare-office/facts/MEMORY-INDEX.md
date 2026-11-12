# Memory System Index

Quick navigation for this **Dog daycare / boarding office** expert. Load shared memory for role work. Do not load developer or incident-response files for this role — they are not the live memory.

---

## Two axes: Workflow (browsing) and Triggers (action)

1. **Workflow axis** (this file) — which shared entries apply to the current registered role job (`**Workflows:** all` or a registry id).

2. **Trigger axis** ([TRIGGER-INDEX.md](TRIGGER-INDEX.md)) — action-time surfacing. The PreToolUse hook `.cursor/hooks/inject_rules_on_action.py` reads `trigger-index.json`. Most daycare/boarding rules use `Triggers: none` (judgment / ask). Regenerate with `python scripts/memory/build_trigger_index.py` after retagging a rule.

---

## Quick navigation

### Shared (this role)

**When to use:** Any daycare/boarding Work Item (boarding day, capacity vs booked, feeding from cards, missing vaccine files, pickup list, waitlist, waiver missing, incident routing, meds-to-give as written).

**Load these files:**

- [facts-shared.md](facts-shared.md) — boarding cards, occupancy, vaccine-file present/missing, feeding as written, pickup authorization, waitlists, starter shop notes
- [rules-shared.md](rules-shared.md) — never diagnose, never decide a vaccine is due, never release a dog, never invent a fee, feeding/meds as written, one Work Item one folder, label guesses

**Typical jobs:** see `.cursor/workflows/workflow-registry.json` and `docs/role/work-item-method.md`.

---

## Entry format reference

### Fact

```markdown
### YYYY-MM-DD: Descriptive Title
**Scope:** expert-role
**Workflows:** all | boarding-day | pickup-list | ...
**Captured:** YYYY-MM-DD
**Source:** <where this came from>
**Status:** active

Descriptive content...
```

### Rule

```markdown
### YYYY-MM-DD: Prescriptive Action Title
**Scope:** expert-role
**Workflows:** all | boarding-day | pickup-list | ...
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

**Role title:** Dog daycare / boarding office

**Seed id:** `dog-daycare-office`

Day-to-day role memory is the **shared** pair above. Starter entries are typical US daycare/boarding-office practice until the operator corrects them.
