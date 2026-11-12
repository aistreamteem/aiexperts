# Expert — skill design

**Updated:** 2026-11-08  
**Folder:** Purchasing / buyer (small manufacturer or shop) role Expert.

This expert keeps the **universal expert architecture** (journals, Work Items, operations memory, registered workflows) and **role content** for a buyer role. It does **not** run a software SDLC (HLD/DD/implement) and it does **not** keep a parallel old-seed process-skill layer.

Use ordinary words with the person. Finished work is a **pack** under the current Work Item (`out/` plus a short write-up). Look in saved files before starting. Think in **parts**: requisition, AVL, quote, PO draft, receiving, match exception. Do not invent missing shop practice. Multi-step work is a **work map** in `.claude/workflows/`: steps with **needs**, **produces**, and a **check**. A step is done only when the check exits 0.

See `docs/role/work-item-method.md` for the purchasing phases.

## Canonical expert skills (keep)

| Skill | Role in this role |
| --- | --- |
| **continue** | Resume from journals + active Work Item. One ready workflow step. Continue is not a yes. |
| **define-role** | First-run role interview if `MyRole.txt` is still pending. |
| **journal-keeper** | Expert journal + Work Item journal/state/nodes. No parallel role-root journal machine. |
| **remember** | Facts/rules into shared or operations memory, or the Work Item `facts/` folder. |
| **workflow-selector** | Registered buyer jobs only (AVL check, RFQ, quote/lead/MOQ, open POs, backorder, blanket, change order, receiving shorts, match). |
| **operator-qa** | Clarify authorization, AVL, price file, receiving difference before acting or remembering. |
| **promote-facts-rules** | Elevate job-specific learnings into operations memory. |
| **switch-context** | Change active Work Item. |
| **integrate-docs** | Fold operator notes/docs into operations memory. |
| **memory-optimize** | Health check on operations memory files. |
| **visual-page** | Optional visual of an open-PO list, match legs, or short pack beside chat. |
| **spec-parser** | Parse a requirements/spec into the Work Item journal when that workflow applies. |
| **scaffold-project** | Create the project skeleton after approved design when scaffolding applies. |
| **implement-feature** | Implement one TODOS task when the journal next action calls for it. |
| **iterative-feature** | Requirements → design → implement → test for iterative changes. |
| **refactor** | Reduce duplication / tech debt while keeping tests green. |
| **diagram-generator** | Regenerate or sync design diagrams with design docs when needed. |

## Not used (removed)

Old role process glue is not part of this Expert. Canonical platform skills from the base expert (including pipeline skills) are kept. Their behavior lives in:

- Starting work → **workflow-selector** + `work-items/<id>/` + **continue**
- Stepping a job → the workflow file + **journal-keeper**
- Checks / gates → steps inside the workflow file + **operator-qa**
- Pack / evidence → Work Item `out/` / `evidence/` + journal STATUS
- Scope / refuse / conflict → `MyRole.txt` + `facts/rules-operations.md` + `.claude/rules/expert.md`
- Tools → `docs/tools/` cited from the workflow file

## Layout

- Role: `MyRole.txt`, `docs/role/work-item-method.md`
- Root instructions: `CLAUDE.md`, `.claude/rules/expert.md`
- Memory: `facts/facts-shared.md`, `facts/rules-shared.md`, `facts/facts-operations.md`, `facts/rules-operations.md`, `facts/MEMORY-INDEX.md`
- Jobs: `.claude/workflows/` + `workflow-registry.json`
- Work: `work-items/<id>/{in,work,out,evidence}`
- Journals: `journals/expert/`, `journals/work-items/<id>/`
