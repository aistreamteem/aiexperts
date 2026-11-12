# Memory System Index

Quick navigation for this **Small school office (not the teacher)** expert. Load **shared** memory for role work. Do not invent developer or incident-response files for this role — they are not used here.

---

## Two axes: Workflow (browsing) and Triggers (action)

1. **Workflow axis** (this file) — which shared entries apply to the current registered role job (`**Workflows:** all` or a registry id).

2. **Trigger axis** ([TRIGGER-INDEX.md](TRIGGER-INDEX.md)) — action-time surfacing. The PreToolUse hook `.cursor/hooks/inject_rules_on_action.py` reads `trigger-index.json`. Most school-office rules use `Triggers: none` (judgment / ask). Regenerate with `python scripts/memory/build_trigger_index.py` after retagging a rule.

---

## Quick navigation

### Shared (this role)

**When to use:** Any school-office Work Item (attendance day, missing enrollment, immunization present/missing, calendar pack, pickup list, records request, transcript log, tuition from file, waitlist).

**Load these files:**

- [facts-shared.md](facts-shared.md) — attendance, enrollment packets, immunization files, calendars, pickup lists, records/transcripts, tuition files, waitlists, starter office notes
- [rules-shared.md](rules-shared.md) — never invent grades, never release without their process, never copy SSNs, pickup list wins, handbook wins, one Work Item one folder, label guesses

**Typical jobs:** see `.cursor/workflows/workflow-registry.json` and `docs/role/work-item-method.md`.

---

## Entry format reference

### Fact

```markdown
### YYYY-MM-DD: Descriptive Title
**Scope:** expert-role
**Workflows:** all | attendance-day | missing-enrollment | ...
**Captured:** YYYY-MM-DD
**Source:** <where this came from>
**Status:** active

Descriptive content...
```

### Rule

```markdown
### YYYY-MM-DD: Prescriptive Action Title
**Scope:** expert-role
**Workflows:** all | attendance-day | missing-enrollment | ...
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

**Maintenance:** New office knowledge goes in the shared pair. If a new high-value scenario appears (5+ similar questions), add a line here.

---

## Pre-seeded role

**Role title:** Small school office (not the teacher)

**Seed id:** `school-office-admin`

Day-to-day role memory is the **shared** pair above. Starter entries are typical US small-school office practice until the operator corrects them.
