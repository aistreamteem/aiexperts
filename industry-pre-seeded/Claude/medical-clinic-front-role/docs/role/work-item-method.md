# Role work-item method — Medical clinic front role

**Role:** Medical clinic front role (not the clinician)

This expert does **role paperwork**, not clinical care. A Work Item is one appointment, one clinic date, or one named pack. Files live under `work-items/<id>/{in,work,out,evidence}/`. Progress lives in `journals/work-items/<id>/`. Role memory lives in shared (`facts/facts-shared.md`, `facts/rules-shared.md`) then operations (`facts/facts-operations.md`, `facts/rules-operations.md`).

Industry sources for the phase list (orientation only, not this shop’s rules): typical US clinic front-role check-in/check-out loops (schedule + eligibility before the visit; identity, insurance, forms, and posted copay at the window; follow-up and no-show at close), HIPAA minimum-necessary habits at the role, and referral/ROI tracking as paperwork completeness.

## Typical phases

| Phase | What happens | Main artifacts | Human gates |
| --- | --- | --- | --- |
| 1. Open the day | Shape tomorrow/today’s book from the schedule export. Keep blocks, lunch, huddle. | Day list (`work/` CSV, `out/` list) | Confirm export date and identifiers allowed on a window print. Do not invent a missing column. |
| 2. Pre-visit eligibility | Quote only the dated screenshot or clearinghouse print they saved. | Eligibility quote in `out/` | Stale, cropped, or wrong-member image → ask. Do not invent remaining benefits. |
| 3. Check-in paperwork | Completeness of intake, NPP ack, consents, photo ID flag, insurance-card image present. | Missing-forms list | Missing NPP or required page → ask. No clinical reading of history answers. Guardian forms for minors: present or missing only. |
| 4. Fill the book | Wait-list options against an open slot; recall list only if they exported one. | Wait-list / recall list | They choose who is offered. Do not message patients. |
| 5. Referrals and records | Inbound/outbound referral packets; ROI log. | Completeness index, ROI log | Auth numbers only if already printed. Records leave only on their ROI process. No diagnosis, no clinical argument. |
| 6. No-shows | List rows they already coded no-show, late cancel, or broken. | No-show list | Do not invent a no-show fee. |
| 7. Day close | Tender types and amounts they recorded. | Day-close list | No PAN or check account numbers. Do not send a deposit. Short-or-over is their math, not a silent fix. |

## Which registered workflows cover which phases

| Workflow id | Phase |
| --- | --- |
| `day-list` | 1 Open the day (default starting job) |
| `eligibility-from-screenshot` | 2 Pre-visit eligibility |
| `intake-completeness` | 3 Check-in paperwork |
| `wait-list` | 4 Fill the book |
| `recall-list-if-file` | 4 Fill the book |
| `referral-paperwork` | 5 Referrals and records |
| `records-release-log` | 5 Referrals and records |
| `no-show-list` | 6 No-shows |
| `day-close-tender` | 7 Day close |

## How a Work Item runs

1. Operator names the job (clinic date, chart pack, or WID). Use **workflow-selector** if the journal has no workflow type.
2. Copy `work-items/_TEMPLATE/` to `work-items/<id>/` if needed. Put source files in `in/`.
3. Follow the selected `.claude/workflows/<id>.md` steps. Each step: read the named `docs/tools/` file, write the produced file under this Work Item, run the listed check if present, then **journal-keeper**.
4. Missing source file or missing clinic procedure → ask (**operator-qa** when several questions must stay together). Do not invent how *this* clinic works.
5. Outside `MyRole.txt` (diagnose, treat, pick CPT as care, promise coverage) → refuse in the pack and journal. Point clinical questions at the clinician.
6. Done when required files exist (or exceptions are documented), the pack in `out/` names sources and artifacts, and the Work Item journal next action is complete.

**Continue** means one ready workflow step, not approval of an open question.

## Canonical expert skills (process)

`continue`, `define-role`, `journal-keeper`, `remember`, `workflow-selector`, `operator-qa`, `promote-facts-rules`, `switch-context`, `integrate-docs`, `memory-optimize`, `visual-page`.

Role *how* lives in `.claude/workflows/*`, `docs/tools/`, and operations facts/rules — not in a second process-skill layer.
