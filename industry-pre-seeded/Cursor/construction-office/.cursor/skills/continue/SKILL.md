---
name: continue
description: >-
  Resume from the expert journal and active Work Item when they say continue,
  resume, or start. Continue is not a yes and not an answer. Walks one ready
  step of this construction office job.
---

# Continue

## When

They say continue / resume / start / pick up where we left off.

## Do not

Do not treat “continue” as an answer to an open question or as approval of a pack, exception, or gate. If the next step is waiting, re-ask and stop.

## Do

### Role gate

0. Read `MyRole.txt`.
   - If they said “define my role”, run **define-role** and stop.
   - If `Role status` is `pending` or missing, run **define-role** and stop.
   - If `defined` or `skipped`, continue.

### Context

0a. Read `.cursor/active-context.txt` (`work-item:<id>`). If missing, read `.cursor/active-work-item.txt` (legacy read fallback only).
0b. If no active Work Item, ask: “What are you working on? Give a Work Item id (WID-…) or the job/pack name (job number, site + date, RFI number).” Parse WID- as `context_id`. Write `.cursor/active-context.txt` only (do not write the legacy pointer).
0c. Paths:
   - Active work item: `.cursor/active-context.txt`, formatted `work-item:<id>`
   - Artifacts: `work-items/<id>/` (`in/`, `work/`, `out/`, `evidence/`)
   - Journal: `journals/work-items/<id>/progress.md` for item-wide fields, `state.json` for the branch map, and `nodes/<active leaf>.md` for step notes
0d. Read `journals/work-items/<id>/progress.md` for **Workflow type**. If missing, run **workflow-selector**, then reload. Load `.cursor/workflows/workflow-registry.json` and the instruction file. Follow `docs/role/work-item-method.md`.
0e. If `work-items/<id>/` is missing, copy `work-items/_TEMPLATE/` (include `in/`, `work/`, `out/`, `evidence/`). If the Work Item journal is missing, copy `journals/work-items/_TEMPLATE/` and set **Work item record** to `work-items/<id>/`. Set `Current work item:` in `journals/expert/progress.md`.
0f. Load `facts/MEMORY-INDEX.md`, then the shared pair `facts/facts-shared.md` and `facts/rules-shared.md`, then `work-items/<id>/facts/` if present. Log counts in the journal.

### One ready step

1. Read the Work Item journal. If empty, set next action to **intake** (confirm job number and source files).
2. If Open questions (blocking) is non-empty → ask those. Stop.
3. If Blockers or Last failure is set → describe the block, ask how to proceed, stop.
4. If next action is wait for operator / wait for pack review / wait for source files → re-prompt. Stop. “Continue” is not approval.
5. If next action is empty or done → ask what they want next.
6. Otherwise perform **one** ready step from the loaded workflow file (or the whole named job if they asked for the whole job):
   - **intake** — confirm job number; source files in `in/`; do not start if needs are missing.
   - **extract** (map step ids such as collect, list, pull, roster, items, export, checklist, agenda) — read the tool doc; write `produce_path` inside this Work Item; run the check.
   - **exception pass** (age, match, flag, photos, actions) — same, still quoting their files.
   - **pack** — write `out/`; quote source filenames and their status words; run the file-exists check.
   - On check fail: retry at most 3, then ask.
7. After the step, **journal-keeper**: last completed, artifacts, next action, checks.
8. At session end, write Last session summary and optionally refresh `STATUS.md`.
9. When the Work Item is done, offer **promote-facts-rules**.

Paths in the workflow YAML (`work/`, `out/`) are relative to `work-items/<id>/`.
