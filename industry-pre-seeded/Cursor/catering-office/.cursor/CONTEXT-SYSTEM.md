# Active Context System

## Purpose

Tracks which **Work Item** (catering event, week board, or named pack) is active.

## Context File

- **Location:** `.cursor/active-context.txt`
- **Format:** `<type>:<id>`
- **Examples:**
  - `work-item:WID-654321` (catering role job)

## Context Types

### work-item

- **Purpose:** One event, one week, or one named pack (pack-out, count versus guarantee, leftover-form completeness, …)
- **ID Format:** `WID-XXXXXXXX`
- **Root Path:** `work-items/<id>/`
- **Journal:** `journals/work-items/<id>/progress.md`
- **Branch map:** `journals/work-items/<id>/state.json`
- **Workflows:** registered catering jobs in `.cursor/workflows/workflow-registry.json`

## Switching Context

User commands:
- `switch to work item WID-12345678` → writes `work-item:WID-12345678`

The agent will:
1. Parse the context file to determine type and ID
2. Route to `work-items/<id>/` and `journals/work-items/<id>/`
3. Load operations memory and the selected catering workflow

## Backward Compatibility

**Legacy file:** `.cursor/active-work-item.txt`

## Skill Integration

Skills that read context:
- **continue:** Reads context to determine next catering-job step
- **workflow-selector:** Writes context when starting new work
- **journal-keeper:** Reads context for journal path
- **switch-context:** Changes the active Work Item
- **remember / promote-facts-rules / operator-qa:** Use the active Work Item paths

All skills should:
1. Read `.cursor/active-context.txt`
2. Parse format: `type:id`
3. Route based on type:
   - `work-item` → `work-items/<id>/` with journal under `journals/work-items/<id>/`

## Context Parsing Logic

```
Read .cursor/active-context.txt
If file doesn't exist:
- Check .cursor/active-work-item.txt (legacy)
- If exists: type=work-item, id=content
- If not exists: prompt user (workflow-selector) to start new work
Parse content as `type:id`
Set context_type = type (work-item)
Set context_id = id
Set root_path = work-items/{id}/
Set journal_path = journals/work-items/{id}/progress.md
```

## Example Usage

```
**Starting new work item:**
User: "start a pack-out for Saturday Acme lunch"
Agent: workflow-selector → writes `work-item:WID-123456` to `.cursor/active-context.txt`
```

**Switching contexts:**

```
User: "switch to work item WID-654321"
Agent: reads current context, writes new context, confirms switch
```

## Benefits

- Single source of truth for active context
- One event / week / pack per Work Item
- Journals stay under `journals/work-items/<id>/`
