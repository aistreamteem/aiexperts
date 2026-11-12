---
name: workflow-selector
description: >-
  Use when the continue skill finds the journal missing a workflow type, or when
  starting a new Work Item. Reads the bakery-cafe workflow registry and prompts
  the operator to select a registered role job.
---

# Workflow Selector

Presents the bakery / cafe production-office job menu and records the selection in the Work Item journal.

## When to use

- Called by continue when the journal is missing "Workflow type"
- On new Work Item initialization

## Instructions

1. **Determine context type:**
 - Read `.claude/active-context.txt` to get `context_type` and `context_id`

2. **Read workflow registry:**
 - Read `.claude/workflows/workflow-registry.json`

3. **Present menu from the registry only:**

 List each workflow as a numbered line: name, then the description. Do not offer a job that is not in the registry.

 Until the operator picks another job, the default daily job is `bake-list-day`.

 Typical pairing:
 - Today’s oven plan → Bake List Day
 - Case looked empty / refill → Case Par Vs Count
 - Account crates today → Wholesale Day
 - Open decorated cakes → Custom Cake Board
 - Pie week / cookie week → Holiday Bake Up
 - Dock vs invoice fight → Receiving Shorts
 - Flour/butter/dairy hole → Ingredient Below Par
 - Unsold / day-old recap → Stale And Waste
 - Contains / sesame / nut matrix → Allergen Sheet Index

4. **Accept user input:** a number, a job id (`bake-list-day`), or a display name (`Bake List Day`).

5. **Validate** against the registry. If invalid, re-prompt.

6. **Ask:**
 - "What is the Work Item ID or pack name? (e.g., WID-21411151 or `2026-11-08-bake-list`)"
 - "Any files to use? (bake sheet, formula file, standing CSV, invoice PDFs, cake-order folder, allergen sheet, calendar)"

7. **Record in journal:**
 - Write `Workflow type` on `journals/work-items/<id>/progress.md` when that field is missing. Do not replace `active`.
 - Set `Context ID: <context_id>`
 - Put `Next action` on `nodes/work-item.md` only when `active` is still just `work-item`. If `active` is already deeper, leave it.
 - Next action should be the first step id of the selected workflow (see that file’s YAML), not a generic role-job token.

8. **Write active context file:**
 - `.claude/active-context.txt` as `<context_type>:<context_id>`
 - Do not write the legacy `.claude/active-work-item.txt`

9. **Confirm:**

 Work Item initialized with \<workflow-name>
 Initial phase: first step of that job (see the workflow file)
 Next action: walk that step with **continue** (read the tool doc, write the artifact under this Work Item, run the check, journal-keeper)

## Workflow-specific fields

- Job id (registry key)
- Current Work Item folder under `work-items/<id>/`
- Named source files they pointed at (bake sheet, standing CSV, and so on)
- No software-design or incident-bridge fields

## Notes

- Called by continue when journal is missing workflow type
- If an existing journal has "Pipeline" but no "Workflow type", map leftover software-design or generic operations labels to `bake-list-day` unless they name another registered job
