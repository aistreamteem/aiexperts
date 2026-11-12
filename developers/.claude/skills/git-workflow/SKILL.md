---
name: git-workflow
description: "Use when the journal says the next action is \"run git-workflow (setup)\" or \"run git-workflow (commit/PR)\", or when implement-feature needs a per-task commit. Three modes: setup (feature branch, commit strategy), commit (one conventional commit per task), and commit-and-PR (merge remote, agent runs the full test suite, push, open PR)."
trigger: Journal says next action is "run git-workflow (setup)" or "run git-workflow (commit/PR)", or implement-feature requests a task commit
---

# Git Workflow

## Journal layer

Step notes and the next action go on the active node through journal-keeper, in `journals/work-items/<id>/nodes/`. Use AskUserQuestion for a fixed choice.

Professional Git workflow for a Work Item: feature branch, commits, tested push, pull request. Three modes: **setup**, **commit**, **commit-and-PR**.

## When to use

- **Setup:** next action is "run git-workflow (setup)" (after task-breakdown, before scaffold-project)
- **Commit:** implement-feature finished a task and the journal **Commit strategy** is `incremental`
- **Commit and PR:** next action is "run git-workflow (commit/PR)" (all tasks complete)

## Instructions

### 0. Work Item context

- Active work item: the line in `.claude/active-context.txt`, formatted `work-item:<id>`.
- Artifacts (spec, docs, TODOS, STATUS, facts): `work-items/<id>/`.
- Journal: `journals/work-items/<id>/progress.md` for item-wide fields, `state.json` for the
  branch map, and `nodes/<active leaf>.md` for step notes, open questions, and the next action.
  Write through journal-keeper.

Read `MyRole.txt` (stop and run define-role if `Role status` is `pending`), the journal for this turn, and load `facts/rules-developer.md`, `facts/rules-shared.md`, and `work-items/<id>/facts/rules.md` (rules **MUST be followed**, e.g. branch naming, commit format, PR content). Pick the mode from the next action.

If any git or remote step fails or needs access (no remote, authentication failure, push rejected, missing URL), do **not** skip it. Explain the situation, record it in the journal (Blockers / Last failure), and ask the user for the URL, credentials, or a decision. Proceed only when you agree on how.

### Mode A: Setup

1. Confirm the folder is a git repository. If not, ask the user whether to `git init` or to supply the repo URL to clone.
2. Check for uncommitted changes (`git status`). If any exist, show them and ask the user: commit, stash, or leave. Do not discard changes.
3. Identify the remote. Ask the user for the remote **Repo URL** if none is configured. Fetch the latest code (`git fetch`).
4. Create and switch to the feature branch `feature/WID-<id>` (from the up-to-date default branch). If it already exists, ask whether to reuse it.
5. Ask the user the **commit strategy** (AskUserQuestion): **incremental** (one commit per completed task) or **single** (one commit at the end).
6. Record in the journal, through journal-keeper: **Repo URL**, **Current branch**, **Commit strategy**.
7. Set the next action to **"run scaffold-project"**.

### Mode B: Commit (one task)

Used when the Commit strategy is `incremental`.

1. Confirm you are on the feature branch (`Current branch` in the journal). Do not commit to the default branch.
2. Stage only the files for this task. Do not stage secrets, `.env` files, or large generated artifacts; update `.gitignore` if needed.
3. Make **one conventional commit per task**: `feat(<area>): <description>`, `fix(<area>): <description>`, `test(<area>): ...`, `docs(<area>): ...`, `refactor(<area>): ...`, `chore(<area>): ...`. Reference the task number or work item in the body (e.g. `Task K/N, WID-<id>`).
4. Record the commit hash in the journal. Do not push here; pushing waits for the commit-and-PR mode and a passing suite.
5. Return control to implement-feature, which sets the next action ("implement-feature (task K+1/N)" or "run git-workflow (commit/PR)").

If the strategy is `single`, do nothing at task time; the commit happens in Mode C.

### Mode C: Commit and PR

1. If the Commit strategy is `single`, commit all changes now with a conventional commit (or a small set of logically grouped conventional commits).
2. Fetch the remote and **merge** the latest default branch into the feature branch (merge, not rebase). If there are conflicts, resolve the clear ones and ask the user about any that need a decision.
3. **The agent runs the full test suite** (unit, integration, and e2e where present; use the commands recorded in the DD / `TODOS.md`) and the build if there is one. Do **not** ask the user to run the tests; ask the user for help only if the agent genuinely cannot run the suite (e.g. missing hardware, credentials, or a service only the user can start), and say exactly what is needed.
4. Record the result in the journal (commands run, pass/fail counts, exceptions). If anything fails, fix it, or if it cannot be fixed, record the failure and discuss with the user. **Do not push until the full suite passes** or the user explicitly accepts a documented exception.
5. Push the branch (`git push -u origin feature/WID-<id>`).
6. Open a pull request (use `gh pr create` or the repo host tool). Follow the repo's PR template if one exists. The description covers: summary, link to the Work Item/design docs, test results, and any known exceptions.
7. Record the **PR URL** in the journal, and give the user the link.
8. Set the next action to **"done"** (set Completion status; add a final handoff note if desired). Suggest promote-facts-rules for the Work Item learnings.

### Proactive detection

If the user corrects branch naming, commit format, or review process, use the remember skill to propose capturing it as a rule.
