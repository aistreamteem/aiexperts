# Active Context System

## Purpose

Tracks the active **Work Item** (trade shop pack: daily board, quote-to-job, permit file, truck load, closeout photos, and the other registered jobs).

## Context File

- **Location:** `.claude/active-context.txt`
- **Format:** `<type>:<id>`
- **Example:** `work-item:WID-654321`

## Context Types

### work-item

- **Purpose:** One trade job pack (one ticket, sold estimate, crew day, permit pack, or callback)
- **ID Format:** `WID-XXXXXXXX` or a shop pack id they named
- **Root Path:** `work-items/<id>/`
- **Folders:** `in/`, `work/`, `out/`, `evidence/`
- **Journal:** `journals/work-items/<id>/progress.md` (item-wide), `state.json` (branch map), `nodes/<leaf>.md` (step notes)
- **Workflows:** registry jobs in `.claude/workflows/workflow-registry.json`

Method: `docs/role/work-item-method.md`.

## Switching Context

User: `switch to work item WID-12345678` → writes `work-item:WID-12345678`

The agent:

1. Parse the context file
2. Route to `work-items/<id>/`
3. Load that journal, shared memory, and the selected job instruction file

## Backward Compatibility

**Legacy file:** `.claude/active-work-item.txt` — read as a fallback only. Do not write it.

## Skill Integration

Skills that read context: **continue**, **workflow-selector**, **journal-keeper**, **switch-context**, **remember**.

All of them:

1. Read `.claude/active-context.txt`
2. Parse `type:id`
3. Route `work-item` → `work-items/<id>/`

## Context Parsing Logic

```
Read .claude/active-context.txt
If missing:
  Check .claude/active-work-item.txt (legacy read fallback)
  If exists: type=work-item, id=content
  Else: prompt for a Work Item / job pack
Parse type:id
root_path = work-items/<id>/
journal_path = journals/work-items/<id>/progress.md
```
