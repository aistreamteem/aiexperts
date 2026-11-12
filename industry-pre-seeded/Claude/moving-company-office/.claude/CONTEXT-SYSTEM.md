# Active Context System

## Purpose

Tracks the active **Work Item** for this moving-company office role (one estimate, move, day list, or claim pack at a time).

## Context File

- **Location:** `.claude/active-context.txt`
- **Format:** `<type>:<id>`
- **Examples:**
  - `work-item:WID-654321`
  - `work-item:2026-09-15-est-9021`

## Context Types

### work-item

- **Purpose:** One move file or pack (estimate, inventory, crew day, truck calendar, weigh tickets, claims)
- **ID Format:** `WID-XXXXXXXX` or a shop folder name (`YYYY-MM-DD-est-…`)
- **Root Path:** `work-items/<id>/`
- **Journal:** `journals/work-items/<id>/progress.md` (item-wide fields), `state.json` (branch map), `nodes/<leaf>.md` (step notes)
- **Workflows:** registered jobs in `.claude/workflows/workflow-registry.json` (default `estimate-from-rate-file`)
- **Method:** `docs/role/work-item-method.md`

## Switching Context

User commands:

- `switch to work item WID-12345678`
- `switch to 2026-09-15-est-9021`

The agent will:

1. Parse the context file to determine type and ID
2. Route to `work-items/<id>/`
3. Load that Work Item journal, shared + operations memory, and the selected workflow file

## Backward Compatibility

**Legacy file (read only):** `.claude/active-work-item.txt` — do not write it; new work uses `.claude/active-context.txt` only.

## Skill Integration

Skills that read context:

- **continue** — next ready step on the selected workflow
- **workflow-selector** — writes context when starting a job
- **journal-keeper** — Work Item journal path
- **remember** / **switch-context** / **operator-qa**

All skills should:

1. Read `.claude/active-context.txt`
2. Parse `type:id`
3. Route `work-item` → `work-items/<id>/`

## Context Parsing Logic

```
Read .claude/active-context.txt
If file doesn't exist:
- Check .claude/active-work-item.txt (legacy read fallback)
- If exists: type=work-item, id=content
- If not exists: prompt for a move / estimate / pack id
Parse content as `type:id`
Set root_path = work-items/{id}/
Set journal_path = journals/work-items/{id}/progress.md
```

Do not use a top-level `items/` tree or `journal/state.json` as the live job root.
