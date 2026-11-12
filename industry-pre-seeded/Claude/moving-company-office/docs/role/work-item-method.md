# Role work-item method — Moving company office

Industry research for US household-goods / local moving offices (owner workflow guides, dispatch/claims field practice, and FMCSA-oriented estimate/inventory/BOL paperwork) plus this seed’s maps and shop constraints.

This role does **not** run a software HLD → DD → implement pipeline. Recurring work is a move file: intake → survey/inventory → estimate → dispatch (crew, truck, materials, delivery window) → load-day papers (weight tickets, high-value list) → post-move claims routing. The operator books, dispatches, issues the bill of lading, sends the estimate, and settles claims. This Expert drafts packs from files they drop.

## Typical phases

| Phase | What happens | Artifacts in the Work Item | Human gates |
| --- | --- | --- | --- |
| 1. Intake | Operator names the move (estimate number, origin date, or their job id) and drops the live rate file, inventory, calendar, tickets, or claim papers. | `in/` source files | Operator confirms which job this is and that the rate/calendar file is the live one. Missing file → ask; do not invent. |
| 2. Survey / inventory | Room-by-room sheet, PBO vs CP, photos, high-value list if their form requires it. Cube/weight stay blank unless their sheet or scale ticket already has a number. | Inventory completeness pack, high-value present/missing check | Operator resurveys missing rooms. Operator collects the high-value list. |
| 3. Estimate | Draft from their rate file + stored inventory. Binding / non-binding / not-to-exceed copied from their form. Accessorials only when the survey already names them. | `out/` estimate draft, questions list | Operator picks binding type if missing. Operator sends the estimate. Fuel/extras only from their memo. |
| 4. Dispatch prep | Crew day list, truck calendar collisions, materials/carton pull, dest delivery windows. | Crew list, truck calendar pack, materials list, window list | Operator dispatches and notifies the customer. Do not invent a person, a free truck day, a box count, or a clock hour. |
| 5. Load-day papers | Weigh-ticket index (tare/gross/net as written). High-value list check if not already done. BOL completeness is listed from their form; they issue and sign. | Weigh-ticket pack, flags | Operator sends the truck back to the scale if a slip is missing. No invented pounds. No DOT legal stamp. |
| 6. Claims routing | Assemble claim row, named photos, inventory lines, BOL number. Quote deadline words from their form only. | Claims routing pack + hole list | Operator names who owns the log. They adjust or send to the van line. This Expert does not settle. |

Payment, deposits, crew pay, tariff/DOT legal opinions, and inventing weight or cube are **out of scope** (see `MyRole.txt`).

## Registered workflows covering the phases

| Workflow | Phases | Instruction file |
| --- | --- | --- |
| `estimate-from-rate-file` | 1, 3 | `.claude/workflows/estimate-from-rate-file.md` |
| `inventory-completeness` | 1, 2 | `.claude/workflows/inventory-completeness.md` |
| `high-value-list-check` | 2, 5 | `.claude/workflows/high-value-list-check.md` |
| `materials-list` | 4 | `.claude/workflows/materials-list.md` |
| `crew-day` | 4 | `.claude/workflows/crew-day.md` |
| `truck-calendar` | 4 | `.claude/workflows/truck-calendar.md` |
| `delivery-window-list` | 4 | `.claude/workflows/delivery-window-list.md` |
| `weigh-ticket-pack` | 5 | `.claude/workflows/weigh-ticket-pack.md` |
| `claims-routing` | 6 | `.claude/workflows/claims-routing.md` |

Default new-job workflow: **estimate-from-rate-file** (typical office start is survey → written estimate). Pick another registered job when the operator already has a booked move, a scale slip, or a claim file.

## How a Work Item runs

1. `workflow-selector` records the job on `journals/work-items/<id>/progress.md`.
2. Files live under `work-items/<id>/` (`in/`, `work/`, `out/`, `evidence/`). Do not mix two moves in one folder.
3. `continue` walks **one ready step** from the selected workflow file (or the whole named job if the operator asked). It is not approval of a gate.
4. Each step: read the named tool under `docs/tools/`, write the produced file, run the check command from the Work Item folder, then `journal-keeper`.
5. Missing shop knowledge or a required operator action → ask (`operator-qa` when clarification would change the pack). Do not invent weight, cube, rates, crew names, or delivery hours.
6. Durable shop corrections → `remember` into shared (`Workflows: all`) or operations memory (or Work Item memory when it is only this move).

Canonical expert skills used with this method: `continue`, `define-role`, `journal-keeper`, `remember`, `workflow-selector`, `operator-qa`, `promote-facts-rules`, `switch-context`, `integrate-docs`, `memory-optimize`, `visual-page`.
