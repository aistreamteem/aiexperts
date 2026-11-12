---
name: operator-qa
description: >-
  Runs a self-contained question-and-answer session with the human operator to
  clarify conversation, build charters or plans, verify assumptions before work,
  or verify notes before persisting them. Creates a qa-sessions folder with a
  journal, records Q&A turns, then extracts answers into conclusions for next
  steps. Use when clarifying requirements, checking assumptions, confirming
  notes, refining a charter or plan with the operator, or when the operator says
  start a Q&A session, clarify with me, verify this, or ask me questions.
---

# Operator Q&A

## Purpose

Hold a focused Q&A session with the human operator. Keep all turns in a session journal. When the session ends, extract answers into conclusions that drive the next action (charter text, plan updates, verified notes, assumption list, or work-item updates).

## Work item branch

Keep the question transcript in this session journal. Use AskUserQuestion for a fixed choice and chat for an open answer. When a question blocks the current work item, add a node on that work item's map. The node id is unique and is not `work-item` or a phase name. Store the session id on the node and make it the active leaf through journal-keeper. When the session closes, store the decision and run the journal-keeper answer transition so `active` leaves this question. Do not copy every question onto the node. A decision for the whole work item or the expert goes in that flat journal.

## Session location

Sessions are folders under `qa-sessions/`, same idea as work items.

| Agent cwd | Session root |
| --- | --- |
| This expert folder (opened as workspace) | `qa-sessions/` |

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

- Clarify ambiguous conversation or management request
- Build or refine a charter, plan, or escalation response with the operator
- Verify assumptions before performing work
- Verify notes or facts/rules before persisting them (often before remember)
- Operator says: "ask me", "clarify", "Q&A", "verify this with me", "let's nail this down"

You may **initiate** a session without being asked when a human answer would change the charter, plan, escalation response, or what you would remember. Prefer it when silent autonomous delivery would guess.

Do not use this skill for silent autonomous delivery steps that already have a clear next action and no blocking ambiguity.

## Phases

### 1. Open

1. Choose the next free id (`Q1`, `Q2`, …) under `qa-sessions/` (skip `_TEMPLATE`).
2. Copy `qa-sessions/_TEMPLATE/` to `qa-sessions/<id>/`.
3. Write `.claude/active-qa-session.txt` with that id.
4. Fill `PURPOSE.md`: goal, context (work item / topic), intended outcome (`spec` | `assumptions` | `notes` | `direction` | `other`).
5. Initialize `journal/progress.md` fields and set Next action to `ask`.
6. Tell the operator the session id and purpose in one short sentence, then present the first question(s) using the presentation rules below.

### 2. Ask

1. Ask only what is needed. Prefer one blocking question at a time. When several independent fixed-choice questions are ready, you may batch up to 4 in one AskUserQuestion call (Claude Code limit); otherwise walk through them one by one.
2. Present questions using **How to present questions** (AskUserQuestion vs chat). Do not rely on the model to invent AskUserQuestion on its own—follow those rules deliberately.
3. Append each asked question under **Open questions** in the journal with the date and presentation mode (`ask-user-question` or `chat`).
4. Set Next action to `wait for operator`.
5. Stop and wait. Do not invent answers. Do not continue the blocked work until answers arrive or the operator defers them.

## How to present questions

Choose the channel from the answer shape. Always journal the question either way.

### Use AskUserQuestion (choice UI)

Use the **AskUserQuestion** tool when it is available and the answer is a small fixed set:

- Yes / no / defer
- A short list of mutually exclusive options (typically 2–4; Claude Code allows 2–4 options per question)
- Confirm / reject a proposed note, fact, rule, or assumption wording
- Pick among named alternatives (charter depth, priority, escalate vs contain, staffing recommendation vs hold, etc.)

When calling AskUserQuestion:

1. Provide 1–4 questions in the `questions` array.
2. For each question set `question` (full prompt), `header` (short chip label, max ~12 chars), and `options` (2–4 items with `label` and `description`).
3. Set `multiSelect` only when several options may apply at once.
4. Do not add an "Other" option yourself—Claude Code provides it automatically. Include an explicit defer/skip-style option when postponing is valid (for example `Defer for later`).
5. After the operator selects, treat the selected label(s) as the answer and continue to Record.

If AskUserQuestion is unavailable in the session, fall back to chat with the same options written as a numbered list and ask the operator to reply with a number or label.

### Use chat (conversational)

Ask in the chat message when the answer is open-ended:

- Free-text outcomes, acceptance criteria, stakeholder wording, or edits
- Explanations, examples, or "tell me how you want this to work"
- Anything that cannot be reduced to a short option list without losing meaning

In chat, ask one blocking question at a time unless the operator asked for a batch. Keep the question plain and specific.

### Mixed sessions

A single Q&A session may alternate: AskUserQuestion for closed choices, chat for free text. Record both the same way in the journal.

### 3. Record (when the operator replies)

In the same response as acknowledging the answer (from AskUserQuestion selection or chat text):

1. Move each answered item from Open questions to **Resolved Q&A** with date, question, answer, and presentation mode.
2. Note any deferred or refused questions under **Deferred**.
3. Update STATUS.md Last session summary.
4. Either ask the next question (phase Ask) or close (phase Close) when enough is known.

### 4. Close

1. Read the full journal Resolved Q&A and Deferred lists.
2. Write `conclusions.md` with:
   - **Session goal**
   - **Decisions / answers** (bullets tied to questions)
   - **Assumptions still open** (if any)
   - **Forward actions** (concrete next steps: update charter, revise plan, run remember, proceed with assignment, etc.)
   - **Artifacts to update** (paths)
3. Set journal Completion status to `done`, Next action to `done`.
4. Clear or leave `.claude/active-qa-session.txt` (leave the id for reference; next Open picks a new id).
5. Tell the operator the session is closed and point to `conclusions.md`.
6. Apply forward actions only after close, unless the operator asked to apply during the session.

## Journal fields

Keep these in `journal/progress.md`:

- Session ID, purpose
- Linked work item (if any)
- Outcome type: spec | assumptions | notes | direction | other
- Open questions
- Resolved Q&A (date, question, answer)
- Deferred
- Last completed, Next action
- Completion status
- Last session summary

## Rules

- One active Q&A session at a time per cwd unless the operator names another id to resume.
- To resume: set `.claude/active-qa-session.txt` and continue from the journal Next action.
- Do not persist remember/facts/rules from unverified notes until this session closes with verification conclusions, when that was the purpose.
- Do not ask the operator to invent a session id; create it.
- Keep operator-facing questions plain and specific.
- Prefer AskUserQuestion for closed choices; do not present a fixed option set only as plain chat when AskUserQuestion is available.

## Examples

**Clarify before charter (closed choice → AskUserQuestion)**

1. Open Q3 with purpose "confirm charter depth and outcome owner before writing".
2. Call AskUserQuestion with options: `Standard`, `Part 1`, `Extended`, `Defer`.
3. Record selected option → Close → conclusions say write charter at that depth and proceed.

**Verify notes before remember (yes/no → AskUserQuestion; edits → chat)**

1. Open Q4 with outcome `notes`.
2. AskUserQuestion: "Persist this as an expert-role rule?" with options `Yes, store as written`, `Yes, but I will edit`, `No`, `Defer`.
3. If the operator chooses edit, ask in chat for the revised wording.
4. Close → conclusions say run remember with the verified wording.

**Open-ended escalation detail (chat)**

1. Open Q5 with outcome `direction`.
2. Ask in chat: "Who must be informed before we change the incident owner, and what is the latest acceptable update time?"
3. If they give a crisp policy, optionally confirm with AskUserQuestion before close.
