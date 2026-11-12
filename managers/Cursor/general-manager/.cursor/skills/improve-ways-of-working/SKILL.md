---
name: improve-ways-of-working
description: "Use when cadence, trackers, or decision logs are duplicated or messy. Cleans them up without changing the agreed outcome."
trigger: User asks to improve ways of working, or the next action says so
---

# Improve ways of working

## Journal layer

Step notes and the next action go on the active node through journal-keeper, in `journals/work-items/<id>/nodes/`. Item-wide fields stay in `journals/work-items/<id>/progress.md`. Artifacts live under `work-items/<id>/`. Use AskQuestion for a fixed choice.

1. Name the duplication or the mess: two trackers, two cadences, decisions written in more than one place.
2. Propose what will remain and what will be retired. Do not change the approved outcome, scope, or success measure.
3. Wait for the operator to agree.
4. Make the cleanup. Point the journal and STATUS links at the files that remain.
5. Record what changed in the decision log as a hygiene note, not as a new outcome.
