---
name: promote-facts-rules
description: Use when the user says "promote facts/rules", "summarize learnings", "elevate to expert level", or at Work Item completion. Reviews Work Item-level facts/rules and promotes selected ones to shared or operations memory.
trigger: User says "promote facts/rules", "summarize learnings", "elevate to expert level", or Work Item completion
---

# Promote Facts and Rules

### 0. Work Item context

- Active work item: the line in `.claude/active-context.txt`, formatted `work-item:<id>`.
- Artifacts (spec, docs, packs, evidence): `work-items/<id>/`.
- Journal: `journals/work-items/<id>/progress.md` for item-wide fields, `state.json` for the
  branch map, and `nodes/<active leaf>.md` for step notes, open questions, and the next action.
  Write through journal-keeper.

Reviews Work Item-level facts and rules and lets the operator promote shop learnings into Expert Role memory.

## When to use

- Operator says promote facts/rules, summarize learnings, or elevate to expert level
- Work Item reaches done and continue offers a promotion review

## Memory model

- `Workflows: all` → `facts/facts-shared.md` / `facts/rules-shared.md`
- Named registered job → `facts/facts-operations.md` / `facts/rules-operations.md`

Work Item files (`work-items/<id>/facts/facts.md`, `.../rules.md`) stay unsplit.

## Instructions

1. Read active Work Item ID from `.claude/active-context.txt` (legacy read fallback: `.claude/active-work-item.txt`).
2. Read `work-items/<id>/facts/facts.md` and `rules.md`.
3. List active (not already promoted) entries. For each, ask Yes / No / Skip.
4. On Yes:
   - Optional edit/generalize.
   - Workflow applicability: default current job (`avl-check`, `match`, …) or `all`.
   - Rules only: Triggers `write:csv` | `write:pack` | `write:doc` | `none`.
   - Append with `### YYYY-MM-DD: Title` header to the matching Expert Role file.
   - After a rule whose trigger is not `none`, run `py -3 scripts/memory/build_trigger_index.py`.
   - Mark the Work Item entry `promoted-to-expert` and record the decision in the journal.
5. Also present journal field “Proactively detected facts/rules”.
6. Summarize counts. Remind the operator to keep Expert Role memory files with the Expert folder.
7. If this pack followed a new repeating job, ask whether to add a workflow to `MyRole.txt` and the registry.

## Example

Work Item fact “Acme Fasteners LLC is the AVL name, not Acme” → promote to `facts/facts-operations.md` with Workflows `avl-check, match`.

Work Item rule “Never hide a short on PO 4412 inside received-in-full” → promote to `facts/rules-operations.md`, trigger `write:pack`.
