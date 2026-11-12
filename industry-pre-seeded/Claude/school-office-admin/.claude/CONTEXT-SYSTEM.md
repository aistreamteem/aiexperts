# Active Context System

## Purpose

Tracks which **Work Item** (school-office role job) is active.

## Context File

- **Location:** `.claude/active-context.txt`
- **Format:** `<type>:<id>`
- **Examples:**
  - `work-item:WID-20261108` (today’s attendance, an enrollment packet, a records request)

## Context Types

### work-item

- **Purpose:** One isolated school-office admin job
- **ID Format:** `WID-XXXXXXXX`
- **Root Path:** `work-items/<id>/` (artifacts: `in/`, `work/`, `out/`, `evidence/`, `STATUS.md`, facts)
- **Journals:** `journals/work-items/<id>/progress.md` (flat item-wide fields), `journals/work-items/<id>/state.json` (branch map), `journals/work-items/<id>/nodes/` (step notes)
- **Agent notes:** `journals/work-items/<id>/agent-notes/`
- **Workflows:** registered role jobs in `.claude/workflows/workflow-registry.json`

## Switching Context

User commands:
- `switch to work item WID-12345678` → writes `work-item:WID-12345678`

The agent will:
1. Parse the context file to determine type and ID
2. Route to `work-items/<id>/`
3. Load the Work Item journal, shared memory, and the selected workflow file

## Backward Compatibility

**Legacy file:** `.claude/active-work-item.txt` — read fallback only. Do not write it.

## Skill Integration

Skills that read context:
- **continue** — next ready work-map step
- **workflow-selector** — writes context when starting new work
- **journal-keeper** — journal paths
- **remember** / **promote-facts-rules** / **switch-context**

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
- If not exists: prompt user to start a new Work Item
Parse content as `type:id`
Set root_path = work-items/{id}/
Set journal_path = journals/work-items/{id}/progress.md
Set map_path = journals/work-items/{id}/state.json
```

## Example Usage

```
**Starting a new attendance-day job:**
User: "start new work item WID-20261108"
Agent: writes `work-item:WID-20261108` to `.claude/active-context.txt`
```
