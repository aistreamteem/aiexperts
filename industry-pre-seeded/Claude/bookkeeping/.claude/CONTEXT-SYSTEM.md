# Active Context System

## Purpose

Tracks the bookkeeping Work Item (period, rec, or pack) currently in progress.

## Context File

- **Location:** `.claude/active-context.txt`
- **Format:** `<type>:<id>`
- **Example:** `work-item:WID-20260801` or `work-item:2026-08-operating-bank-rec`

## Context Types

### work-item

- **Purpose:** One books period, account rec, card statement, 1099 year, or close pack
- **ID Format:** `WID-XXXXXXXX` or a filesystem-safe pack name
- **Root Path:** `work-items/<id>/`
- **Folders:** `in/`, `work/`, `out/`, `evidence/`, `facts/`
- **Journal:** `journals/work-items/<id>/progress.md` for item-wide fields, `state.json` for the branch map, and `nodes/<active leaf>.md` for step notes
- **Workflows:** registered bookkeeping jobs in `.claude/workflows/workflow-registry.json`

## Switching Context

User: `switch to work item WID-12345678` → writes `work-item:WID-12345678`

The agent:

1. Parses the context file
2. Routes to `work-items/<id>/`
3. Loads that journal, shared + operations memory, and the selected workflow

## Backward Compatibility

**Legacy file:** `.claude/active-work-item.txt` — read as a fallback only. Do not write it.

## Skill Integration

Skills that read context:

- **continue:** next ready workflow step
- **workflow-selector:** writes context when starting a pack
- **journal-keeper:** journal paths
- **switch-context:** changes the pointer
- **remember / promote-facts-rules / operator-qa:** Work Item vs expert memory

All skills should:

1. Read `.claude/active-context.txt`
2. Parse `type:id`
3. Route `work-item` → `work-items/<id>/` for artifacts and `journals/work-items/<id>/` for the journal

If the file is missing, check `.claude/active-work-item.txt`; if that is missing, prompt for a Work Item / pack name.

## Example

Starting August month-end: write `work-item:2026-08-month-end`, copy `work-items/_TEMPLATE/`, run **workflow-selector** (default `month-end`), put statements in `in/`.
