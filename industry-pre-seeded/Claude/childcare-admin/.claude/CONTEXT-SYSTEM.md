# Active Context System

## Purpose

Tracks the active **Work Item** for this childcare center office Expert.

## Context File

- **Location:** `.claude/active-context.txt`
- **Format:** `<type>:<id>`
- **Examples:**
  - `work-item:WID-654321`
  - `work-item:2026-11-08-room-a-attendance`

## Context Types

### work-item

- **Purpose:** One office job (attendance date, child packet, tuition period, licensing pack, incident list, waitlist slice)
- **ID Format:** `WID-XXXXXXXX` or a job label (`YYYY-MM-DD-room-or-childid`)
- **Root Path:** `work-items/<id>/`
- **Journal:** `journals/work-items/<id>/progress.md` (item-wide), `nodes/<leaf>.md` (step notes), `agent-notes/` (background merges)
- **Branch map:** `journals/work-items/<id>/state.json`
- **Workflows:** registered role jobs in `.claude/workflows/workflow-registry.json` (default `attendance-day`)
- **Method:** `docs/role/work-item-method.md`

## Switching Context

User commands:

- `switch to work item WID-12345678`
- `switch to 2026-11-08-room-a-attendance`

The agent will:

1. Parse the context file
2. Route to `work-items/<id>/`
3. Load that journal, STATUS, and facts/rules

## Backward Compatibility

**Legacy read-only fallback:** `.claude/active-work-item.txt` (hooks and continue may read it; do not write it)

## Skill Integration

Skills that read context:

- **continue** — next ready work-map step
- **workflow-selector** — writes context when starting a job
- **journal-keeper** — journal paths
- **switch-context** — changes the pointer
- **remember** / **promote-facts-rules** — Work Item vs operations/shared memory

All skills should:

1. Read `.claude/active-context.txt`
2. Parse `type:id`
3. Route `work-item` → `work-items/<id>/` artifacts and `journals/work-items/<id>/` journal

Do not look for software-design skill paths or a deleted process-skill layer.

## Context Parsing Logic

```
Read .claude/active-context.txt
If file doesn't exist:
- Check .claude/active-work-item.txt (legacy read fallback)
- If exists: type=work-item, id=content
- If not exists: prompt to start a Work Item (workflow-selector)
Parse content as `type:id`
Set root_path = work-items/{id}/
Set journal_path = journals/work-items/{id}/progress.md
```

## Example Usage

```
User: "start attendance for Room A today"
Agent: writes work-item:2026-11-08-room-a-attendance
       selects attendance-day
```
