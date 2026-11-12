# How Memory Loading Works

**Question:** How does the agent know where to look first for facts and rules?

**Answer:** This childcare-office Expert always loads the **shared** pair, then the **operations** pair for registered jobs. It does not invent software-build or incident-response memory.

---

## Discovery Process

### Step 1: Load Navigation Index (Always First)

**File:** `facts/MEMORY-INDEX.md`

### Step 2: Determine Workflow Context

| Session Type | Directory Pattern | Memory Files to Load |
| --- | --- | --- |
| **Role Work Item** | `work-items/<id>/` | shared + operations |

**Detection:**

1. `.cursor/active-context.txt` (legacy read fallback: `.cursor/active-work-item.txt`)
2. Work Item journal **Workflow type** (a registered job id such as `attendance-day`)
3. Default if ambiguous: `attendance-day`

### Step 3: Load Files

```
1. Load MEMORY-INDEX.md
2. Load facts-shared.md + rules-shared.md
3. Load facts-operations.md + rules-operations.md
4. Load work-items/<id>/facts/facts.md and rules.md when present
```

Filter Expert Role entries by `**Workflows:**` (`all` or the current job id). Work Item entries are not filtered.

### Step 4: On-Demand References

Large tool docs under `docs/tools/` and work maps under `.cursor/workflows/` load when the selected job names them.

---

## Configuration (AGENTS.md)

At start of each session or skill: load `facts/MEMORY-INDEX.md`, then shared, then operations, then the active Work Item facts/rules.

---

## Maintenance

- Required live files: `facts-shared.md`, `rules-shared.md`, `facts-operations.md`, `rules-operations.md`, `MEMORY-INDEX.md`
- Missing software-build or incident-response memory files is **not** an error
- Quarterly: `py -3 .cursor/skills/memory-optimize/scripts/analyze-memory.py facts`
- After new topics: update MEMORY-INDEX.md
