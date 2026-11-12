---
name: operator-qa
description: >-
  Runs a self-contained question-and-answer session with the human operator to
  clarify conversation, missing sheets, shop practice, or notes before persisting them.
  Creates a qa-sessions folder with a journal, records Q&A turns, then extracts
  answers into conclusions for next steps.
trigger: Clarify, verify with operator, or operator asks for Q&A
---

# Operator Q&A

## Purpose

Hold a focused Q&A session. Keep turns in a session journal. When it ends, extract answers into conclusions that drive the next processor step (confirm a missing conditions sheet, accept a labeled guess, confirm CTC/lock as their flag, or persist a fact/rule).

## Work item branch

Keep the question transcript in this session journal. Present a fixed choice with **AskQuestion**. Ask an open-ended question in chat. When a question blocks the current work item, also add a node on that work item's map. The node id is unique and is not `work-item` or a phase name. Store the session id on the node and make it the active leaf through journal-keeper. When the session closes, store the decision and run the journal-keeper answer transition so `active` leaves this question.

## Session location

Sessions live at the expert root under `qa-sessions/`.

Active session id file: `.cursor/active-qa-session.txt`

Ids are `Q` plus a counter: `Q1`, `Q2`, …

Copy `qa-sessions/_TEMPLATE/` to `qa-sessions/<id>/` when opening a session.

## When to use

- Confirm which loan this pack is for
- Missing conditions sheet or LOS export when a checklist is requested
- Verify a labeled document-type or LOS-code guess
- Confirm CTC / lock / docs-out as their flag, not a conclusion
- Verify notes before **remember**
- Operator says ask me / clarify / Q&A / verify this

Initiate on your own when a human answer would change the pack. Prefer this skill over inventing shop practice.

Do not use this skill for a workflow step that already has a clear next action and no blocking ambiguity.

## Phases

### 1. Open

1. Choose the next free id (`Q1`, `Q2`, …) under `qa-sessions/` (skip `_TEMPLATE`).
2. Copy `qa-sessions/_TEMPLATE/` to `qa-sessions/<id>/`.
3. Write `.cursor/active-qa-session.txt` with that id.
4. Fill `PURPOSE.md`: goal, context (work item / topic / conversation), intended outcome (`assumptions` | `notes` | `loan` | `gate` | `direction` | `other`).
5. Initialize `journal/progress.md` fields and set Next action to `ask`.
6. Tell the operator the session id and purpose in one short sentence, then present the first question(s).

### 2. Ask

1. Ask only what is needed. Prefer one blocking question at a time.
2. Present questions using **How to present questions** (AskQuestion vs chat).
3. Append each asked question under **Open questions** in the journal with the date and presentation mode (`ask-question` or `chat`).
4. Set Next action to `wait for operator`.
5. Stop and wait. Do not invent answers. Do not continue the blocked work until answers arrive or the operator defers them.

## How to present questions

### Use AskQuestion (choice UI)

Use the **AskQuestion** tool when it is available and the answer is a small fixed set:

- Yes / no / defer
- Confirm / reject a proposed note, fact, rule, or guess
- Pick among named alternatives (which loan, which sheet, chase vs hold)

When calling AskQuestion, pass a `questions` array. Each item has `id`, `prompt`, `options` (at least two, each with `id` and `label`), and `allow_multiple` only when several options may apply. Do not add an "Other" option. Include an explicit defer option when postponing is valid.

Prefer one blocking question at a time. After the operator selects, treat the selected label as the answer and continue to Record.

If AskQuestion is unavailable, fall back to chat with the same options as a numbered list.

### Use chat (conversational)

Ask in the chat message when the answer is open-ended: loan labels, shop wording, how *this* shop codes PTD versus PTF.

### 3. Record (when the operator replies)

In the same response:

1. Move each answered item from Open questions to **Resolved Q&A** with date, question, answer, and presentation mode.
2. Note any deferred or refused questions under **Deferred**.
3. Update STATUS.md Last session summary.
4. Either ask the next question or close when enough is known.

### 4. Close

1. Read the full journal Resolved Q&A and Deferred lists.
2. Write `conclusions.md` with Session goal, Decisions / answers, Assumptions still open, **Forward actions**, and Artifacts to update.
3. Set journal Completion status to `done`, Next action to `done`.
4. Leave `.cursor/active-qa-session.txt` with the closed id; next Open picks a new id.
5. Tell the operator the session is closed and point to `conclusions.md`.
6. Apply forward actions only after close, unless the operator asked to apply during the session.

**Forward actions** after close must be processor next steps, for example:

- Put the conditions sheet in `work-items/<id>/in/` and **continue** the first workflow step
- Run **remember** with the verified wording
- Start or switch to a Work Item for the named loan
- Resume `conditions-checklist` / `missing-docs` / other selected job

Do not forward to software design, HLD approval, or deleted process skills.

## Journal fields

Keep these in `journal/progress.md`: Session ID, purpose, linked work item, outcome type, Open questions, Resolved Q&A, Deferred, Last completed, Next action, Completion status, Last session summary.

## Rules

- One active Q&A session at a time unless the operator names another id to resume.
- Do not persist remember/facts/rules from unverified notes until this session closes with verification conclusions, when that was the purpose.
- Do not ask the operator to invent a session id; create it.
- "Continue" is not an answer to an open Q&A question.

## Examples

**Missing conditions sheet**

1. Open Q2 with purpose “confirm source before building a checklist”.
2. AskQuestion: `Conditions sheet is in in/`, `LOS export is coming (wait)`, `Defer`.
3. Close → continue `conditions-checklist` after the file is in `in/`.

**Verify before remember**

1. Open Q4 with outcome `notes`.
2. AskQuestion: persist “Never declare CTC from a green checklist” as an expert-role rule? `Yes`, `Yes, I will edit`, `No`, `Defer`.
3. Close → **remember** with verified wording.

**Guessed document type**

1. Ask whether a scan labeled “bank.pdf” is a VOD or a statement.
2. Close → next action is label the guess on the index, not invent a shop document type.
