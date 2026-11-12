---
name: operator-qa
description: >-
  Runs a self-contained question-and-answer session with the human operator to
  clarify conversation, pin down a role job, verify assumptions before work, or
  verify notes before persisting them. Creates a qa-sessions folder with a
  journal, records Q&A turns, then extracts answers into conclusions for next
  steps.
trigger: Clarify, verify with operator, pin down a salon-role job, or operator asks for Q&A
---

# Operator Q&A

## Purpose

Hold a focused Q&A session with the human operator. Keep all turns in a session journal. When the session ends, extract answers into conclusions that drive the next action (confirmed notes, which workflow to start, missing-file list, or remember).

## Work item branch

Keep the question transcript in this session journal. Present a fixed choice with **AskUserQuestion** when available. Ask an open-ended question in chat. When a question blocks the current work item, also add a node on that work item's map. The node id is unique and is not `work-item` or a phase name. Store the session id on the node and make it the active leaf through journal-keeper. When the session closes, store the decision and run the journal-keeper answer transition so `active` leaves this question.

## Session location

Sessions live at the expert root under `qa-sessions/`.

Active session id file: `.cursor/active-qa-session.txt`

Ids are `Q` plus a counter: `Q1`, `Q2`, …

Copy `qa-sessions/_TEMPLATE/` to `qa-sessions/<id>/` when opening a session.

## When to use

- Clarify which role job this is (day’s book vs closeout vs booth split)
- Verify assumptions before producing a list (which hours file is live, which POS report is official)
- Verify notes before **remember**
- Operator says: "ask me", "clarify", "Q&A", "verify this with me"

**Initiate on your own** when a human answer would change the pack. Prefer this skill over inventing shop procedure.

Do not use this skill when the next YAML step is clear and unblocked.

## Phases

### 1. Open

Choose the next free id, copy the template, write `.cursor/active-qa-session.txt`, fill PURPOSE.md, set Next action to `ask`, present the first question(s).

### 2. Ask

Ask only what is needed. Prefer one blocking question at a time. Use AskUserQuestion for fixed choices (yes/no, which file is live, which workflow). Use chat for free text (menu names, roster labels).

Set Next action to `wait for operator`. Stop. Do not invent answers. "Continue" is not an answer.

### 3. Record

Move answered items to Resolved Q&A. Update STATUS.md. Ask the next question or close.

### 4. Close

Write `conclusions.md` with:
- Session goal
- Decisions / answers
- Assumptions still open
- **Forward actions** (start or resume a Work Item, run remember, produce the next YAML artifact, wait for a dropped export — not a software-build step)
- Artifacts to update

Set completion to done. Apply forward actions only after close unless they asked to apply during the session.

## Examples

**Which hours file is live (AskUserQuestion)**

1. Open Q2 with purpose "confirm posted hours before the day’s book".
2. Options: `Use hours.pdf dated 2026-11-01`, `Use the holiday insert`, `Defer`.
3. Close → conclusions say resume Days Book with the chosen file in `in/`.

**Verify a note before remember**

1. Open Q4 with outcome `notes`.
2. AskUserQuestion: "Persist this as an expert-role rule?" Yes as written / Yes I will edit / No / Defer.
3. Close → conclusions say run **remember** with the verified wording.

**Pin down a new job**

1. Open Q1 with outcome `direction`.
2. Ask which registered workflow matches, or whether to stub a new map.
3. Close → forward action: **workflow-selector** / continue the matching job.
