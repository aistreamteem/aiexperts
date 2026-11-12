# How Memory Loading Works

**Question**: How does the agent know where to look first for facts and rules?

**Answer**: Load the index, then this gym role's operations pair, then the active Work Item files.

---

## Discovery process

### Step 1: Load navigation index (always first)

**File**: `facts/MEMORY-INDEX.md`

Small routing table. Always load before operations files.

### Step 2: Determine workflow context

| Session type | Directory | Workflow | Memory files |
| --- | --- | --- | --- |
| **Gym role Work Item** | `work-items/<id>/` | selected registry job (`check-in-day`, …) | `facts-operations.md` + `rules-operations.md` |

Detection:

1. Read `.cursor/active-context.txt` (legacy `.cursor/active-work-item.txt` is read-only fallback)
2. Read `journals/work-items/<id>/progress.md` for **Workflow type**
3. Default to **check-in-day** (typical daily job) if a Work Item exists but the job is unset — then run **workflow-selector**
4. Do **not** default to a software-build or production-incident workflow

### Step 3: Load operations files only

```
1. Load MEMORY-INDEX.md
2. Detect work-items/<id> → gym role operations
3. Load facts-operations.md + rules-operations.md
4. Load work-items/<id>/facts/facts.md + rules.md when present
```

### Step 4: On-demand tools and workflows

Load `docs/tools/<name>.md` and `.cursor/workflows/<job>.md` when the selected step cites them. Do not load every tool up front.

---

## Routing logic

```
IF session is a Work Item under work-items/
  → workflow = journal "Workflow type" or check-in-day after selector
  → load facts-operations.md + rules-operations.md
ELSE
  → check active context file
  → if still ambiguous, ask which role job; do not assume a developer pipeline
```

Entries with `**Workflows:** all` apply to every role job. Entries tagged with a job id apply when that job is selected.

---

## Why this approach works

This role is one role. Splitting memory into developer / incident files would hide the membership and check-in notes. Growth stays in the operations pair. Use **memory-optimize** when those files bloat.

---

## Configuration

Documented in `AGENTS.md`: at start of each session or skill, load MEMORY-INDEX first, then operations facts/rules, then Work Item memory. See MEMORY-INDEX.md.

## Memory system files

### Always load first

- **MEMORY-INDEX.md** — navigation

### Role memory (this role)

- **facts-operations.md** — check-in, waivers, freeze/cancel, PT, classes, retail
- **rules-operations.md** — never invent dues, no medical/diet, no EFT, one Work Item one folder

### Maintenance

Run a **memory-optimize** metrics pass to verify operations files stay usable. Regenerate the trigger index after retagging rules: `python scripts/memory/build_trigger_index.py`.
