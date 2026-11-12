# Role work-item method — Optometry front role (not the doctor)

This role is **not** a software pipeline. Work Items are one clinic date, one lab/optical ticket, one recall or wait-list pack, or one close date. Research (typical US optometry front-office practice) plus this seed’s maps:

- Pre-day: print or export tomorrow’s schedule, confirmations, wait-list fill after cancellations
- Insurance: verify eligibility/benefits for the next day’s book; flag exceptions; keep vision vs medical prints separate
- Check-in support: intake packet completeness, NPP ack, posted copay — from files they drop, not live EHR login
- Optical: frame/lens order completeness, missing Rx files, tracing present-or-missing
- Lab/optical follow-through: status, ready-pickup notify lists, redos with their reason code
- Recall: shape their recall/reminder export; they contact patients
- Close: tender types and amounts they recorded for one clinic date

Sources consulted for industry steps (orientation only; this shop’s files win): FrontDesk.care optometry front-role efficiency guide; EyeCareWorks virtual-assistant task list (scheduling, verification, recall, optical status); typical check-in / insurance-verification / check-out / close SOPs used in optometry training checklists.

## Typical phases (one Work Item)

| Phase | What happens | Artifacts (under `work-items/<id>/`) | Human gates |
| --- | --- | --- | --- |
| **Intake / identify the pack** | Name the clinic date, ticket, or list. Copy operator files into `in/`. | `in/` exports, screenshots, PDFs | Operator confirms which pack this is |
| **Load shop memory** | Read `facts/MEMORY-INDEX.md`, then operations facts/rules and the matching tool docs | Journal note of files loaded | If shop procedure is missing, **ask** — do not invent |
| **Shape the list** | Follow the registered workflow’s steps: read the named tool, write `work/` files | CSVs/sheets in `work/` | Missing required export → stop and ask |
| **Check** | Run the step’s check command against the Work Item path; keep logs in `evidence/` | `evidence/*.log` | Check fail after 3 retries → ask; never invent a pass |
| **Pack note** | Write the finished list plus source files, open questions, and what staff must do | `out/*.md` (and list files) | Doctor for clinical/Rx meaning; staff notify patients; coverage only from a dated screenshot |
| **Close / remember** | Journal the pack; optional **remember** / **promote-facts-rules** | Journal STATUS | Operator approval before treating a starter guess as *this* shop |

`work/` and `out/` in a workflow file mean **inside the current Work Item folder**.

## Which registered workflows cover which phases

| Workflow | Covers |
| --- | --- |
| `day-list` | Pre-day schedule: time, doctor, type, their patient label; closed blocks stay |
| `eligibility-screenshot` | Insurance verification quotes from dated screenshots they saved |
| `wait-list` | Backfill options after a cancellation; they choose who is offered |
| `frame-lens-order-completeness` | Optical ticket missing-fields list |
| `missing-rx-on-order` | Jobs that need a Rx file and the file is not present |
| `pickup-notify-list` | Ready jobs not yet marked notified; they call or text |
| `recall-list` | Shape their recall export; they send reminders |
| `redo-log` | Remake rows with their reason code |
| `day-close` | Tender types and amounts they recorded for one clinic date |

Default when starting a typical clinic day: **day-list**. Other jobs are named by the operator.

## Canonical expert skills (not a second process layer)

- **workflow-selector** — pick a registered role job and open/switch the Work Item
- **continue** — one ready workflow step (not an answer or approval)
- **journal-keeper** — record progress, artifacts, checks, open questions
- **operator-qa** — clarify missing shop knowledge, stale eligibility, who may pick up, etc.
- **remember** / **integrate-docs** / **promote-facts-rules** — durable shop memory
- **switch-context** — change the active Work Item
- Scope, refuse, and conflict live in `MyRole.txt` and `facts/rules-operations.md`

## Hard stops (always)

- Never diagnose, prescribe, interpret a spectacle or contact-lens Rx, fit contacts, or adjust/repair as the optician
- Never invent remaining vision benefits, frame allowance, PD, add, lens type, or auth numbers
- Never log into payer portals or store passwords, PAN, or SSN
- Never message patients; produce the list only
- Coverage sentences quote a dated saved screenshot or stay asked
