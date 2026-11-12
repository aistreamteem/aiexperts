---
name: operator-qa
description: >-
  Runs a self-contained question-and-answer session with the human operator to
  clarify conversation, verify assumptions before work, or verify notes before
  persisting them. Creates a qa-sessions folder with a journal, records Q&A
  turns, then extracts answers into conclusions for next steps.
  Use when clarifying requirements, checking assumptions, confirming notes,
  or when the operator says start a Q&A session, clarify with me, verify this, or ask me
  questions.
trigger: Clarify, verify with operator, or operator asks for Q&A
---

# Operator Q&A

## Purpose

Hold a focused Q&A session with the human operator on this janitorial-office role. Keep all turns in a session journal. When the session ends, extract answers into conclusions that drive the next action (verified notes, which calendar wins, missing SDS file, start a Work Item, or **remember**).

## Work item branch

Keep the question transcript in this session journal. Present a fixed choice with **AskQuestion**. Ask an open-ended question in chat. When a question blocks the current work item, also add a node on that work item's map. The node id is unique and is not `work-item` or a phase name. Store the session id on the node and make it the active leaf through journal-keeper. When the session closes, store the decision and run the journal-keeper answer transition so `active` leaves this question. Do not copy every question onto the node. A decision for the whole work item or the expert goes in that flat journal.

## Session location

Sessions live at the expert root under `qa-sessions/`.

Active session id file: `.cursor/active-qa-session.txt`

Ids are `Q` plus a counter: `Q1`, `Q2`, …

## Folder layout

```
qa-sessions/
  _TEMPLATE/
    PURPOSE.md
    STATUS.md
    journal/progress.md
    conclusions.md
  Q1/
    PURPOSE.md
    STATUS.md
    journal/progress.md
    conclusions.md
```

Copy `_TEMPLATE/` to `qa-sessions/<id>/` when opening a session.

## When to use

- Clarify which site-night, which calendar wins, courtesy vs billable callback
- Verify assumptions before building a pack
- Verify notes before **remember**
- Operator says: "ask me", "clarify", "Q&A", "verify this with me"

**Initiate on your own** when a human answer would change the pack. Prefer this skill over inventing missing shop practice.

Do not use this skill for a workflow step that already has a clear next action and no blocking ambiguity.

## Phases

### 1. Open

1. Choose the next free id under `qa-sessions/` (skip `_TEMPLATE`).
2. Copy `_TEMPLATE/` to `qa-sessions/<id>/`.
3. Write `.cursor/active-qa-session.txt`.
4. Fill `PURPOSE.md`: goal, context, intended outcome (`assumptions` | `notes` | `direction` | `other`).
5. Initialize `journal/progress.md`; Next action `ask`.
6. Tell the operator the session id and purpose, then present the first question(s).

### 2. Ask

1. Prefer one blocking question at a time. Batch up to 4 AskQuestion items when they are independent.
2. Append each asked question under **Open questions**.
3. Next action: `wait for operator`.
4. Stop. Do not invent answers.

## How to present questions

### Use AskQuestion (choice UI)

- Yes / no / defer
- Courtesy vs billable, company vs customer calendar, create Work Item vs wait for file
- Confirm a proposed fact/rule wording

### Use chat

- Free-text shop wording, site names, how *this* shop numbers callbacks

### 3. Record

Move answers to **Resolved Q&A**. Update STATUS. Ask next or close.

### 4. Close

Write `conclusions.md` with:

- Session goal
- Decisions / answers
- Assumptions still open
- **Forward actions** — concrete next steps on **this role’s** method: **remember** verified wording, start or resume a Work Item, follow the selected `.cursor/workflows/<job>.md` step, supply a missing file. Do not point at a software-design pipeline.
- Artifacts to update

Set Completion status `done`. Tell the operator the session is closed.

## Rules

- One active Q&A session at a time unless the operator names another id.
- "Continue" is not an answer to an open Q&A question.
- Do not persist remember/facts/rules from unverified notes until this session closes when that was the purpose.

## Examples

**Missing SDS**
1. Open Q2: "par sheet names a disinfectant with no SDS index row."
2. AskQuestion: `They will drop the SDS`, `Leave as missing on the pack`, `Defer`.
3. Close → forward action: resume `sds-index-missing` pack step or **remember** their filing rule.

**Verify before remember**
1. Open Q4 with outcome `notes`.
2. AskQuestion: persist as expert-role rule? Yes / edit / No / Defer.
3. Close → run **remember** with the verified wording.
