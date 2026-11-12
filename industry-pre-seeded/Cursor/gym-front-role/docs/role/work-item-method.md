# Role work-item method — Gym / fitness front role

**Role:** Gym / fitness front role  
**Industry:** Typical US gym or boutique studio front role (file-side lists and packs)  
**Research date:** 2026-11-08

Industry front-role practice is a **shift loop**, not a software design pipeline: prepare the role, check members and guests in, handle exceptions (expired, frozen, past due, missing waiver), record guest and class activity, then close retail and cash with a handover note. This expert does the **file-side** of that loop: membership exports, scan CSVs, waiver folders, policy PDFs, and price sheets the operator drops in. It does not run the live POS, door, or EFT.

Research used (orientation only; shop files still win): Cloud Gym Manager front-role SOP and open/close checklists; gym member check-in SOP (verify active status, guest waiver, minor guardian); GymLiquid daily close (cash vs card, discrepancy note, next-shift handover); Gymizen exception categories and manager gates for overrides/refunds; cancellation SOP (request date, notice from the agreement, confirm in writing, deactivate on the effective date). Physical opening tasks (boot POS, test scanners, lock doors) stay with the operator on the floor.

## Typical phases

1. **Intake shop files** — Put the membership export, scan/check-in CSV, waiver folder, freeze log, policy/price PDFs, and other named sources in `work-items/<id>/in/`. Read `docs/tools/` for the matching file shape. Do not invent dues, freeze days, class capacity, or a deny reason.
2. **Select the role job** — Use **workflow-selector** against `.cursor/workflows/workflow-registry.json`. Default daily job is **check-in-day**. One Work Item = one day, member id, class date, or named pack.
3. **Build the list or pack** — Follow the registered workflow file. Each YAML step: confirm `needs` files exist, read the cited tool doc, write `produce_path` under the Work Item (`work/` or `out/`), run the `check` command, keep the log in `evidence/`. Pass produced files—not chat summaries—to the next step.
4. **Exception and eligibility review** — Denied or frozen scans, missing waivers, guest-without-host, failed drafts, freeze/cancel mismatches. List exceptions; do not rewrite the live access flag, retry a draft, or mark someone released.
5. **Human gates** — Stop for operator answer or approval when shop policy is missing, an override is requested, freeze/cancel terms would be applied, a member must be contacted, or a check cannot be written from a file. `continue` is not approval.
6. **Close the pack** — Finished list or close pack in `out/`, check logs in `evidence/`, STATUS and journal updated. Optional **remember** / **promote-facts-rules** for a durable shop correction.

## Artifacts

| Phase | Typical artifacts (under `work-items/<id>/`) |
| --- | --- |
| Intake | `in/` exports, PDFs, waiver copies |
| Build | `work/check-in.csv`, `work/access-flags.csv`, rosters, freeze lists, guest logs |
| Exceptions | exception CSV/markdown joined to flags or waivers |
| Close | `out/<job>.md` (or CSV), `evidence/` check logs, `STATUS.md` pack note |

## Human gates

- Missing shop file (policy, price, contract PDF, waiver folder, scan export): ask; do not invent.
- Access override, freeze length, cancel channel, ETF amount, class capacity: quote their file or wait.
- Failed draft / collections: list from their export; **they** contact the member. Do not run EFT, refund, or a demand letter.
- Medical / diet / PAR-Q / freeze medical note: present-or-missing only. Not clinical advice.
- Operator approval or waiver must be explicit. The word `continue` is not a yes.

## Registered workflows vs phases

| Workflow | Covers |
| --- | --- |
| `check-in-day` | Daily check-in list from scan export + access flags (typical daily job) |
| `access-flag-exceptions` | Denied walks, questioned allows, recorded overrides |
| `guest-pass-log` | Guest visits, host rows, waiver join |
| `missing-waivers` | Members/guests whose required form is absent |
| `freeze-and-cancel-list` | Open freezes and pending cancels vs their policy files |
| `failed-draft-list` | Failed drafts from billing export (list only) |
| `class-roster` | Named class roster vs schedule capacity |
| `pt-session-counts` | Purchased / used / remaining PT from their menu sheet |
| `retail-close` | Retail count + day-close tender (cash/card as their file) |

Canonical expert skills that drive the loop: **continue**, **workflow-selector**, **journal-keeper**, **operator-qa**, **remember**, **integrate-docs**, **promote-facts-rules**, **switch-context**, **define-role**, **memory-optimize**, **visual-page**. Role *how* lives in `.cursor/workflows/*` and `docs/tools/`, not in a second process-skill layer.

## Definition of done

Required workflow steps and checks passed (or documented exceptions accepted), pack files exist under the Work Item `out/`, evidence logs exist, and the Work Item journal next action is `done` or waiting on a named operator action.

## Assumptions

- This seed is a **gym / boutique front role** file expert, not the trainer, clinician, diet adviser, payment processor, or collections counsel.
- Existing nine work maps already match the admin slices of the industry shift loop; no extra workflow was added.
- Physical open/close (boot POS, lock doors) is the operator on the floor; this expert stays file-side.
- Step checks stay as Python file/CSV checks the operator can replace when they correct this shop.
