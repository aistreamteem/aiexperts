---
name: continue
description: >-
  Resume from journals/expert/progress.md and the active Work Item journal when
  they say continue, resume, or start. Continue is not a yes and not an answer.
  Walks one ready step of the selected purchasing workflow.
---

# Continue

Resume this **purchasing / buyer** role from the journals. Use when the operator says continue, start, or resume. Continue is not approval of a gate and not an answer to an open question.

## When to use

- Operator says "continue", "start", or "resume"
- Operator asks to pick up a PO, AVL, RFQ, match, or other purchasing pack
- When the next action waits for an answer or approval, "continue" means re-prompt, not "they answered"

## Do

**Do not** treat "continue" as an answer or as approval/waiver. If the next action waits, ask again and do not advance until they give a substantive answer or an explicit approval/waiver.

### Role gate

0. Read `MyRole.txt`.
   - If they said "define my role", run **define-role** and stop.
   - If `Role status` is `pending` or missing, run **define-role** and stop. Do not ask for a Work Item ID.
   - If `defined` or `skipped`, go to 0a.

### Context

0a. Read `.cursor/active-context.txt` (`work-item:<id>`). If missing, check `.cursor/active-work-item.txt` (legacy read fallback). If both missing, ask: "Which purchasing job should we open? Give a Work Item id (WID-…) or a PO/pack name (for example 2026-09-15-po-4412)." Write the chosen id only to `.cursor/active-context.txt` as `work-item:<id>` (do not write the legacy pointer).

0b. Paths:
   - `root_path` = `work-items/<id>/`
   - `journal_path` = `journals/work-items/<id>/progress.md`
   - `map_path` = `journals/work-items/<id>/state.json`
   - Node notes: `journals/work-items/<id>/nodes/<active leaf>.md`
   - Background notes: `journals/work-items/<id>/agent-notes/` (merged by the stop hook)

0c. If `root_path` does not exist, copy `work-items/_TEMPLATE/` there. If `journals/work-items/<id>/` does not exist, copy `journals/work-items/_TEMPLATE/` and set **Work item record** to `work-items/<id>/`. Set `Current work item:` in `journals/expert/progress.md` (copy `journals/_TEMPLATE/expert/progress.md` first if needed).

0d. Load workflow:
   - Read **Workflow type** on `journal_path`. If missing, run **workflow-selector**, then reload.
   - Read `.cursor/workflows/workflow-registry.json` and load `.cursor/workflows/<workflow-type>.md`.
   - Method note: `docs/role/work-item-method.md`.

0e. Load memory:
   - `facts/MEMORY-INDEX.md`
   - `facts/facts-shared.md` and `facts/rules-shared.md` (always)
   - `facts/facts-operations.md` and `facts/rules-operations.md` (filter `**Workflows:**` to this job or `all`)
   - `work-items/<id>/facts/facts.md` and `.../rules.md` when present
   - Follow every matching rule. Log conflicts in the journal.

### Execute one ready step

1. Read `journal_path` and the active node under `journals/work-items/<id>/nodes/`.
2. If Open questions (blocking) is non-empty, ask those questions and stop. Continue is not an answer.
3. If Blockers / Last failure is set, describe the block and wait for agreement. Do not skip or invent a pass.
4. If next action waits for operator approval (authorization, AVL add, close-short, change order, treating a PO as issued), re-prompt. Do not treat continue as approval.
5. If next action is empty or done, ask what they want next.
6. Otherwise perform **one ready step** from the loaded workflow file (or the whole named job if they asked):
   - Put source files in `work-items/<id>/in/`.
   - Paths `work/` and `out/` in the map mean inside this Work Item.
   - Do not start a step whose `needs` files are missing — ask for the export or file.
   - Read the cited `docs/tools/` file. Write `produce_path`. Run the `check`. Copy logs to `evidence/`.
   - On check fail: retry at most three times from the tool doc, then record the blocker and ask.
   - Do not invent unit prices, freight, or discounts. Do not hide receiving shorts.
7. **journal-keeper**: what ran, artifacts, check result, next action.
8. At session end, write Last session summary on the Work Item journal and refresh `STATUS.md`.
9. When the Work Item is done, offer **promote-facts-rules**.

Registered jobs: avl-check, rfq-from-files, quote-lead-moq, open-pos, backorder-list, blanket-release, change-order-pack, receiving-shorts, match.
