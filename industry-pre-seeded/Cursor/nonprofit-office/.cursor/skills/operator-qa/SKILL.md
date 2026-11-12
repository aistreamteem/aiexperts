---
name: operator-qa
description: >-
  Runs a self-contained question-and-answer session with the human operator to
  clarify conversation, pin down a role job, verify assumptions before work, or
  verify notes before persisting them. Creates a qa-sessions folder with a
  journal, records Q&A turns, then extracts answers into conclusions for next
  steps.
disable-model-invocation: false
---

# Operator Q&A

## Purpose

Hold a focused Q&A session with the human operator. Keep all turns in a session journal. When the session ends, extract answers into conclusions that drive the next action (confirmed notes, which workflow to start, missing-file list, or remember).

## Work item branch

Keep the question transcript in this session journal. Present a fixed choice with **AskQuestion** when available. Ask an open-ended question in chat. When a question blocks the current work item, also add a node on that work item's map. The node id is unique and is not `work-item` or a phase name. Store the session id on the node and make it the active leaf through journal-keeper. When the session closes, store the decision and run the journal-keeper answer transition so `active` leaves this question.

## Session location

Sessions live at the expert root under `qa-sessions/`.

Active session id file: `.cursor/active-qa-session.txt`

Ids are `Q` plus a counter: `Q1`, `Q2`, …

Copy `qa-sessions/_TEMPLATE/` to `qa-sessions/<id>/` when opening a session.

## When to use

- Clarify which role job this is (board pack vs grant deadlines vs gift ack draft)
- Verify assumptions before producing a pack (which award PDF is live, which ack template)
- Verify notes before **remember**
- Operator says: "ask me", "clarify", "Q&A", "verify this with me"

**Initiate on your own** when a human answer would change the pack. Prefer this skill over inventing shop procedure.

Do not use this skill when the next YAML step is clear and unblocked.

## Phases

### 1. Open

Choose the next free id, copy the template, write `.cursor/active-qa-session.txt`, fill PURPOSE.md, set Next action to `ask`, present the first question(s).

### 2. Ask

Ask only what is needed. Prefer one blocking question at a time. Use AskQuestion for fixed choices (yes/no, which file is live, which workflow). Use chat for free text (grant names, meeting dates).

Set Next action to `wait for operator`. Stop. Do not invent answers. "Continue" is not an answer.

### 3. Record

Move answered items to Resolved Q&A. Update STATUS.md. Ask the next question or close.

### 4. Close

Write `conclusions.md` with answers and **forward actions** (next YAML step, **remember**, start a Work Item via **workflow-selector**). Clear `.cursor/active-qa-session.txt`. Do not act on answers until conclusions exist.

## How to present questions

- Fixed choices → AskQuestion when available
- Open-ended → chat
- Do not invent a session id; create it
- Keep questions plain: which meeting, which grant, which donor export

## Forward actions (this role)

After close, typical next steps:

- Start or continue the matching registered job
- **remember** verified shop wording
- Wait for a missing award PDF, ack template, donor CSV, or board folder

Not: software-build pipelines or deleted role-glue skills.

## Examples

**Clarify which job**

1. Open Q1 with purpose "which role job for this grant folder".
2. AskQuestion: board pack, grant deadlines, funder gap, or gift ack draft.
3. Close. Conclusions: run **workflow-selector** / **continue** on that job.

**Verify notes before remember**

1. Open Q2 with outcome `notes`.
2. Ask whether to persist the correction as an expert-role rule.
3. Close. Conclusions say to run **remember** with the verified wording.
