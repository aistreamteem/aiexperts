---
name: git-workflow
description: "Use when the journal says the next action is \"run git-workflow (setup)\", \"run git-workflow (commit)\", or \"run git-workflow (commit/PR)\", or when implement-feature or iterative-feature needs a branch, commit, or pull request. Three modes: setup, commit, and commit and PR."
disable-model-invocation: false
---

# Git Workflow

## Journal layer

Step notes and the next action go on the active node through journal-keeper, in `journals/work-items/<id>/nodes/`. Use AskQuestion for a fixed choice.

Handles branching, commits, and the pull request for a work item. Three modes: **Setup**, **Commit**, and **Commit and PR**. Never initialize git, change git config, or force-push without asking the user.

## When to use

- Journal says next action is "run git-workflow (setup)" (after task-breakdown)
- implement-feature finishes a task and **Commit strategy** is "incremental" (Commit mode)
- Journal says next action is "run git-workflow (commit/PR)" (all tasks done and tests run)
- iterative-feature needs a branch (step 6) or a commit and PR (step 9)

## Instructions

### 0. Work Item context

- Active work item: the line in `.cursor/active-context.txt`, formatted `work-item:<id>`.
- Artifacts (spec, docs, TODOS, STATUS, facts): `work-items/<id>/`.
- Journal: `journals/work-items/<id>/progress.md` for item-wide fields, `state.json` for the
  branch map, and `nodes/<active leaf>.md` for step notes, open questions, and the next action.
  Write through journal-keeper.

1. Read the journal and decide the mode from the next action. Read the **Repo URL**, **Current branch**, **Commit strategy**, and **PR URL** fields of `progress.md`.

### Mode A: Setup

2. Check for uncommitted changes (`git status`). If there are any, show them and offer to stash or commit them first; do not discard anything.
3. If the repo has no remote or is not connected, ask the user for the repo URL (or whether to create one). Do not skip the step or invent a URL. Fetch the latest code from the remote.
4. Create and check out the feature branch `feature/WID-<id>` (for iterative features, `feature/<work-item-id>-<feature-id>`). If it already exists, ask whether to reuse it.
5. Ask the user for the **commit strategy** with AskQuestion: **incremental** (one commit per task) or **single** (one commit at the end).
6. Update the journal: **Repo URL**, **Current branch**, **Commit strategy**. Set next action to **"run scaffold-project"**.

### Mode B: Commit (one task)

7. Only when Commit strategy is **incremental**. Stage the task's changes and make one conventional commit, `feat(<area>): <description>` or `fix(<area>): <description>`, for example `feat(auth): add user login endpoint`. Do not commit failing work. Do not push in this mode.
8. If the strategy is **single**, make no commit; return to implement-feature. Update the journal with the commit (or "deferred") and leave the next action to implement-feature (task K+1/N).

### Mode C: Commit and PR

9. If Commit strategy is **single**, commit all changes now with a conventional commit message.
10. Fetch and **merge** the latest code from the remote (merge strategy, not rebase). If there are conflicts, stop and work through them with the user.
11. **Run the full build and test suite yourself** (unit, integration, and e2e if present) so previous features are proven to still work. Record the result in the journal. Ask the user to run it only when you cannot run the suite yourself (for example, a missing environment), then wait for "tests pass" or "build successful". **Do not push until the suite passes** or a documented exception is recorded and agreed with the user.
12. Push the branch and open the pull request with a summary of the change, the design docs, and the test result. Record the **PR URL** in the journal.
13. If a push, auth, or network step fails, do not skip it: tell the user what failed, record it in the journal (Blockers / Last failure), and agree on the next step (retry, user supplies URL or credentials, manual step).
14. Set next action to **"done"** (set Completion status and a final handoff note through journal-keeper). Offer **promote-facts-rules** to review the work item's learnings.
