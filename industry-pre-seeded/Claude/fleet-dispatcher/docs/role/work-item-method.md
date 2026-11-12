# Role work-item method — Fleet / delivery dispatcher

Industry research (dispatcher daily SOP / freight dispatch SOP / DOT DVIR-POD close): a small fleet role typically runs a **start → assign → follow exceptions → close the day** loop, not a software HLD/DD/implement pipeline.

Starter notes until this shop teaches otherwise. FMCSA pages are orientation, not a legal opinion.

## Typical phases

| Phase | What happens | Artifacts (inside `work-items/<id>/`) | Human gates |
| --- | --- | --- | --- |
| 1. Intake / board | Operator names the service date and drops roster, route sheet, DVIR/POD folders, exception log, ELD/GPS/fuel exports. | `in/` originals | Operator supplies files; do not invent a roster, GPS ping, or second day’s stops. |
| 2. Start-of-day assignment | Who is on which unit from their roster. Draft options only if asked and labeled as drafts. | `work/assignments.csv`, `out/assignments.md` | Live board stays theirs. Off-roster / PTO drivers stay off. |
| 3. Today’s routes | Stops and windows from their sheet for one date. Sequence stays theirs. | `work/routes.csv`, `out/routes.md` | Do not invent addresses or windows. |
| 4. Equipment / DVIR presence | Which roster units have a DVIR file for the date. Missing is missing. | `work/units.csv`, `work/dvir.csv`, `out/dvir-gaps.md` | No invented clean report; no copy-forward; no OOS ruling. |
| 5. In-transit exceptions | Late, failed, detention, breakdown from their files. Breakdown first. | `work/exceptions.csv`, `work/breakdown.csv`, `work/dwell.csv`, matching `out/*.md` | Times and locations only if the file has them. Operator reviews customer-facing language. |
| 6. Delivery close / POD | Required stops vs files in the POD folder. Presence is yes/no + file name. | `work/pod-required.csv`, `out/pod-check.md` | Do not invent a signature. Unreadable images are questions. |
| 7. File questions | ELD gaps and fuel outliers as questions, not findings or legal stamps. | `work/eld.csv`, `work/fuel.csv`, `out/hos-questions.md`, `out/fuel-questions.md` | Operator decides what a gap means. No remaining-hours legal math. |
| 8. Day pack complete | Checks pass (or documented exceptions). STATUS and journal name the pack. | `out/` pack files, `evidence/` check logs | Operator accepts the pack before treating it as dispatched, billed, or certified. |

## Which registered workflows cover which phases

| Workflow | Phases |
| --- | --- |
| `assignment-pack` | 1–2 |
| `todays-routes` | 1, 3 |
| `dvir-gap` | 1, 4 |
| `exceptions` | 5 |
| `breakdown` | 5 (unit down first) |
| `detention` | 5 (in/out times only) |
| `pod-check` | 6 |
| `hos-questions` | 7 |
| `fuel-outliers` | 7 |

Default workflow in the registry: `assignment-pack`. A typical morning board may run assignment-pack, todays-routes, and dvir-gap as separate Work Items (or a named combined pack the operator asked for). Exception jobs run as they arrive. POD and file-question jobs close the date.

Research also mentions check-calls, billing handover, and tomorrow’s board. This role covers tracking via GPS/exception tools inside the exception jobs; billing is out of scope except POD presence; tomorrow uses the same assignment/routes maps on the next date.

## How continue walks a job

1. Read `MyRole.txt`. Role is already defined for this seed.
2. Resolve the active Work Item under `work-items/<id>/` and its journal under `journals/work-items/<id>/`.
3. If **Workflow type** is missing, run **workflow-selector** and offer only registry jobs.
4. Load `facts/MEMORY-INDEX.md`, then shared then operations facts/rules, plus this Work Item’s facts/rules.
5. Open `.claude/workflows/<workflow>.md` and walk **one ready step** (or the whole named job if requested).
6. Produce files under the Work Item `work/` / `out/` / `evidence/`. Run the step’s check. Update **journal-keeper**.
7. If a gate is waiting, re-ask. The word “continue” is not approval and not an answer.

Canonical expert skills (not a second process-skill layer): `continue`, `define-role`, `journal-keeper`, `remember`, `workflow-selector`, `operator-qa`, `promote-facts-rules`, `switch-context`, `integrate-docs`, `memory-optimize`, `visual-page`.
