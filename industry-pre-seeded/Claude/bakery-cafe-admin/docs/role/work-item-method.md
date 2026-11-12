# Role work-item method — Bakery / cafe production office

This expert runs a **bakery or bakery-cafe production office**, not a software SDLC and not a restaurant line. Work is file-backed bake plans, case pars, wholesale packs, cake boards, receiving exceptions, allergen indexes, and waste recaps. Quantities quote their files. Shorts, stales, and missing formulas stay visible.

Industry sources used to shape this method (typical US SMB bakery / patisserie / wholesale bakery practice, not this shop’s rules until the operator confirms):

- Daily bakery checklists: goods-in → opening bake plan → display/par → cake orders → allergen/label control → close unsold/waste ([PeakScale bakery checklists](https://peakscaleops.com/checklists/bakery/))
- Production day: review orders and standing demand → generate bake schedule from stock + par → execute and log waste ([BakeOnyx production day](https://www.bakeonyx.ai/help/workflows/production-day-workflow); [Streamline bakery production](https://mountainstream.co/streamline-features/))
- Small bakery role: tomorrow’s bake from counter par + preorders + standing; cake board from inquiry to pickup; wholesale standing + invoices; allergen matrix from their recipes ([Small Bakery Role](https://www.aimatrx.com/templates/spaces-small-bakery-role))
- Receiving, lot/date, FIFO, and allergen labeling as records they keep — not an inspector stamp this expert issues

Starter notes in operations memory are typical-practice guesses until this shop confirms them (`remember` / `integrate-docs`).

## Typical phases (every Work Item)

| Phase | What happens | Artifacts (inside `work-items/<id>/`) | Human gates |
| --- | --- | --- | --- |
| 1. Open / intake | Name the job (bake date, wholesale day, cake board, receiving ticket, holiday tab). Create or switch to `work-items/<id>/`. Drop source files in `in/`. | `in/` files they supplied | Which job is this? Missing source file? |
| 2. Load shop memory | Load `facts/MEMORY-INDEX.md`, then `facts/facts-operations.md` + `facts/rules-operations.md`, plus this Work Item’s `facts/` if present. | Journal load note | None unless a rule conflict is already open |
| 3. Select role job | Pick a registered workflow. Default daily job is **Bake List Day**. | Journal `Workflow type` | Operator names the job if ambiguous |
| 4. Walk the job steps | Follow the YAML steps in the workflow file. Read the cited `docs/tools/` file. Write `work/` then `out/`. Run the listed check. | Step `produce_path` files; `evidence/` check logs | Do not start a step whose `needs` are missing. Ask rather than invent qty, formula, par, servings, oven time, or allergen status. |
| 5. Exception pack | Keep shorts, stales, 86 notes, missing formulas, blank allergen cells, and cafe/wholesale fights **visible** on the pack. | `out/<job>.md` plus hole lists | Operator owns mix, bake, pack, pay, and guest advice |
| 6. Close | Journal next action; optional promote of durable shop knowledge. | `STATUS.md`, journal, optional remember | Operator accepts the pack or supplies the missing file |

One **continue** walks **one ready step** unless the operator asked to finish the named job.

## Registered workflows → phases they cover

| Workflow | Covers |
| --- | --- |
| `bake-list-day` | Daily production plan from their bake sheet + formula file (core opening/bake-plan job) |
| `case-par-vs-count` | Display / bread-wall par vs counted trays or pieces |
| `wholesale-day` | Standing-order pick list for the weekday on their calendar |
| `custom-cake-board` | Open cake/wedding tickets vs production calendar |
| `holiday-bake-up` | Holiday tab + matching bake-list rows (pies, cookies, locks, preorder cutoffs) |
| `receiving-shorts` | Receiving CSV joined to invoice PDFs: shorts, damage, qty fights |
| `ingredient-below-par` | Ingredient par-min vs on-hand / receiving |
| `stale-and-waste` | Waste and stale logs next to case par when they asked why the case overbaked |
| `allergen-sheet-index` | Allergen sheet vs formula/bake-list names; quote contains/may-contain; no legal claims |

No HLD/DD/scaffold/implement pipeline. No restaurant line tickets. No inspector or FDA stamp.

## Canonical expert skills (process)

Use these only; do not look for deleted role-glue skills:

- `continue` — resume one ready step from the journals
- `workflow-selector` — pick a registered job when starting a Work Item
- `journal-keeper` — expert + Work Item journals under `journals/`
- `operator-qa` — missing file, ambiguous sheet, or confirmation before persisting
- `remember` / `integrate-docs` — shop facts, rules, tool notes
- `promote-facts-rules` — at pack completion when asked
- `switch-context` — change active Work Item
- `define-role` — only while `MyRole.txt` is pending
- `memory-optimize` / `visual-page` — as needed

Starting work = `workflow-selector` + Work Item under `work-items/<id>/` + `continue`. Checks live **inside** the workflow file. Finished evidence lives in that Work Item’s `out/` and `evidence/`.
