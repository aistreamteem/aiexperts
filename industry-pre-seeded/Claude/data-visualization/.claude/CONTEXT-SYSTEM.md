# Active Context System

## Purpose

Tracks the active **Work Item** (one chart pack: question + source file + outputs) for this data-visualization role.

## Context File

- **Location:** `.claude/active-context.txt`
- **Format:** `<type>:<id>`
- **Examples:**
  - `work-item:WID-654321`
  - `work-item:2026-11-08-sales-by-week`

## Context Types

### work-item

- **Purpose:** One chart pack (describe, bars, histogram, line, scatter, small multiples, missing/outliers, or refresh)
- **ID Format:** `WID-XXXXXXXX` or a dated slug
- **Root Path:** `work-items/<id>/`
- **Folders:** `in/`, `work/`, `out/`, `evidence/`, `facts/`
- **Journal:** `journals/work-items/<id>/progress.md`
- **Branch map:** `journals/work-items/<id>/state.json`
- **Workflows:** registered jobs in `.claude/workflows/workflow-registry.json` (default `describe-csv`)
- **Method:** `docs/role/work-item-method.md`

## Switching Context

User commands:

- `switch to work item WID-12345678` → writes `work-item:WID-12345678`
- `switch to 2026-11-08-sales-by-week` → same, pack slug

The agent will:

1. Parse the context file to determine type and ID
2. Route to `work-items/<id>/` and `journals/work-items/<id>/`
3. Load shared + operations memory plus that Work Item’s facts/rules

## Backward Compatibility

**Legacy file:** `.claude/active-work-item.txt` (id only)

## Skill Integration

Skills that read context:

- **continue:** next ready step of the selected chart workflow
- **workflow-selector:** writes context when starting a pack
- **journal-keeper:** Work Item journal path
- **remember / promote-facts-rules / switch-context / operator-qa**

All skills should:

1. Read `.claude/active-context.txt`
2. Parse `type:id`
3. Route `work-item` → `work-items/<id>/` and `journals/work-items/<id>/progress.md`

Live journal paths are under `journals/work-items/<id>/` only. Do not write a legacy `work-items/<id>/journal/` tree.

## Context Parsing Logic

```
Read .claude/active-context.txt
If file doesn't exist:
- Check .claude/active-work-item.txt (legacy read fallback only)
- If exists: type=work-item, id=content
- If not exists: prompt to start a Work Item (workflow-selector)
Parse content as `type:id`
Set root_path = work-items/{id}/
Set journal_path = journals/work-items/{id}/progress.md
```

Do not write `.claude/active-work-item.txt`; keep reading it only for old copies.

## Example Usage

**Starting a pack:**

```
User: "Here is this week’s sales export. Bar chart of sales by location."
Agent: workflow-selector → work-item:2026-11-08-sales-by-location
       writes .claude/active-context.txt
```

**Switching packs:**

```
User: "switch to work item WID-654321"
Agent: reads current context, confirms, writes work-item:WID-654321
```
