# Active Context System

## Purpose

Tracks which **Work Item** this dental front-role expert is on (clinic day, claim pack, recall export, and similar).

## Context File

- **Location:** `.claude/active-context.txt`
- **Format:** `<type>:<id>`
- **Examples:**
  - `work-item:WID-654321`
  - `work-item:2026-11-10-day-list`

## Context Types

### work-item

- **Purpose:** One dental-role job pack (day list, forms check, claims fields, recall, day close, …)
- **ID Format:** `WID-XXXXXXXX` or a dated pack name
- **Root Path:** `work-items/<id>/`
- **Journal:** `journals/work-items/<id>/progress.md`
- **Branch map:** `journals/work-items/<id>/state.json`
- **Node notes:** `journals/work-items/<id>/nodes/`
- **Workflows:** registered jobs in `.claude/workflows/workflow-registry.json`
- **Method:** `docs/role/work-item-method.md`

## Switching Context

User commands:
- `switch to work item WID-12345678` → writes `work-item:WID-12345678`

The agent will:
1. Parse the context file to determine type and ID
2. Route to `work-items/<id>/`
3. Load the Work Item journal, operations memory, and the selected role job

## Backward Compatibility

**Legacy file:** `.claude/active-work-item.txt` — read fallback only. Skills must not write it.

## Skill Integration

Skills that read context:
- **continue:** Reads context to determine next map step
- **workflow-selector:** Writes context when starting new work
- **journal-keeper:** Reads context for journal path
- **switch-context:** Changes the active Work Item
- **remember / promote-facts-rules / operator-qa:** Scope captures to the active Work Item or Expert Role

All skills should:
1. Read `.claude/active-context.txt`
2. Parse format: `type:id`
3. Route `work-item` → `work-items/<id>/` and `journals/work-items/<id>/`

## Context Parsing Logic

```
Read .claude/active-context.txt
If file doesn't exist:
- Check .claude/active-work-item.txt (legacy read fallback)
- If exists: type=work-item, id=content
- If not exists: prompt to start a new Work Item
Parse content as `type:id`
Set root_path = work-items/{id}/
Set journal_path = journals/work-items/{id}/progress.md
Set map_path = journals/work-items/{id}/state.json
```

## Example Usage

```
**Starting a day list:**
User: "start new work item 2026-11-10-day-list"
Agent: writes `work-item:2026-11-10-day-list` to `.claude/active-context.txt`
```
