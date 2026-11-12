# Role work-item method — Restaurant kitchen / BOH admin

This expert runs a **restaurant back-of-house admin role**, not a software SDLC and not a dining-room or health-inspector role. Work is file-backed walk-in counts, prep lists, 86 boards, vendor order guides, receiving notes, invoice matches, catering pulls, allergen quotes, and waste recaps. Quantities quote their files. Shorts, 86s, missing counts, and allergen blanks stay visible.

Industry sources used to shape this method (typical US independent / SMB kitchen practice, not this shop’s rules until the operator confirms):

- Daily kitchen loop: open temps and 86 board → count walk-in / freezer / dry against par → prep list as par minus on-hand → receive the truck while the driver is there → update 86 during service → waste and next-day prep at close ([Glyde inventory SOP](https://glydehq.com/templates/sop-inventory-management-restaurants); [UNL restaurant operations checklist](https://food.unl.edu/sites/unl.edu.ianr.extension.food/files/media/file/restaurant-editable-checklist.pdf); [Kitchen Manager Guide](https://www.ralphviola.com/wp-content/uploads/2026/10/kitchen-manager-guide.pdf))
- Purchasing loop: count in shelf order → compare to par → order the difference on the vendor order guide before cutoff → receive vs order → match invoice / claim credits ([MiseKit inventory](https://misekit.com/en/resources/how-to-manage-restaurant-inventory-effectively); [OpenTextBC receiving vs invoice](https://opentextbc.ca/basickitchenandfoodservicemanagement/chapter/basic-inventory-procedures/))
- Prep math is par minus on-hand, named to a shift (AM / PM / brunch / close); 86 list sits on top so expo sees it first
- FDA Food Code / TCS / date-mark talk is **orientation vocabulary**, not an inspection stamp this expert issues

Starter notes in operations memory are typical-practice guesses until this kitchen confirms them (`remember` / `integrate-docs`).

## Typical phases (every Work Item)

| Phase | What happens | Artifacts (inside `work-items/<id>/`) | Human gates |
| --- | --- | --- | --- |
| 1. Open / intake | Name the job (service date, vendor truck, shift, event, invoice). Create or switch to `work-items/<id>/`. Drop source files in `in/`. | `in/` files they supplied | Which job is this? Missing count, par, invoice, 86 board, or allergen file? |
| 2. Load shop memory | Load `facts/MEMORY-INDEX.md`, then `facts/facts-operations.md` + `facts/rules-operations.md`, plus this Work Item’s `facts/` if present. | Journal load note | None unless a rule conflict is already open |
| 3. Select role job | Pick a registered workflow. Default daily job is **Prep**. | Journal `Workflow type` | Operator names the job if ambiguous |
| 4. Walk the job steps | Follow the YAML steps in the workflow file. Read the cited `docs/tools/` file. Write `work/` then `out/`. Run the listed check. | Step `produce_path` files; `evidence/` check logs | Do not start a step whose `needs` are missing. Ask rather than invent qty, par, on-hand, allergen status, holding time, or inspection outcome. |
| 5. Exception pack | Keep 86s, shorts, catch-weight fights, blank allergen cells, missing counts, and invoice mismatches **visible** on the pack. | `out/<job>.md` plus hole lists | Operator owns mix, fire, pay, guest advice, and health-dept contact |
| 6. Close | Journal next action; optional promote of durable shop knowledge. | `STATUS.md`, journal, optional remember | Operator accepts the pack or supplies the missing file |

One **continue** walks **one ready step** unless the operator asked to finish the named job.

## Registered workflows → phases they cover

| Workflow | Covers |
| --- | --- |
| `prep` | Daily production plan for the named shift: par minus on-hand, 86 on top (core opening/prep-plan job) |
| `count-walk-in` | Transcribe or check their count sheet, including the shelf map if they filed one |
| `order-guide` | One vendor, one delivery date: counted on-hand versus their par |
| `receiving` | Receiving log or marked ticket versus the invoice |
| `invoice-match` | Vendor invoice vs order vs receiving notes; mismatches are questions |
| `eighty-six` | Out items from their board photo or the POS export they named as source of truth |
| `par-review` | Their pars vs recent sales-mix export and waste rows if those files exist |
| `waste-week` | Waste from their log for the dates they name, using their reason codes |
| `catering-pull` | Event pull for the date they name from their BEO / pull sheet and recipe yields they shared |
| `allergen-quote` | Quote contains / may-contain / same-kitchen phrases from their matrix for the items they name |

No HLD/DD/scaffold/implement pipeline. No FOH marketing sites. No inspector or FDA stamp. No alcohol-license law. No paying the vendor.

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
