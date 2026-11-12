# How Memory Loading Works

**Question:** How does the agent know where to look first for facts and rules?

**Answer:** This gym front role loads **shared** then **operations** memory for every Work Item, plus that Work Item’s own facts/rules.

---

## Discovery

### Step 1 — Index

Always load `facts/MEMORY-INDEX.md` first.

### Step 2 — Workflow context

Identify the current Work Item from `.claude/active-context.txt` (`work-item:<id>`). Fall back to `.claude/active-work-item.txt` only when the current pointer is missing.

| Session | Directory | Memory to load |
| --- | --- | --- |
| Gym role Work Item | `work-items/<id>/` | `facts-shared` + `rules-shared` + `facts-operations` + `rules-operations` + optional `work-items/<id>/facts/` |

Read **Workflow type** from `journals/work-items/<id>/progress.md` to know which registered job is active (`check-in-day`, `retail-close`, …). That selects the workflow **instruction file**, not a different facts file. Default daily job when unset: **check-in-day** (then run **workflow-selector**).

### Step 3 — Filter inside memory files

Include an entry if `**Workflows:**` is `all` or lists the current job. Work Item facts/rules are not filtered; they belong to this pack. Route new `Workflows: all` captures to the shared pair.

### Step 4 — Tools on demand

Load `docs/tools/<name>.md` only when the workflow step names that tool.

---

## Why this shape

This Expert is one role: gym / fitness front. Shared holds always-on entries; operations holds the large pre-seeded shop starter notes. Growth stays in those pairs; **memory-optimize** watches line counts there.

---

## Configuration (`CLAUDE.md`)

At the start of each session or skill: (1) load `facts/MEMORY-INDEX.md`, (2) load shared then operations facts and rules, (3) load the active Work Item facts/rules, (4) follow `docs/role/work-item-method.md` and the selected `.claude/workflows/<job>.md`.
