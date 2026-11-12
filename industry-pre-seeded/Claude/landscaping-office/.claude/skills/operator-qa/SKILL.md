---
name: operator-qa
description: >-
  Runs a self-contained question-and-answer session with the human operator to
  clarify conversation, verify assumptions before work, or verify notes before
  persisting them. Creates a qa-sessions folder with a journal, records Q&A
  turns, then extracts answers into conclusions for next steps.
  Use when clarifying shop practice, checking assumptions, confirming notes,
  or when the operator says start a Q&A session, clarify with me, verify this,
  or ask me questions.
trigger: Clarify, verify with operator, or operator asks for Q&A
---

# Operator Q&A

## Purpose

Hold a focused Q&A session. Keep turns in the session journal. When it ends, extract answers into conclusions that drive the next landscaping-office step (ask for a missing ticket, confirm a weather call, verify a note before **remember**, start a Work Item).

## Work item branch

Keep the transcript in this session journal. Present a fixed choice with **AskUserQuestion** when available. Ask an open-ended question in chat. When a question blocks the current Work Item, also add a node on that Work Item's map. When the session closes, store the decision and run journal-keeper so `active` leaves this question.

## Session location

Sessions live at the expert root under `qa-sessions/`. Active session id file: `.claude/active-qa-session.txt`. Ids: `Q1`, `Q2`, …

Copy `qa-sessions/_TEMPLATE/` to `qa-sessions/<id>/` when opening.

## When to use

- Clarify which crew day, ticket, or week this is
- Missing ticket, price, dump fee, hours, access, dog flag, extra-work auth, or commercial PO
- Weather: have they called a postpone, or is it still on the board?
- Verify notes before **remember**
- Operator says: "ask me", "clarify", "Q&A", "verify this with me"

**Initiate on your own** when a human answer would change the pack. Prefer this over inventing shop practice.

Do not use this skill for a silent next workflow step that already has files and no ambiguity.

## Phases

### 1. Open

1. Next free id under `qa-sessions/` (skip `_TEMPLATE`).
2. Copy template. Write `.claude/active-qa-session.txt`.
3. Fill `PURPOSE.md`. Initialize journal. Next action: `ask`.
4. Tell the operator the session id and the first question.

### 2. Ask

Ask only what is needed. Prefer one blocking question. Record under Open questions. Next action: `wait for operator`. Stop. Do not invent answers.

### How to present questions

**AskUserQuestion** for fixed choices (yes/no/defer; warranty vs courtesy vs billable; draft vs sold; skip vs run). **Chat** for free text (how this shop names crews, what the price-file columns are).

### 3. Record

Move answers to Resolved Q&A the same turn. Update STATUS. Ask next or close.

### 4. Close

Write `conclusions.md` with session goal, decisions, open assumptions, **forward actions** (next workflow step, **remember**, start/continue Work Item — not a software pipeline), artifacts to update. Completion status `done`.

## Rules

- One active Q&A session unless the operator names another id.
- "Continue" is not an answer to an open Q&A question.
- Do not persist remember/facts from unverified notes until this session closes when that was the purpose.

## Examples

**Missing ticket before crew-day pack**

1. Open Q1: "Route row for 12 Oak has no ticket."
2. AskUserQuestion: `They will add a ticket`, `Skip this stop`, `Defer`.
3. Close → continue **crew-day** with the hole listed or the ticket file.

**Verify a skip-list rule before remember**

1. Open Q2 with outcome `notes`.
2. AskUserQuestion: persist as expert-role rule? `Yes`, `Yes, I will edit`, `No`, `Defer`.
3. Close → **remember** with verified wording.
