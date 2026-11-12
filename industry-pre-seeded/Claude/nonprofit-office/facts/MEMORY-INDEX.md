# Memory System Index

Quick navigation for this **Nonprofit office admin** expert. Load **shared** memory for role work. Do not invent developer or incident-response files for this role — they are not used here.

---

## Two axes: Workflow (browsing) and Triggers (action)

1. **Workflow axis** (this file) — which shared entries apply to the current registered role job (`**Workflows:** all` or a registry id).

2. **Trigger axis** ([TRIGGER-INDEX.md](TRIGGER-INDEX.md)) — action-time surfacing. The PreToolUse hook `.claude/hooks/inject_rules_on_action.py` reads `trigger-index.json`. Most nonprofit-office rules use `Triggers: none` (judgment / ask). Regenerate with `python scripts/memory/build_trigger_index.py` after retagging a rule.

---

## Quick navigation

### Shared (this role)

**When to use:** Any nonprofit-office Work Item (board pack, grant file, donor list, acknowledgment draft, restricted-fund questions, minutes index, in-kind list).

**Load these files:**

- [facts-shared.md](facts-shared.md) — grant award files, restricted vs board-designated, board packets, donor CSV lists, ack templates, minutes, in-kind without FMV, fiscal year, starter shop notes
- [rules-shared.md](rules-shared.md) — never invent compliance, no money movement, no donor blast as a product, no deductibility opinion, one Work Item one folder, ask the bookkeeper

**Typical jobs:** see `.claude/workflows/workflow-registry.json` and `docs/role/work-item-method.md`.

| Workflow | Load | Start with |
| --- | --- | --- |
| board-pack, minutes-index | shared pair | board folder, minutes folder |
| grant-deadlines, grant-report, funder-gap | shared pair | award PDF, grants sheet, grant folder |
| donor-list, gift-ack-draft, in-kind-list | shared pair | donor CSV, ack template, in-kind log |
| restricted-ask | shared pair | restricted-fund sheet + gift/bank rows |

Always also load Work Item `work-items/<id>/facts/` when present.

---

## Entry format reference

### Fact

```markdown
### YYYY-MM-DD: Descriptive Title
**Scope:** expert-role
**Workflows:** all | board-pack | donor-list | ...
**Captured:** YYYY-MM-DD
**Source:** <where this came from>
**Status:** active

Descriptive content...
```

### Rule

```markdown
### YYYY-MM-DD: Prescriptive Action Title
**Scope:** expert-role
**Workflows:** all | board-pack | donor-list | ...
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

**Role title:** Nonprofit office admin

**Seed id:** `nonprofit-office`

Day-to-day role memory is the **shared** pair above. Starter entries are typical US nonprofit-office practice until the operator corrects them.
