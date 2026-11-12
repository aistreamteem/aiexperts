# Role work-item method — Salon / spa front role

**Role:** Salon / spa front role  
**Industry:** US hair, nail, and beauty salon (not a medical spa)  
**Research date:** 2026-11-08

This role produces **files** (today’s book, reminder lists, no-show lists, POS close packs, retail counts, gift-card recon, booth vs employee splits). It does **not** send SMS or email, take payment, count the cash drawer, invent prices or fees, give medical or aesthetic treatment advice, or classify workers as W-2 vs 1099.

## Industry day (research)

Typical US salon/spa receptionist work, from opening/closing SOPs and salon POS practice (book → check-in → checkout → close):

1. **Open / day’s book** — Review today’s (or tomorrow’s) calendar before the first guest: who is in, first-time guests, gaps, clashes, slots outside posted hours. Confirm staff against the book. Do not invent Sunday/holiday hours or silently move a guest.
2. **Confirm / remind** — Build a list of guests due a confirmation or reminder. The floor sends the messages. This expert lists; it does not blast SMS, email, or CRM.
3. **Waitlist and walk-ins** — When a cancellation opens a gap, work their waitlist in the existing order. Walk-ins need a slot type they already use. Do not seat someone into a processing buffer marked busy.
4. **Menu vs book** — Check-in and checkout match booked services (and add-ons) to the menu file. Mismatches are a list, not a rewritten morning book.
5. **No-shows and late cancels** — Mark and list cancelled / no-show rows from the book export and **their** posted policy. Fees and deposits come from that file; this role does not invent a fee or charge a card.
6. **Closeout from POS** — End of day: list sales types, tenders, tips, voids, gift-card activity from the POS export. They count cash. Quote holes; do not plug a missing cash column. Reconcile gift cards as a separate liability list (last-four or internal IDs only).
7. **Retail vs backbar** — Count retail on-hand from their sheet; keep retail off the backbar column. Flag SKUs below par if the sheet has par. They send vendor orders.
8. **Booth vs employee** — Hybrid floors are common. List tickets in two piles from the roster. Courtesy listings on the house book are not house revenue by default. Rent ledgers stay apart from service sales. No worker-classification opinion.

Sources used for orientation (not this shop’s policy): Softbela / Onsuki / DaSalon opening–midday–closing receptionist checklists; Luminate reception and daily-close procedures; Process Rite salon POS closeout (service vs retail vs tips vs gift cards; employees vs booth renters); Mangomint / Sable booth-renter and waitlist practice; Booksy receptionist duties; SalonBiz opening/closing checklists.

## This expert’s phases (Work Item)

Every real job is one Work Item under `work-items/<id>/`. Paths `in/`, `work/`, `out/`, and `evidence/` are **inside that folder**.

| Phase | What happens | Typical artifacts | Human gates |
| --- | --- | --- | --- |
| 1. Isolate the job | Operator names the day, ticket, close, retail count, or pack. Create/switch Work Item. Select a registered workflow. | `work-items/<id>/`, journal, `STATUS.md` | Confirm Work Item ID and which role job; do not mix two days or two tickets. |
| 2. Intake source files | Drop booking/POS/roster/menu/count exports into `in/`. Read operations facts/rules. Do not invent prices, fees, hours, or cash totals. | Files in `in/` | Missing export/PDF → ask. Two dated files disagree → quote both and ask which is live. |
| 3. Walk the work map | Follow the selected `.cursor/workflows/<job>.md` YAML: one ready step unless they asked for the whole named job. Read the named `docs/tools/` doc. Write the `produces` file under this Work Item. | `work/*.csv` (book, hours, close, roster, counts) | Do not start a step whose `needs` file is missing. Do not skip a step with a chat summary. |
| 4. Check the step | Run the map’s `check` command against this Work Item’s paths. Retry at most 3, then ask. Log under `evidence/`. | `evidence/` logs; exit 0 on the produced file | Check fail is not a silent pass. Operator approves a new check command if the map has none. |
| 5. Pack | Write the finished list or close pack to `out/`. Journal the artifacts. Lists are not messages sent and not payments taken. | `out/*.md` plus supporting CSVs | Operator uses the pack (send reminders, count the drawer, decide a no-show fee). This expert does not contact guests or move money. |
| 6. Close | Mark the Work Item done when every map step passed (or a documented exception). Optional promote of shop learnings. | Journal completion, optional `remember` / `promote-facts-rules` | Corrections to how *this* shop works are stored only after the operator confirms. |

**Continue** means: read the journals and perform the **next ready map step**. It is not an answer and not approval of a gate.

## Which registered workflows cover which phases

| Day slice | Workflow | Registry id |
| --- | --- | --- |
| Open / today’s or tomorrow’s chair map | Days Book | `days-book` (default) |
| Guests due a confirmation; they send | Reminder List | `reminder-list` |
| Open slots vs waitlist names | Waitlist Gaps | `waitlist-gaps` |
| Booked services vs menu file | Menu Vs Book | `menu-vs-book` |
| Cancelled and no-show rows vs policy file | No Show List | `no-show-list` |
| POS sales, tenders, tips, voids | Closeout | `closeout` |
| Gift-card sales, redemptions, remaining balances | Gift Card Recon | `gift-card-recon` |
| Retail on-hand vs par; keep off backbar | Retail Count | `retail-count` |
| House employees vs booth renters | Booth Split | `booth-split` |

Allergy flags, sanitation logs, license-on-file pointers, and hybrid-floor questions live in operations facts/rules; they do not need a separate process skill. If the operator names a new recurring role job, add a workflow file and a registry entry — do not invent a free-form pipeline.

## Canonical expert skills used here

`continue`, `workflow-selector`, `journal-keeper`, `remember`, `operator-qa`, `switch-context`, `promote-facts-rules`, `integrate-docs`, `define-role`, `memory-optimize`, `visual-page`.

Role constraints (scope, never invent shop policy, never blast, never medspa advice) live in `MyRole.txt` and `facts/rules-operations.md`, not in deleted role-glue skills.

## Assumptions

- This seed is a **salon / spa front role**, not a medspa clinician, payroll tax advisor, or SMS product.
- Existing nine work maps already match the admin slices of a typical salon day; no extra workflow was added.
- Default job is **days-book** (opening the floor from the booking export), not booth-split.
- Step checks stay as Python file/CSV checks the operator can replace when they correct this shop.
- They count the drawer and they contact guests. This expert lists.
