# How Memory Loading Works

**Question**: How does the agent know where to look first for facts and rules?

**Answer**: This kitchen uses **operations memory** for every Work Item. Load the index, then the operations pair, then any Work Item files.

---

## Discovery Process

### Step 1: Load Navigation Index (Always First)

**File**: `facts/MEMORY-INDEX.md`

This small index is **always loaded first**. It points at operations memory and the kitchen jobs.

### Step 2: Determine Workflow Context

The agent identifies current context from session files:

| Session Type | Directory Pattern | Memory Files to Load |
| --- | --- | --- |
| **Kitchen Work Item** | `work-items/<id>/` | `facts-operations.md` + `rules-operations.md` |
| **Work Item extras** | `work-items/<id>/facts/` | that Work Item’s `facts.md` / `rules.md` if present |

**Workflow detection rules:**

1. Check `.cursor/active-context.txt` (legacy read fallback: `.cursor/active-work-item.txt`)
2. Read `journals/expert/progress.md` then the Work Item journal
3. Read `Workflow type` from the Work Item journal (a registry id such as `prep`)
4. **Default to operations memory** if ambiguous — never default to `developer` or `production-incident`

### Step 3: Load Operations Files

```
1. Load MEMORY-INDEX.md — navigation
2. Detect Work Item → kitchen operations
3. Load facts-operations.md
4. Load rules-operations.md
5. Open .cursor/workflows/<job-id>.md
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

Memory loading is documented in **AGENTS.md**: always load `facts/MEMORY-INDEX.md` first; every kitchen Work Item loads the operations pair (`facts/facts-operations.md`, `facts/rules-operations.md`).

## Memory System Files Reference

### Always Load First

- **MEMORY-INDEX.md** — Navigation

### This role (load for every job)

- **facts-operations.md** — Prep, par, walk-in count, 86, order guide, receiving, invoice, catering, allergen file, waste
- **rules-operations.md** — Never invent quantities, allergen status, inspection outcomes, or payments

### Maintenance

Run memory-optimize against the **operations** files only. Missing developer/incident/shared files are expected on this role, not an error.

When adding facts/rules, append to the operations pair and update this index if a new common scenario appears.
