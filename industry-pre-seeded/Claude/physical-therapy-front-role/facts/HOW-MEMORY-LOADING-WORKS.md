# How Memory Loading Works

**Question:** How does the agent know where to look first for facts and rules?

**Answer:** This physical-therapy front-role expert loads **shared** then **operations** memory for every Work Item, then the active Work Item's own facts/rules.

---

## Discovery process

### Step 1: Load navigation index (always first)

**File:** `facts/MEMORY-INDEX.md`

Small routing table: which shared/operations files to load, which fact topics belong to which role job.

### Step 2: Determine workflow context

| Session type | Directory pattern | Workflow | Memory files |
| --- | --- | --- | --- |
| PT front-role Work Item | `work-items/WID-*` or named pack | registered job id (`day-list`, `auth-remaining-from-file`, …) | shared + operations pairs |

Detection:

1. Read `.claude/active-context.txt` (legacy `.claude/active-work-item.txt` fallback only)
2. Read the Work Item journal **Workflow type**
3. Default to shared + operations memory + job `auth-remaining-from-file` if the journal has no type yet (then run workflow-selector)

Do **not** default to a software-build or incident-response workflow. This role is not those jobs.

### Step 3: Load shared, operations, and Work Item files

```
1. MEMORY-INDEX.md
2. facts-shared.md + rules-shared.md
3. facts-operations.md + rules-operations.md
4. work-items/<id>/facts/facts.md + rules.md (if present)
```

Filter Expert Role entries by `**Workflows:**` (`all` or the current job id). Work Item entries are not filtered.

### Step 4: On-demand tools and workflow maps

Load `docs/tools/<name>.md` and `.claude/workflows/<job>.md` only for the selected job. Large PDFs in `in/` are read when the map step needs them.

---

## Why this approach

- Shared holds cross-cutting `Workflows: all` entries every loader path includes.
- Operations holds clinic day-to-day starter knowledge for this front role.
- Work Items isolate one clinic date or pack so Tuesday does not overwrite Monday.
- Split software-build vs incident files are not part of this seed.

## Maintenance

Run memory-optimize when shared/operations files grow quickly, after capturing many facts/rules, or when the operator asks for a health check. Thresholds: warn if a memory file exceeds ~1,500 lines or ~80 entries.

After adding or retagging a rule with a non-`none` trigger, regenerate `facts/trigger-index.json` with `python scripts/memory/build_trigger_index.py`.
