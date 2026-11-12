# Role work-item method — Job coordinator in a trade shop

**Role:** Job coordinator in a trade shop  
**Industry:** US small/mid HVAC, plumbing, electrical (and similar) service and install shops  
**Research date:** 2026-11-08

This role produces **files** (daily boards, sold-job packs, packing lists, permit-number rows, closeout photo checklists, callback flags). It does **not** hold a trade license, pass an inspection, specify a design or load calc, send money, or store gate/alarm codes.

## Industry funnel (research)

Typical US trade-office coordinator / dispatcher / install-coordinator work runs two clocks (demand service vs sold install) and a closeout/callback loop:

1. **Intake and priority** — Log the request; flag life-safety (gas smell, CO, sparking, freeze no-heat, active flood) ahead of memberships. Confirm address/unit. Do not invent an ETA. Callbacks link to the original job; do not classify free vs billable at intake unless their file already marks it.
2. **Sold scope (install clock)** — Convert only what they marked sold. Parts/SKUs come from the sold PDF, not a usual kit. Deposit/payment is theirs; this role does not send money.
3. **Permits and locates** — Permit *number on file*, AHJ, dates. Do not say passed unless their file names the result and date. Dig jobs need a locate ticket they already have — do not invent 811 clearance.
4. **Parts and staging** — Packing list before the truck rolls. Special orders vs truck stock. Warranty/RMA parts need serial + install date from their file. They pay the supply house.
5. **Schedule and dispatch** — Daily board and week view: assigned tech, PTO, overbook, sold installs without parts. Ask before moving a customer window. Two-person and weather holds from their SOP.
6. **Truck load** — Combined packing list for one tech/crew; missing specials stay questions. They load the truck.
7. **Closeout** — Required photos (data plate, before/after, as-built if they require it) present or missing. Serials from photos, not invented. Inspection results quoted from their file only.
8. **Callback / warranty** — Flag same-symptom returns; labor warranty vs manufacturer parts warranty are different clocks. No legal fault admission. No manufacturer promise.

Sources used for orientation (not this shop’s policy): Ballard-style install coordinator duties (schedule, permits, materials, closeout); SMBwiki install-project gates (accepted quote → permits/supply → crew date → work order → closeout); Trade Edge 360 install-coordinator SOP (sold jobs, staging, photos/serials); Moore Mechanical installation-admin coordinator (docs, permits/inspections, weekly schedule); BuildOps service-order chain (request → schedule → execute → docs → follow-up); Pavado “two clocks” (same-day demand vs weeks-long replacement); Contractor College HVAC callback intake (link original job; coverage is a later decision).

## This expert’s phases (Work Item)

Every real job is one Work Item under `work-items/<id>/`. Paths `in/`, `work/`, `out/`, and `evidence/` are **inside that folder**.

| Phase | What happens | Typical artifacts | Human gates |
| --- | --- | --- | --- |
| 1. Isolate the job | Operator names the ticket, sold estimate, crew day, permit pack, or callback. Create/switch Work Item. Select a registered workflow. | `work-items/<id>/`, journal, `STATUS.md` | Confirm Work Item ID and which role job; do not mix two tickets. |
| 2. Intake source files | Drop schedule exports, sold PDFs, packing lists, permit logs, photo folders into `in/`. Read shared facts/rules. Do not invent ETAs, SKUs, permit numbers, or inspection results. | Files in `in/` | Missing export/PDF → ask. Two dated files disagree → quote both and ask which is live. |
| 3. Walk the work map | Follow the selected `.claude/workflows/<job>.md` YAML: one ready step unless they asked for the whole named job. Read the named `docs/tools/` doc. Write the `produces` file under this Work Item. | `work/*.csv` (boards, parts, permit rows, photo gaps) | Do not start a step whose `needs` file is missing. Do not skip a step with a chat summary. Do not roll a truck without a packing list they asked for. |
| 4. Check the step | Run the map’s `check` command against this Work Item’s paths. Retry at most 3, then ask. Log under `evidence/`. | `evidence/` logs; exit 0 on the produced file | Check fail is not a silent pass. Operator approves a new check command if the map has none. |
| 5. Pack | Write the finished board, packing list, permit pack, or photo checklist to `out/`. Journal the artifacts. Completeness packs are not inspection passes or licenses. | `out/*.md` plus supporting CSVs | Operator uses the pack (dispatch, order parts, chase a permit). This expert does not decide. |
| 6. Close | Mark the Work Item done when every map step passed (or a documented exception). Optional promote of shop learnings. | Journal completion, optional `remember` / `promote-facts-rules` | Corrections to how *this* shop works are stored only after the operator confirms. |

**Continue** means: read the journals and perform the **next ready map step**. It is not an answer and not approval of a gate.

## Which registered workflows cover which phases

| Funnel slice | Workflow | Registry id |
| --- | --- | --- |
| Life-safety / emergency board | Emergency Queue | `emergency-queue` |
| Same-symptom / warranty returns | Callback Triage | `callback-triage` (default) |
| Sold estimate → job pack | Quote To Job | `quote-to-job` |
| Permit number, AHJ, dates | Permit File | `permit-file` |
| Packing list for one job | Parts Ready | `parts-ready` |
| Serial / RMA / failed-part order question | Warranty Parts | `warranty-parts` |
| Today’s jobs vs missing packing lists | Daily Board | `daily-board` |
| Week view, PTO, overbook, parts-not-ready sold | Week Schedule | `week-schedule` |
| Combined load for one tech/crew | Truck Load | `truck-load` |
| Required closeout photos present/missing | Closeout Photos | `closeout-photos` |

Access secrets, 811 locates, weather holds, two-person flags, and “sold before schedule install” live in shared facts/rules; they do not need a separate process skill. If the operator names a new recurring role job, add a workflow file and a registry entry — do not invent a free-form pipeline.

## Canonical expert skills used here

`continue`, `workflow-selector`, `journal-keeper`, `remember`, `operator-qa`, `switch-context`, `promote-facts-rules`, `integrate-docs`, `define-role`, `memory-optimize`, `visual-page`.

Role constraints (scope, never invent shop policy, never claim a license or inspection pass) live in `MyRole.txt` and `facts/rules-shared.md`, not in deleted role-glue skills.

## Assumptions

- This seed is a **trade-shop job coordinator** role, not a licensed tech, engineer, AHJ, or CRM vendor.
- Existing ten work maps already match the admin slices of the industry funnel (demand vs install clocks plus closeout/callback); no extra workflow was added.
- Step checks stay as Python file/CSV checks the operator can replace when they correct this shop.
- Default registry job remains `callback-triage` (original seed); operator can pick daily-board or quote-to-job when that is the real work.
