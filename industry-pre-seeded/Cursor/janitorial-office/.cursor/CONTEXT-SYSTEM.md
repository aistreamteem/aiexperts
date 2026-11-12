# Active Context System

## Purpose

Tracks the active **Work Item** on this janitorial / contract-cleaning office role (site-night, callback pack, supply week, key closeout, and similar).

## Context File

- **Location:** `.cursor/active-context.txt`
- **Format:** `<type>:<id>`
- **Examples:**
  - `work-item:WID-654321`
  - `work-item:2026-09-15-clinic-night`

## Context Types

### work-item

- **Purpose:** One role pack (night board, quality walk, complaint list, …)
- **ID Format:** `WID-XXXXXXXX` or a shop pack name (`YYYY-MM-DD-site`)
- **Root Path:** `work-items/<id>/`
- **Journal:** `journals/work-items/<id>/progress.md` (flat journal), `state.json` (branch map), `nodes/` (step notes). Artifacts live under `work-items/<id>/`.
- **Workflows:** registered jobs in `.cursor/workflows/workflow-registry.json` (`night-board`, `complaint-callback`, `quality-checklist-pack`, …)

## Switching Context

User commands:

- `switch to work item WID-12345678`
- `switch to 2026-09-15-clinic-night`

The agent will:

1. Parse the context file
2. Route to `work-items/<id>/`
3. Load that Work Item journal and artifacts

## Backward Compatibility

**Legacy file:** `.cursor/active-work-item.txt` — read-only fallback when `active-context.txt` is missing. Do not write it.

## Skill Integration

Skills that read context: **continue**, **workflow-selector**, **journal-keeper**, **switch-context**, **remember**, **promote-facts-rules**.

All of those should:

1. Read `.cursor/active-context.txt`
2. Parse `type:id`
3. Route `work-item` → `work-items/<id>/`

## Context Parsing Logic

```
Read .cursor/active-context.txt
If file doesn't exist:
- Check .cursor/active-work-item.txt (legacy)
- If exists: type=work-item, id=content
- If not exists: prompt user to start a pack
Parse content as `type:id`
Set root_path = work-items/{id}/
Set journal_path = journals/work-items/{id}/progress.md
```

## Example Usage

**Starting a pack:**
User: "start work item 2026-09-15-clinic-night"
Agent: writes `work-item:2026-09-15-clinic-night` and runs workflow-selector if Workflow type is missing.

**Switching:**
User: "switch to work item WID-654321"
Agent: confirms, writes the new context, shows next action from that journal.
