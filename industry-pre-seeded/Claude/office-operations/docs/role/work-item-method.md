# Role work-item method — Office and operations

This expert runs **recurring small-office administration**, not software delivery. A Work Item is one named pack: a week, a meeting, a mail log, a supply count, a key audit, a license watch, a visitor week, a vendor list, a retention hold list, or a recurring checklist.

Industry practice for office managers and office administrators (daily open / mail / calendar; weekly supplies and visitor confirmation; monthly or quarterly license, key, and vendor reviews) maps onto the registered jobs below. Sources used for this note: small-business office-manager daily checklists, license/COI tracking routines, records-retention SOPs, and mail/visitor/key logs. Starter notes are typical US SMB orientation until the operator confirms this shop.

## Typical phases

| Phase | What happens | Artifacts (under `work-items/<id>/`) |
| --- | --- | --- |
| 1. Intake | Name the pack. Collect the operator’s source files (calendar export, tracker, log sheet, minutes). Do not scrape a live mailbox or invent a missing export. | `in/` source files; journal names the period |
| 2. Confirm period and owners | Confirm week start if the export and wall calendar disagree. Blank owners stay questions. Two conflicting dates: list both and ask. | Open questions on the Work Item journal |
| 3. Build from their files | Copy, flag, and list from files they provided. Follow the selected workflow’s step map. Do not invent contacts, mins, SKUs, retention years, meetings, or key numbers. | `work/` CSVs and working notes |
| 4. Completeness check | Required columns exist. Named pack file exists. Gaps are listed as questions, not filled with guesses. Retry a failed file check at most three times, then ask. | Check logs in `evidence/`; pack in `out/` |
| 5. Operator review (human gate) | Operator reviews the pack. They send mail, place orders, deposit checks, shred boxes, rekey, or file a renewal. This expert drafts files only. | Approval or waiver in journal |
| 6. Close | STATUS done. Session summary. Optionally promote Work Item facts/rules that the operator confirmed. | `STATUS.md`; journal Completion status |

Do **not** use software design-doc, scaffold, or implement phases on this role.

## Human gates

- Confirm week start / pack period when sources disagree.
- Confirm owner when a line has no owner — do not assign a name.
- Operator sends, orders, pays, deposits, shreds, or files with a city or carrier.
- Continue is not approval. Wait for an explicit answer or “I approve this pack.”
- Work outside `MyRole.txt` (HR decisions, legal opinions, payroll tax, money movement, blasts, CRM, passwords, SSNs, complete medical files) is refused; ask what in-scope pack they want instead.

## Registered workflows

| Workflow | Covers phases | Typical cadence (research + source maps) |
| --- | --- | --- |
| `weekly-pack` | 1–6 for the week’s calendar + task sheet | Weekly hub |
| `meeting-pack` | 1–6 for one agenda + open actions | Per meeting |
| `mail-log` | Intake → log → pack; checks seen only | Daily / weekly |
| `supplies` | Count → flag at their min → pack they order | Weekly |
| `visitor-week` | Sign-in sheet for the named week | Weekly |
| `recurring-checklist` | Only lines they named | Weekly / monthly |
| `license-watch` | Dates from their tracker; flag past or blank | Weekly glance / monthly audit |
| `key-audit` | Who holds what from their log | Monthly / quarterly |
| `vendor-contacts` | Contacts and renewal months from their file | Monthly / quarterly |
| `retention-boxes` | Label and hold flag from their sheet | As-needed / quarterly |

Default job when the operator has not named one: **weekly-pack** (the usual small-office weekly digest). Other maps stay first-class; pick them when the operator names that job.

## How continue walks a job

1. Read `MyRole.txt`, then `journals/expert/progress.md` and the active Work Item journal.
2. Load `facts/MEMORY-INDEX.md`, then `facts/facts-operations.md` and `facts/rules-operations.md`, plus this Work Item’s `facts/` and `rules/`.
3. Load `.claude/workflows/<workflow-id>.md` from the registry.
4. Perform **one ready step** (or the whole named job if requested): read the tool doc under `docs/tools/`, write files under this Work Item, run the step’s check, update the journal.
5. If blocked, ask with **operator-qa**. Do not invent shop practice.

Canonical skills for this loop: `continue`, `workflow-selector`, `journal-keeper`, `operator-qa`, `remember`, `integrate-docs`, `promote-facts-rules`, `switch-context`. Role *how* lives in the workflow files and `docs/tools/`, not in a second process-skill layer.
