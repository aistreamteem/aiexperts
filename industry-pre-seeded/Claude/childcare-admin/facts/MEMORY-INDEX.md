# Memory System Index

Quick navigation for the **Childcare center office** Expert. Load only the files this role needs.

---

## Two Axes: Workflow (browsing) and Triggers (action)

Rules are indexed on **two orthogonal axes**:

1. **Workflow axis** (this file) — load shared + operations memory for this role’s registered jobs.
2. **Trigger axis** ([TRIGGER-INDEX.md](TRIGGER-INDEX.md)) — action-time surfacing. The PreToolUse hook `.claude/hooks/inject_rules_on_action.py` reads `trigger-index.json`. Most childcare-office rules use `Triggers: none` (judgment/gates), so the generated index may be empty until a rule is tagged `write:doc` or `write:csv`.

`TRIGGER-INDEX.md` and `trigger-index.json` are **generated** by `python scripts/memory/build_trigger_index.py` — never hand-edit them; regenerate after adding or retagging a rule.

---

## Pre-seeded role

**Role title:** Childcare center office (not the teacher)

**Seed id:** `childcare-admin`

**Work-item method:** `docs/role/work-item-method.md`

### Shared (always loaded)

- [facts-shared.md](facts-shared.md)
- [rules-shared.md](rules-shared.md)

### Operations (this role’s jobs)

- [facts-operations.md](facts-operations.md)
- [rules-operations.md](rules-operations.md)

Do **not** invent software-build or incident-response memory files for this role.

**Registered workflows** (also in `.claude/workflows/workflow-registry.json`):

| Job | When |
| --- | --- |
| `attendance-day` | Present/absent list for a program date |
| `pickup-list-check` | Authorized adults vs sign-out |
| `ratio-from-their-posted` | Their posted ratio only |
| `missing-enrollment-forms` | Packet pages present/missing |
| `waitlist` | Wait pool as they coded it |
| `tuition-from-file` | Rates and ledger they dropped |
| `licensing-packet-completeness` | Binder pages vs their checklist |
| `incident-routing` | Forms still needing a director signature |
| `holiday-calendar-pack` | Closures from their calendar file |

---

## Entry Format Reference

### Fact Entry Template

```markdown
### YYYY-MM-DD: Descriptive Title
**Scope:** expert-role
**Workflows:** all | attendance-day | pickup-list-check | ...
**Captured:** YYYY-MM-DD
**Source:** <where this came from>
**Status:** active
```

### Rule Entry Template

```markdown
### YYYY-MM-DD: Prescriptive Action Title
**Scope:** expert-role
**Workflows:** all | attendance-day | ...
**Triggers:** write:doc | write:csv | none
**Captured:** YYYY-MM-DD
**Source:** <where this came from>
**Status:** active
**Rule:** Clear statement of what MUST be done
```

---

### Usage Tips

1. Always load this index first.
2. Then load the shared pair, then the operations pair.
3. Then load `work-items/<id>/facts/` for the active job.
4. For how files are laid out, see the “How this role files work items” fact in facts-operations.md.

---

**Maintenance Note:** `Workflows: all` entries go in the shared files. Job-specific entries go in operations. If a topic is new, add a line here. See [HOW-MEMORY-LOADING-WORKS.md](HOW-MEMORY-LOADING-WORKS.md).
