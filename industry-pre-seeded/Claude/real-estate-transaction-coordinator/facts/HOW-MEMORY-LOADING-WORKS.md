# How Memory Loading Works

**Question:** How does the agent know where to look first for facts and rules?

**Answer:** This real-estate transaction-coordinator Expert loads **operations memory** for every Work Item, plus that Work Item’s own facts/rules when they exist.

---

## Discovery Process

### Step 1: Load Navigation Index (Always First)

**File:** `facts/MEMORY-INDEX.md`

Small routing file. Always load it before operations memory.

### Step 2: Determine workflow context

| Session type | Directory pattern | Memory files to load |
| --- | --- | --- |
| **Transaction Work Item** | `work-items/WID-*` | `facts-operations.md` + `rules-operations.md` |
| **Q&A session** | `qa-sessions/Q*` | Same operations pair; do not persist unverified notes until close |

Detection:

1. Read `.claude/active-context.txt` (legacy read fallback: `.claude/active-work-item.txt`)
2. Read the Work Item journal **Workflow type** (a registry id such as `dates-calendar`, `missing-docs`, `closing-checklist`)
3. Default to **operations** memory if ambiguous. Never load software-pipeline or incident-bridge files; this role does not have them.

### Step 3: Load operations files only

```
1. Load MEMORY-INDEX.md
2. Detect work-items/WID-… → TC role job
3. Load facts-operations.md
4. Load rules-operations.md
5. Load work-items/<id>/facts/facts.md and rules.md when present
```

Filter Expert Role entries by **Workflows:** when a specific registered job is active: include the entry if the field is `all` or lists that job id.

### Step 4: On-demand tools and method

Load `docs/role/work-item-method.md` when starting or continuing a Work Item. Load a `docs/tools/*.md` file only when the current workflow step cites it.

---

## Why this approach works

This role is one role. Splitting memory into developer vs incident files would hide shop TC rules. Growth stays in the operations pair (this role’s always-loaded equivalent of the shared pair). `/memory-optimize` watches those two files.

### Updating MEMORY-INDEX.md

After adding facts/rules:

1. Keep the operations pair as the live store
2. Add a pointer only for a new high-value topic
3. Regenerate the trigger index after tagging a rule with a non-`none` trigger
