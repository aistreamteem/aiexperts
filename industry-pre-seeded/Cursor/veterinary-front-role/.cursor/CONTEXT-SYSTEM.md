# Active Context System

## Purpose

Tracks which **Work Item** this veterinary front-role expert is on (clinic day, records pack, estimate, boarding drop-off, and similar).

## Context File

- **Location:** `.cursor/active-context.txt`
- **Format:** `<type>:<id>`
- **Examples:**
  - `work-item:WID-654321`
  - `work-item:2026-11-10-day-book`

## Context Types

### work-item

- **Purpose:** One veterinary-role job pack (day appointments, emergency flag, new-client forms, records, reminders, estimate, checkout, boarding)
- **ID Format:** `WID-XXXXXXXX` or a dated pack name
- **Root Path:** `work-items/<id>/`
- **Journal:** `journals/work-items/<id>/progress.md`
- **Pointer (do not write notes):** `journals/work-items/<id>/progress.md`
- **Workflows:** registered jobs in `.cursor/workflows/workflow-registry.json`
- **Method:** `docs/role/work-item-method.md`

## Switching Context

User commands:
- `switch to work item WID-12345678` → writes `work-item:WID-12345678`

The agent will:
1. Parse the context file to determine type and ID
2. Route to `work-items/<id>/`
3. Load the Work Item journal, shared memory, and the selected role job

## Backward Compatibility

**Legacy file:** `.cursor/active-work-item.txt`

## Skill Integration

Skills that read context:
- **continue:** Reads context to determine next map step
- **workflow-selector:** Writes context when starting new work
- **journal-keeper:** Reads context for journal path
- **switch-context:** Changes the active Work Item
- **remember / promote-facts-rules / operator-qa:** Scope captures to the active Work Item or Expert Role

All skills should:
1. Read `.cursor/active-context.txt`
2. Parse format: `type:id`
3. Route `work-item` → `work-items/<id>/`

## Context Parsing Logic

```
Read .cursor/active-context.txt
If file doesn't exist:
- Check .cursor/active-work-item.txt (legacy)
- If exists: type=work-item, id=content
- If not exists: prompt to start a new Work Item
Parse content as `type:id`
Set root_path = work-items/{id}/
Set journal_path = journals/work-items/{id}/progress.md
```

## Example Usage

```
**Starting a day book:**
User: "start new work item 2026-11-10-day-book"
Agent: writes `work-item:2026-11-10-day-book` to `.cursor/active-context.txt`
```
