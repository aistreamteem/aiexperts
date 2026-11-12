# How Memory Loading Works

**Question:** How does the agent know where to look first for facts and rules?

**Answer:** Load a small index, then the **shared** pair (always), then this role’s **operations** pair, then the active Work Item’s own facts/rules.

---

## Discovery

### Step 1 — Index

Always load `facts/MEMORY-INDEX.md` first.

### Step 2 — Workflow context

Identify the current Work Item from `.cursor/active-context.txt` (`work-item:<id>`), with legacy read fallback `.cursor/active-work-item.txt`.

| Session | Directory | Memory to load |
| --- | --- | --- |
| Inventory Work Item | `work-items/<id>/` | shared pair + operations pair + optional `work-items/<id>/facts/` |

Read **Workflow type** from `journals/work-items/<id>/progress.md` to know which registered job is active (`receiving-match`, `cycle-count`, …). That selects the workflow instruction file, not a different facts file. Default if ambiguous: **shared + operations**, then ask **workflow-selector**.

### Step 3 — Filter

- Shared pair: always load; entries are `Workflows: all`.
- Operations pair: include an entry if `**Workflows:**` is `all` or lists the current job.
- Work Item facts/rules are not filtered; they belong to this job.

### Step 4 — Tools on demand

Load `docs/tools/<name>.md` only when the workflow step names that tool.

---

## Why this shape

This Expert is one role: wholesale / inventory. Do not invent developer or incident-response memory pairs. Growth stays in shared + operations; **memory-optimize** watches line count.

---

## Configuration (`AGENTS.md`)

At the start of each session or skill: (1) load `facts/MEMORY-INDEX.md`, (2) load shared facts/rules, (3) load operations facts/rules, (4) load the active Work Item facts/rules, (5) follow `docs/role/work-item-method.md` and the selected `.cursor/workflows/<job>.md`.
