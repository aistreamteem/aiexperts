# How Memory Loading Works

**Question:** How does the agent know where to look first for facts and rules?

**Answer:** Load a small index, then this role’s **shared** pair, then the active Work Item’s own facts/rules.

---

## Discovery

### Step 1: Load the index

**File:** `facts/MEMORY-INDEX.md`

Always first. It names the shared files and the registered school-office jobs.

### Step 2: Determine workflow context

| Session | Directory | Memory to load |
| --- | --- | --- |
| **School-office Work Item** | `work-items/WID-*` | `facts-shared.md` + `rules-shared.md` |

**Detection:**

1. Read `.cursor/active-context.txt` (legacy read fallback: `.cursor/active-work-item.txt`)
2. Read the Work Item journal **Workflow type** (a registry id such as `attendance-day` or `missing-enrollment`)
3. If still ambiguous, default to **shared** memory and ask **workflow-selector** — do not invent a developer or incident pipeline

### Step 3: Load shared files

```
1. MEMORY-INDEX.md
2. facts-shared.md
3. rules-shared.md
4. work-items/<id>/facts/facts.md and rules.md when present
```

Filter Expert Role entries whose `**Workflows:**` is `all` or matches the current registry id.

### Step 4: On-demand tools

Load `docs/tools/<name>.md` only when the current YAML step names that tool.

---

## Why this is enough

This expert is one role. Splitting memory into developer vs incident files would hide school-office rules. Growth stays in the shared pair; use **memory-optimize** if a file becomes unwieldy.

## Configuration (AGENTS.md)

At the start of each session or skill: load MEMORY-INDEX, then shared facts/rules, then Work Item memory. Method: `docs/role/work-item-method.md`.
