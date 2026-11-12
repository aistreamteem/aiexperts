# How Memory Loading Works

**Question:** How does the agent know where to look first for facts and rules?

**Answer:** Load the index, then the **shared** pair, then this role’s **operations** pair. Work Items use the visualization method in `docs/role/work-item-method.md`. Default job is `describe-csv`.

---

## Discovery Process

### Step 1: Load Navigation Index (Always First)

**File:** `facts/MEMORY-INDEX.md`

### Step 2: Determine Workflow Context

| Session Type | Directory Pattern | Memory Files to Load |
| --- | --- | --- |
| **Chart pack (Work Item)** | `work-items/<id>/` | shared + operations (+ Work Item facts/rules) |
| **Q&A session** | `qa-sessions/Q*` | shared + operations |

**Detection:**

1. Read `.claude/active-context.txt` (legacy read fallback: `.claude/active-work-item.txt`)
2. Read `journals/work-items/<id>/progress.md` for **Workflow type**
3. If still ambiguous, default to **`describe-csv`**

### Step 3: Load Files

```
1. Load MEMORY-INDEX.md
2. Load facts-shared.md + rules-shared.md
3. Load facts-operations.md + rules-operations.md
4. Load work-items/<id>/facts/ when present
```

Do not invent developer or incident-response memory files for this role.

### Step 4: On-Demand Reference Materials

Large tool docs under `docs/tools/` load only when the current workflow step names them. Workflow instruction files under `.claude/workflows/` load when that job is selected.

---

## Routing

- `Workflows: all` → shared pair
- Registered chart-job id → operations pair
- Work Item scope → `work-items/<id>/facts/`

## Maintenance

Run **memory-optimize** `--metrics` when memory files grow quickly. Thresholds: warn >1,500 lines per file.
