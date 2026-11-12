# Active Context System

## Purpose

Tracks the physical-therapy front-role Work Item (clinic date, remaining-visits pack, referral folder, or close) currently in progress.

## Context File

- **Location:** `.claude/active-context.txt`
- **Format:** `<type>:<id>`
- **Example:** `work-item:WID-20261108` or `work-item:2026-11-08-day-list`

## Context Types

### work-item

- **Purpose:** One clinic date, remaining-visits pack, referral/POC folder, recert pull, HEP print, no-show list, wait-list, visit-count check, or day-close
- **ID Format:** `WID-XXXXXXXX` or a filesystem-safe pack name
- **Root Path:** `work-items/<id>/`
- **Folders:** `in/`, `work/`, `out/`, `evidence/`, `facts/`
- **Journal:** `journals/work-items/<id>/progress.md` for item-wide fields, `state.json` for the branch map, and `nodes/<active leaf>.md` for step notes
- **Workflows:** registered front-role jobs in `.claude/workflows/workflow-registry.json`
- **Method:** `docs/role/work-item-method.md`

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

Starting Thursday’s day list: write `work-item:2026-11-08-day-list`, copy `work-items/_TEMPLATE/`, run **workflow-selector** (or confirm `day-list`), put the schedule export in `in/`.
