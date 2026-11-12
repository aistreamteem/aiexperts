# Memory System Index

Quick navigation for this **Gym / fitness front role** Expert. Load only what the current pack needs.

---

## Two axes

1. **Workflow axis** (this file) — which memory files to load for a gym role job.
2. **Trigger axis** ([TRIGGER-INDEX.md](TRIGGER-INDEX.md)) — action-time surfacing. The PreToolUse hook `.claude/hooks/inject_rules_on_action.py` reads `trigger-index.json`. Regenerate with `python scripts/memory/build_trigger_index.py` after adding or retagging a rule.

---

## This role’s memory

**Role title:** Gym / fitness front role  
**Seed id:** `gym-front-role`

Always load the **shared** pair, then the **operations** pair:

- [facts-shared.md](facts-shared.md) / [rules-shared.md](rules-shared.md) — `Workflows: all` entries
- [facts-operations.md](facts-operations.md) — memberships, check-in, waivers, freeze/cancel, PT, classes, retail close
- [rules-operations.md](rules-operations.md) — never invent dues, no medical/diet, no EFT run, waiver required, one Work Item one folder

**When to load:** every Work Item for this role.

**Registered role jobs:** `check-in-day`, `access-flag-exceptions`, `guest-pass-log`, `missing-waivers`, `freeze-and-cancel-list`, `failed-draft-list`, `class-roster`, `pt-session-counts`, `retail-close`.

This expert does **not** load developer or production-incident memory files. Those are not this role.

### Work Item memory

- `work-items/<id>/facts/facts.md`
- `work-items/<id>/facts/rules.md`

Job-specific notes (this day’s scan export quirks, this class capacity). Promote into shared or operations when the operator agrees.

---

## Entry format

### Fact

```markdown
### YYYY-MM-DD: Descriptive Title
**Scope:** expert-role
**Workflows:** all | check-in-day | retail-close | …
**Captured:** YYYY-MM-DD
**Source:** <where this came from>
**Status:** active

Descriptive content...
```

### Rule

```markdown
### YYYY-MM-DD: Prescriptive Title
**Scope:** expert-role
**Workflows:** all | check-in-day | …
**Triggers:** write:csv | write:pack | write:doc | none
**Captured:** YYYY-MM-DD
**Source:** <where this came from>
**Status:** active

**Rule:** what MUST be done
```

---

## Usage

1. Always load this index first.
2. Load `facts-shared.md` + `rules-shared.md`, then `facts-operations.md` + `rules-operations.md`.
3. Load the active Work Item facts/rules if present.
4. Follow the selected workflow file under `.claude/workflows/`.

**Maintenance:** when adding a new topic, add a pointer here if operators would not find it from the headings alone. Run the memory-optimize analyze script when files grow quickly.
