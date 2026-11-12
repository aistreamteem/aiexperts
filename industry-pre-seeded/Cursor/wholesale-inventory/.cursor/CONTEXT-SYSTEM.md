# Active Context System

## Purpose

Tracks the inventory Work Item (receipt, count, pick, transfer, RMA, or reorder) currently in progress.

## Context File

- **Location:** `.cursor/active-context.txt`
- **Format:** `<type>:<id>`
- **Example:** `work-item:WID-20261108` or `work-item:2026-11-08-receiving-po-9021`

## Context Types

### work-item

- **Purpose:** One receipt, count date, pick, transfer, RMA, or reorder pull
- **ID Format:** `WID-XXXXXXXX` or a filesystem-safe short name
- **Root Path:** `work-items/<id>/`
- **Folders:** `in/`, `work/`, `out/`, `evidence/`, `facts/`
- **Journal:** `journals/work-items/<id>/progress.md` (item-wide), `state.json` (branch map), `nodes/<leaf>.md` (step notes)
- **Workflows:** registered inventory jobs in `.cursor/workflows/workflow-registry.json`

## Switching Context

User: `switch to work item WID-12345678` → writes `work-item:WID-12345678`

The agent:

1. Parses the context file
2. Routes to `work-items/<id>/`
3. Loads that journal, shared + operations memory, and the selected workflow

## Backward Compatibility

**Legacy file:** `.cursor/active-work-item.txt` — read fallback only. Do not write it.

## Skill Integration

Skills that read context:

- **continue:** next ready workflow step
- **workflow-selector:** writes context when starting a job
- **journal-keeper:** journal paths
- **switch-context:** changes the pointer
- **remember / promote-facts-rules / operator-qa:** Work Item vs expert memory

All skills should:

1. Read `.cursor/active-context.txt`
2. Parse `type:id`
3. Route `work-item` → `work-items/<id>/`

If the file is missing, check `.cursor/active-work-item.txt`; if that is missing, prompt for a Work Item / short name.

## Example

Starting receiving for PO-9021: write `work-item:2026-11-08-receiving-po-9021`, copy `work-items/_TEMPLATE/`, run **workflow-selector** (default `receiving-match`), put the PO PDF and dock count in `in/`.
