# Memory System Index

Quick navigation for this **Nonprofit office admin** expert. Load shared memory for role work. Do not load developer or incident-response files for this role — they are not the live memory.

---

## Two axes: Workflow (browsing) and Triggers (action)

1. **Workflow axis** (this file) — which shared entries apply to the current registered role job (`**Workflows:** all` or a registry id).

2. **Trigger axis** ([TRIGGER-INDEX.md](TRIGGER-INDEX.md)) — action-time surfacing. The PreToolUse hook `.cursor/hooks/inject_rules_on_action.py` reads `trigger-index.json`. Most nonprofit-office rules use `Triggers: none` (judgment / ask). Regenerate with `python scripts/memory/build_trigger_index.py` after retagging a rule.

---

## Quick navigation

### Shared (this role)

**When to use:** Any nonprofit-office Work Item (board pack, minutes index, grant deadlines, grant report, funder gap, donor list, gift ack draft, in-kind list, restricted ask).

**Load these files:**

- [facts-shared.md](facts-shared.md) — grants, board packs, donor files, acknowledgments, restricted funds, minutes, starter shop notes
- [rules-shared.md](rules-shared.md) — never invent restriction codes or deductibility, no 990 stamp, no money movement, they communicate, one Work Item one folder

**Typical jobs:** see `.cursor/workflows/workflow-registry.json` and `docs/role/work-item-method.md`.

---

## Entry format reference

### Fact

```markdown
### YYYY-MM-DD: Descriptive Title
**Scope:** expert-role
**Workflows:** all | board-pack | grant-deadlines | ...
**Captured:** YYYY-MM-DD
**Source:** <where this came from>
**Status:** active

Descriptive content...
```

### Rule

```markdown
### YYYY-MM-DD: Prescriptive Action Title
**Scope:** expert-role
**Workflows:** all | board-pack | grant-deadlines | ...
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

**Maintenance:** New shop knowledge goes in the shared pair (`Workflows: all` or specific registry ids). If a new high-value scenario appears (5+ similar questions), add a line here.

---

## Pre-seeded role

**Role title:** Nonprofit office admin

**Seed id:** `nonprofit-office`

Day-to-day role memory is the **shared** pair above. Starter entries are typical US small-nonprofit office practice until the operator corrects them.
