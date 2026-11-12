# How Memory Loading Works

**Question:** How does the agent know where to look first for facts and rules?

**Answer:** This construction office Expert always loads **shared** memory. Work Items are role jobs (daily log, RFI aging, punch, …), not software-build or outage-role workflows.

---

## Discovery

### Step 1: Load this navigation index

**File:** `facts/MEMORY-INDEX.md`

Always first. It points at shared memory and this role’s registered jobs.

### Step 2: Determine Work Item context

| Session type | Directory | Memory files |
| --- | --- | --- |
| Construction office pack | `work-items/WID-*` | `facts-shared.md` + `rules-shared.md` |
| Work Item extras | `work-items/<id>/facts/` | that Work Item’s facts.md + rules.md |

Detection:

1. Read `.claude/active-context.txt` (`work-item:<id>`); if missing, read legacy `.claude/active-work-item.txt`
2. Read the Work Item journal **Workflow type** (a registry id such as `daily-log`)
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

## Why this is smaller than a split-by-engineering-workflow memory

This seed stores shop knowledge in one shared pair. Adding a new RFI fact does not require extra workflow files. `memory-optimize` should score **shared** files only.

## Configuration (CLAUDE.md)

Memory loading by workflow: at start of each session or skill, load (1) `facts/MEMORY-INDEX.md`, (2) shared facts and rules, (3) active Work Item facts/rules. See MEMORY-INDEX.md.
