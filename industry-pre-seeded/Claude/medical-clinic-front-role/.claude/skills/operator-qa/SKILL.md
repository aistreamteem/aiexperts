---
name: operator-qa
description: >-
  Runs a self-contained question-and-answer session with the human operator to
  clarify conversation, verify assumptions before role work, or verify notes
  before persisting them. Creates a qa-sessions folder with a journal,
  records Q&A turns, then extracts answers into conclusions for next steps.
trigger: Clarify, verify with operator, or operator asks for Q&A
---

# Operator Q&A

## Purpose

Hold a focused Q&A session with the human operator. Keep all turns in a session journal. When the session ends, extract answers into conclusions that drive the next action (verified notes, clinic-procedure answers, Work Item start, or remember).

## Work item branch

Keep the question transcript in this session journal. Present a fixed choice with **AskUserQuestion**. Ask an open-ended question in chat. When a question blocks the current work item, also add a node on that work item's map. The node id is unique and is not `work-item` or a phase name. Store the session id on the node and make it the active leaf through journal-keeper. When the session closes, store the decision and run the journal-keeper answer transition so `active` leaves this question. Do not copy every question onto the node. A decision for the whole work item or the expert goes in that flat journal.

## Session location

Sessions live at the expert root under `qa-sessions/`.

Active session id file: `.claude/active-qa-session.txt`

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

- Clarify which clinic date, chart pack, or export this Work Item is
- Confirm a missing form, stale eligibility screenshot, or shop procedure
- Verify notes or facts/rules before persisting them (often before remember)
- Operator says: "ask me", "clarify", "Q&A", "verify this with me"

**Initiate on your own** when a human answer would change the pack. Prefer this skill over inventing missing clinic procedure.

Do not use this skill for silent workflow steps that already have a clear next action and no blocking ambiguity.

## Phases

### 1. Open

1. Choose the next free id (`Q1`, `Q2`, …) under `qa-sessions/` (skip `_TEMPLATE`).
2. Copy `qa-sessions/_TEMPLATE/` to `qa-sessions/<id>/`.
3. Write `.claude/active-qa-session.txt` with that id.
4. Fill `PURPOSE.md`: goal, context (work item / topic), intended outcome (`assumptions` | `notes` | `direction` | `other`).
5. Initialize `journal/progress.md` fields and set Next action to `ask`.
6. Tell the operator the session id and purpose in one short sentence, then present the first question(s).

### 2. Ask

1. Ask only what is needed. Prefer one blocking question at a time. When several independent fixed-choice questions are ready, you may batch up to 4 in one AskUserQuestion call when available.
2. Present questions using **How to present questions**.
3. Append each asked question under **Open questions** in the journal.
4. Set Next action to `wait for operator`.
5. Stop and wait. Do not invent answers. Do not continue the blocked role job until answers arrive or the operator defers them.

## How to present questions

### Use AskUserQuestion (choice UI)

Use **AskUserQuestion** when it is available and the answer is a small fixed set:

- Yes / no / defer
- Confirm / reject a proposed note, fact, or rule wording
- Pick among named alternatives (which posted copay file, which ROI form, which clinic date)

If AskUserQuestion is unavailable, fall back to chat with the same options as a numbered list.

### Use chat (conversational)

Ask in chat when the answer is open-ended: export headers, how *this* clinic names visit types, wording of a missing-forms question.

### 3. Record (when the operator replies)

1. Move each answered item from Open questions to **Resolved Q&A**.
2. Note deferred questions under **Deferred**.
3. Update STATUS.md Last session summary.
4. Either ask the next question or close.

### 4. Close

1. Write `conclusions.md` with session goal, decisions, assumptions still open, **Forward actions**, and artifacts to update.
2. Forward actions must be this role’s next step: continue the registered workflow, **remember** verified wording, start or resume a Work Item, or ask for a missing file. Do not send the operator to a software design phase.
3. Set journal Completion status to `done`, Next action to `done`.
4. Tell the operator the session is closed and point to `conclusions.md`.
5. Apply forward actions only after close, unless the operator asked to apply during the session.

## Journal fields

Keep these in `journal/progress.md`: Session ID, purpose, linked work item, outcome type, Open questions, Resolved Q&A, Deferred, Last completed, Next action, Completion status, Last session summary.

## Rules

- One active Q&A session at a time unless the operator names another id to resume.
- Do not persist remember/facts/rules from unverified notes until this session closes with verification conclusions, when that was the purpose.
- "Continue" is not an answer to an open Q&A question.

## Examples

**Confirm stale eligibility (closed choice)**

1. Open Q2 with purpose "confirm whether to quote last month’s screenshot".
2. AskUserQuestion: `Get a new screenshot`, `Quote as dated/stale`, `Defer`.
3. Close → conclusions say resume `eligibility-from-screenshot` with that choice.

**Verify notes before remember**

1. Open Q4 with outcome `notes`.
2. AskUserQuestion: "Persist this as an expert-role rule?" `Yes, store as written`, `Yes, but I will edit`, `No`, `Defer`.
3. Close → conclusions say run remember with the verified wording.

**Missing NPP acknowledgment**

1. Open Q1. Ask whether the NPP ack is in another folder, declined-to-sign, or still missing.
2. Close → resume `intake-completeness`; do not mark the packet complete if still missing.
