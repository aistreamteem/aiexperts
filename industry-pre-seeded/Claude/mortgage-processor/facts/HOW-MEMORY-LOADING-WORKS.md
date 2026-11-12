# How Memory Loading Works

**Question:** How does the agent know where to look first for facts and rules?

**Answer:** This mortgage-processor Expert always loads **shared** memory. Work Items are registered loan-file jobs (conditions checklist, missing docs, date stamps, …), not software-build or outage-role workflows.

---

## Discovery

### Step 1: Load this navigation index

**File:** `facts/MEMORY-INDEX.md`

Always first. It points at shared memory and this role’s registered jobs.

### Step 2: Determine Work Item context

| Session type | Directory | Memory files |
| --- | --- | --- |
| Processor Work Item | `work-items/<id>/` | `facts-shared.md` + `rules-shared.md` |
| Work Item extras | `work-items/<id>/facts/` | that Work Item’s facts.md + rules.md |

Detection:

1. Read `.claude/active-context.txt` (`work-item:<id>`); if missing, read legacy `.claude/active-work-item.txt` (read-only fallback)
2. Read the Work Item journal **Workflow type** (a registry id such as `conditions-checklist`)
3. Always load the **shared** pair for this role

### Step 3: Load shared files only

```
1. MEMORY-INDEX.md
2. facts/facts-shared.md
3. facts/rules-shared.md
4. work-items/<id>/facts/ if present
```

Do not load software-engineering or outage-role memory files. Those files are not this role.

### Step 4: On-demand tools

Load `docs/tools/<name>.md` only when the current workflow step names that tool.

---

## Why this shape

This Expert is one role: mortgage processor (file completeness). Shop knowledge that applies to every loan pack lives in the shared pair. A registered job selects the workflow instruction file, not a different facts file. `memory-optimize` scores the shared files.

## Configuration (CLAUDE.md)

At the start of each session or skill: (1) load `facts/MEMORY-INDEX.md`, (2) load shared facts and rules, (3) load the active Work Item facts/rules, (4) follow `docs/role/work-item-method.md` and the selected `.claude/workflows/<job>.md`.
