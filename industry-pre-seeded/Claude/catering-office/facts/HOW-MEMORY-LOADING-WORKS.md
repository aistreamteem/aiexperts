# How Memory Loading Works

**Question**: How does the agent know where to look first for facts and rules?

**Answer**: This catering office uses **operations memory** for every Work Item. Load the index, then the operations pair, then any Work Item files.

---

## Discovery Process

### Step 1: Load Navigation Index (Always First)

**File**: `facts/MEMORY-INDEX.md`

This small index is **always loaded first**. It points at operations memory and the catering jobs.

### Step 2: Determine Workflow Context

The agent identifies current context from session files:

| Session Type | Directory Pattern | Memory Files to Load |
| --- | --- | --- |
| **Catering Work Item** | `work-items/WID-*` | `facts-operations.md` + `rules-operations.md` |
| **Work Item extras** | `work-items/<id>/facts/` | that Work Item’s `facts.md` / `rules.md` if present |

**Workflow detection rules:**

1. Check `.claude/active-context.txt` (legacy read fallback: `.claude/active-work-item.txt`)
2. Read `journals/expert/progress.md` then the Work Item journal
3. Read `Workflow type` from the Work Item journal (a registry id such as `pack-out-list`)
4. **Default to operations memory** if ambiguous — never default to `developer` or `production-incident`

### Step 3: Load Operations Files

```
1. Load MEMORY-INDEX.md — navigation
2. Detect Work Item WID-… → catering office operations
3. Load facts-operations.md
4. Load rules-operations.md
5. Open .claude/workflows/<job-id>.md
```

### Step 4: On-Demand Reference Materials

Tool docs under `docs/tools/` load only when the current workflow step names them.

---

## Routing Logic

```
IF a Work Item is active
  → workflow memory = operations
  → load facts-operations.md + rules-operations.md
  → job steps = selected registry workflow
ELSE
  → check active-context / ask workflow-selector
  → still load operations memory
```

Do not route this role to developer or production-incident files.

---

## Configuration (AGENTS.md)

Memory loading is documented in **AGENTS.md** item 21: always load `facts/MEMORY-INDEX.md` first; every catering Work Item loads the operations pair.

## Memory System Files Reference

### Always Load First

- **MEMORY-INDEX.md** — Navigation

### This role (load for every job)

- **facts-operations.md** — Event order, guarantee, pack-out, kit, dietary, leftover policy
- **rules-operations.md** — Ask-if-missing, never-invent, leftover form, one Work Item per event

### Maintenance

Run memory-optimize against the **operations** files only. Missing developer/incident files are expected on this role, not an error.

When adding facts/rules, append to the operations pair and update this index if a new common scenario appears (5+ similar questions).
