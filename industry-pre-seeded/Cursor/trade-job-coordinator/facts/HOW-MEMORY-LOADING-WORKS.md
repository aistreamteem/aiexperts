# How Memory Loading Works

**Question:** How does the agent know where to look first for facts and rules?

**Answer:** Load a small index, then this role’s **operations** pair, then the active Work Item’s own facts/rules.

---

## Discovery

### Step 1: Load the index

**File:** `facts/MEMORY-INDEX.md`

Always first. It names the operations files and the registered coordinator jobs.

### Step 2: Determine workflow context

| Session | Directory | Memory to load |
| --- | --- | --- |
| **Coordinator Work Item** | `work-items/WID-*` | `facts-operations.md` + `rules-operations.md` |

**Detection:**

1. Read `.cursor/active-context.txt` (legacy `.cursor/active-work-item.txt` as read fallback only)
2. Read the Work Item journal **Workflow type** (a registry id such as `daily-board` or `parts-ready`)
3. If still ambiguous, default to **operations** memory and ask **workflow-selector** — do not default to a developer or incident pipeline

### Step 3: Load operations files

```
1. MEMORY-INDEX.md
2. facts-operations.md
3. rules-operations.md
4. work-items/<id>/facts/facts.md and rules.md when present
```

Filter Expert Role entries whose `**Workflows:**` is `all` or matches the current registry id.

### Step 4: On-demand tools

Load `docs/tools/<name>.md` only when the current YAML step names that tool.

---

## Why this is enough

This expert is one role. Splitting memory into developer vs incident files would hide trade-coordinator rules. Growth stays in the operations pair; use **memory-optimize** if a file becomes unwieldy. `Workflows: all` entries live in the operations pair (this role’s always-loaded memory).

## Configuration (AGENTS.md)

At the start of each session or skill: load MEMORY-INDEX, then operations facts/rules, then Work Item memory. Method: `docs/role/work-item-method.md`.
