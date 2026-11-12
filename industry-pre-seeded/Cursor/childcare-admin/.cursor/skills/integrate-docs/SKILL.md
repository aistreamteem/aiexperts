---
name: integrate-docs
description: "Use when the user provides documentation, notes, handbook pages, licensing checklists, or exports to integrate into operations facts, rules, and MyRole.txt."
---

# integrate-docs

**Purpose:** Integrate documentation into this childcare-office Expert (facts, rules, role definition).

**When to use:** Operator provides a handbook PDF, licensing visit checklist, tuition policy page, export legend, or similar.

**Outputs:**
- New facts/rules in the shared pair (`Workflows: all`) or operations pair (named job)
- Optional reference doc `facts/<topic>.md` with a `MEMORY-INDEX.md` pointer for large checklists
- `MyRole.txt` / `docs/role/work-item-method.md` only if a new repeating job is confirmed
- Summary of what was integrated

> **Memory model:** Shared + operations. Do not invent software-build or incident-response memory files.

## Behavior

### 1. Gather documents

Ask for path(s) and whether the content is primarily facts (how they file) or rules (never / always).

### 2. Analyze

**Facts:** room names, export headers, which calendar is live, packet page list, posted ratio chart location, tuition codes.

**Rules:** never release a child, ask on pickup mismatch, handbook wins, no invented tuition, present-or-missing immunizations, incidents to director.

**Role updates:** a new repeating job worth a registered workflow.

### 3. Classify and confirm

Present counts by topic (enrollment, attendance, pickup, tuition, licensing, incidents). Ask which workflows apply; default `all`. For rules, ask Triggers (`write:doc`, `write:csv`, or `none`).

### 4. Format and route

Use heading `### YYYY-MM-DD: Title`. Include `**Triggers:**` on every rule. Route `Workflows: all` to `facts/facts-shared.md` / `facts/rules-shared.md`; a registered job id to the operations pair. Check for duplicates/conflicts. Ask before overwriting a starter guess they have not confirmed.

### 5. Summary

List files touched. Do not modify Work Item facts/rules here — use **remember** during an active job.

### 6. Regenerate the trigger index

After any rule whose Triggers is not `none`, run `python scripts/memory/build_trigger_index.py`.

## Complements

- **remember**: one fact/rule during a job
- **promote-facts-rules**: elevate Work Item notes after a pack

## Example

Handbook illness page → fact quoting *their* exclusion wording + rule "do not invent exclusion days". Forward action: use in attendance-day when illness wording appears.
