---
name: task-breakdown
description: "Use when the journal says the next action is \"run task-breakdown\" (after the DD is approved and diagrams are done). Fills TODOS.md from the DD with environment setup before package installs, numbered tasks, and tasks to obtain any repo or download."
trigger: Journal says next action is "run task-breakdown"
---

# Task Breakdown

## Journal layer

Step notes and the next action go on the active node through journal-keeper, in `journals/work-items/<id>/nodes/`. Use AskUserQuestion for a fixed choice.

Turns the approved DD into an ordered, numbered task list so that the app can be set up and run locally with every requirement installed by the agent.

## When to use

- Journal says next action is "run task-breakdown"
- User asks to build or rebuild the task list for the active Work Item

## Instructions

### 0. Work Item context

- Active work item: the line in `.claude/active-context.txt`, formatted `work-item:<id>`.
- Artifacts (spec, docs, TODOS, STATUS, facts): `work-items/<id>/`.
- Journal: `journals/work-items/<id>/progress.md` for item-wide fields, `state.json` for the
  branch map, and `nodes/<active leaf>.md` for step notes, open questions, and the next action.
  Write through journal-keeper.

### 1. Load context and check the gate

1. Read `MyRole.txt`. If `Role status` is `pending`, stop and run define-role.
2. Read the journal for this turn (hook text, or the expert journal, work item journal, `state.json`, and the active node note).
3. Confirm the journal records "DD approved on <date>" or an explicit waiver. If not, re-prompt the user for approval. "Continue" is not approval.
4. Read `work-items/<id>/docs/design/dd.md` (especially its run environment and setup requirements), the HLD, and the loaded facts/rules (`facts/rules-developer.md`, `facts/rules-shared.md`, `work-items/<id>/facts/rules.md`).

### 2. Skip check

If `work-items/<id>/TODOS.md` exists, is filled (not just the template placeholders), and the journal says task-breakdown is complete, do not rebuild it. Set the next action to "run git-workflow (setup)" through journal-keeper. Stop.

### 3. Start from the template

Copy `work-items/_TEMPLATE/TODOS.md` to `work-items/<id>/TODOS.md` if it does not exist. Fill in Work Item ID and Pipeline. Fill the sections **in this order**:

1. **Setup / Environment Tasks**: portable Python, venv, Node project, Visual Studio solution, or whatever the DD names; created before anything is installed into it. Include tasks to **obtain any repository or download** the design needs (clone a GitHub repo, download model files or an SDK) using the URLs in the DD. If a URL is missing or unknown, ask the user for it. Do not drop the task.
2. **Library / Dependency Installation**: pip, npm, NuGet, and similar installs, each run inside the environment from section 1, with versions from the DD.
3. **Scaffold Tasks**: project structure, config files, tooling, CI skeleton.
4. **Implementation Tasks**: ordered from the design (dependencies first); one task is one reviewable unit that implement-feature can finish and test on its own.
5. **Testing Tasks**: unit, integration, and e2e tests per the DD test strategy, plus the task that runs the full suite.
6. **Documentation Tasks**: README, API docs, run/deploy instructions.

**Ordering rule:** environment setup tasks come before every task that installs libraries or packages. Repo/download tasks come before any task that uses them.

### 4. Number the tasks

Number every task sequentially across all sections (`1`, `2`, ... `N`), one line each with a checkbox, so that "implement-feature (task K/N)" has a real N. Each task states what to do and how to verify it. Include the total: write `Status: Not started (0/N)` at the bottom of `TODOS.md`.

### 5. Coverage check

Walk the DD run environment section and confirm each requirement (runtime, environment, every package, every repo/download, every credential or service) has a task. The app must be runnable locally after the last setup/implementation task. Name likely blockers (downloads, credentials, access) and ask the user about them now.

### 6. Proactive detection

If the user corrects the ordering or states a task-structure constraint, use the remember skill to propose capturing it.

### 7. Update the journal

Through journal-keeper: phase = task-breakdown done, Artifacts = `TODOS.md`, total task count N, blockers noted. Set the next action to **"run git-workflow (setup)"**.
