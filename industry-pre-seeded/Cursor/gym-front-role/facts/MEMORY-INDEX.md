# Memory System Index

Quick navigation for the Gym / fitness front role expert. Load only the files you need.

---

## Two axes: workflow (browsing) and triggers (action)

1. **Workflow axis** (this file) — which memory files to load for this role job.
2. **Trigger axis** ([TRIGGER-INDEX.md](TRIGGER-INDEX.md)) — action-time surfacing via `.cursor/hooks/inject_rules_on_action.py` and `trigger-index.json`.

`TRIGGER-INDEX.md` and `trigger-index.json` are **generated** by `python scripts/memory/build_trigger_index.py` — never hand-edit them; regenerate after adding or retagging a rule.

---

## Pre-seeded role

**Role title:** Gym / fitness front role

**Seed id:** `gym-front-role`

**Work-item method:** `docs/role/work-item-method.md`

Day-to-day role memory lives in the **operations** pair:

- [facts-operations.md](facts-operations.md) — memberships, check-in, waivers, freeze/cancel, PT, classes, retail close
- [rules-operations.md](rules-operations.md) — never invent dues, no medical/diet, no EFT run, waiver required, one Work Item one folder

### Operations (this role)

**When to use:** Any Work Item under `work-items/` for this gym role.

**Load these files:**
- [facts-operations.md](facts-operations.md)
- [rules-operations.md](rules-operations.md)

**Registered role jobs:** `check-in-day`, `access-flag-exceptions`, `guest-pass-log`, `missing-waivers`, `freeze-and-cancel-list`, `failed-draft-list`, `class-roster`, `pt-session-counts`, `retail-close`.

This expert does **not** load developer or production-incident memory files. Those are not this role.

---

## Entry format reference

### Fact entry template

```markdown
### YYYY-MM-DD: Descriptive Title

**Scope:** expert-role

**Workflows:** all | check-in-day | retail-close | ...

**Captured:** YYYY-MM-DD

**Source:** <where this came from>

Descriptive content...
```

### Rule entry template

```markdown
### YYYY-MM-DD: Prescriptive Action Title

**Scope:** expert-role

**Workflows:** all | check-in-day | ...

**Triggers:** write:doc | write:csv | none

**Captured:** YYYY-MM-DD

**Source:** <where this came from>

**Rule:** Clear statement of what MUST be done
```

---

### Usage tips

1. Always load this index first, then the operations pair.
2. Add Work Item `work-items/<id>/facts/facts.md` and `work-items/<id>/facts/rules.md` when a Work Item is active.
3. Starter notes are guesses until this club corrects them.

**Maintenance:** When adding facts/rules, classify by role job if needed; otherwise `all`. For health checks, see [HOW-MEMORY-LOADING-WORKS.md](HOW-MEMORY-LOADING-WORKS.md).
