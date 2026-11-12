# Repair plan for the current expert scaffold

**Applied to this Engineering Manager (Claude) folder, adapted.** Paths use `.claude/` and `CLAUDE.md` instead of `.cursor/` / `AGENTS.md`. Fix 10 (developer HLD/DD skills) and the production-incident workflow do not apply here; this role already has charter/plan/escalation skills and team-delivery / team-escalation workflows. Vocabulary is management triggers, not SQL/git.

## Summary

There are 13 fixes in four groups:

| Group | Fixes | What it achieves | Needs a decision from you |
| --- | --- | --- | --- |
| A. Small code fixes | 1 to 6 | Hooks work on a fresh clone and read their own templates; triggers match the vocabulary | Fix 5 only (D5) |
| B. One journal location | 7 to 9 | Every skill and hook reads and writes the same files; the audit trail records the real journal | D6, D7 |
| C. Content | 10 to 12 | The missing phase skills and memory files exist; leftovers from the earlier role are gone; `AGENTS.md` agrees with the skills | D1 to D4 |
| D. Keeping it fixed | 13 | A check that fails when a reference goes stale again | None |

Group A can be applied today without any decisions except D5. Groups B and C wait on the seven decisions in the next section.



### What changed since the first document

Checking each item more closely turned up three things that the first document got wrong or missed:

- **A fresh clone on Windows has broken stop hooks.** This is new. Git for Windows converts the `.sh` files to CRLF on checkout, and `bash` then fails with a syntax error (exit code 2). Your working copy is unaffected only because its `.sh` files were never re-checked-out. See fix 1.
- **The audit hook is worse than I reported.** I had only read it. Running it showed that it does more than snapshot the wrong file: it appends background-agent notes into the pointer file whose first line says "Do not write notes here", commits that, and leaves the real journal uncommitted. See fix 9.
- **The stop hooks do run on this machine.** They run through WSL and exit cleanly. What does not work is the note merge inside them, which needs `jq`.

## Decisions needed

Each has a recommendation. The fixes are written assuming the recommendation is accepted.

| # | Decision | Recommendation | Reason |
| --- | --- | --- | --- |
| D1 | Are hld-writer, dd-writer, task-breakdown, and git-workflow skills, or sections of the workflow file? | Skills, one folder each | define-role lists them as starter skills that a role can mark "required" or "not used", `AGENTS.md` rule 4 says each phase has a skill, and skills load only when needed |
| D2 | `AGENTS.md` rule 8 points to `docs/design/hld-profiles.md` and `hld-extended-sections.md`, which do not exist. Do you have the originals? | Supply them if you have them; otherwise keep only the Standard profile | The README gives one line per profile. Writing the Part 1 and Extended section lists from that would be invention |
| D3 | The production-incident workflow is referenced throughout the skills but has no workflow file and is not in the registry. Two different phase lists exist for it. | Write `production-incident.md` once, using the five phases in the continue skill; leave it out of the registry until define-role approves it | The skills then point at something real, and define-role already handles enabling it |
| D4 | Which expert memory files exist? Skills name three sets (developer, incident-response, operations), and "operations" is not a workflow. | A developer pair, an incident pair created with that workflow, and a shared pair (`facts-shared.md`, `rules-shared.md`) that is always loaded and replaces "operations" | See fix 11: entries marked `Workflows: all` are currently filed in the developer file, which the incident workflow never loads |
| D5 | The trigger `config:change` fires on any shell command containing "config". | Drop it from the generic vocabulary until a role defines how its configuration changes are made | There is no way to recognise "a production configuration change" from a command string without knowing the role's tooling |
| D6 | `.cursor/active-work-item.txt` is the legacy pointer; `.cursor/active-context.txt` is the current one. | Stop writing the legacy file. Keep the hook's read fallback for old copies | This scaffold has no work items yet, so nothing depends on the legacy file |
| D7 | `work-items/<id>/journal/progress.md` exists only to say "the journal is elsewhere". | Remove it from the template once fix 7 has corrected every reference | A file that must never be written to, in the place nine skills still write to, keeps the confusion alive |

## Group A: small code fixes

### Fix 1. Keep shell scripts LF on every platform

**Problem.** There is no `.gitattributes`. I cloned the repository with this machine's git settings (`core.autocrlf=true`, the Git for Windows default). The `.sh` files came out CRLF, and the stop hook failed:

```text
.cursor/hooks/on-stop.sh: line 5: $'\r': command not found
.cursor/hooks/on-stop.sh: line 6: syntax error near unexpected token `$'{\r''
exit=2
```

**Change.** Add `.gitattributes` at the root:

```gitattributes
* text=auto
*.sh text eol=lf
```

**Verified.** After committing that file in a test clone, a second fresh clone had LF shell scripts and the stop hook returned `{}` with exit code 0.

Fix 9 removes the shell scripts altogether. Do this fix anyway: it is two lines, and it protects fresh clones until fix 9 lands.

### Fix 2. Add a `.gitignore`

**Problem.** None exists. Importing a hook module leaves `.cursor/hooks/__pycache__/` as an untracked directory. My own probes did this (I removed it), and the index builder in fix 5 and the check script in fix 13 will import the hook too.

**Change.** Add `.gitignore` at the root:

```gitignore
__pycache__/
*.pyc
```

### Fix 3. Journal hook: read bolded fields

**Problem.** The journal templates write `**Current work item:**` and `**Completion status:**`. The hook only matches lines that begin with the unbolded text. So the fallback that finds the work item from the expert journal returns nothing, and a work item marked done is never recognised as done.

**Change.** In `.cursor/hooks/inject_journal_context.py`, replace the two ad hoc line checks with one field reader:

```diff
 import json
+import re
 import sys
 from pathlib import Path
@@
-def _current_work_item(text: str) -> str:
+_FIELD = re.compile(
+    r"^\s*(?:[-*]\s+)?\*{0,2}(?P<name>[^:*]+?)\*{0,2}\s*:\s*\*{0,2}\s*(?P<value>.*?)\s*$"
+)
+
+
+def _field(text: str, name: str) -> str:
+    """Value of a `Name: value` line, with or without bold markers."""
+    wanted = name.lower()
     for line in text.splitlines():
-        if line.startswith("Current work item:"):
-            return line.split(":", 1)[1].strip()
+        match = _FIELD.match(line)
+        if match and match.group("name").strip().lower() == wanted:
+            return match.group("value")
     return ""
 
 
+def _current_work_item(text: str) -> str:
+    return _field(text, "Current work item")
+
+
@@
-    if any(
-        line.lower().startswith("completion status:") and line.split(":", 1)[1].strip().lower() == "done"
-        for line in flat_text.splitlines()
-    ):
+    if _field(flat_text, "Completion status").lower() == "done":
         return _drop_read(tool_name, file_path, sections)
```

**Verified.** The reader returns the right value for `**Name:** value`, `Name: value`, `**Name**: value`, a bulleted field, and an empty field, and it ignores a dated Q&A line. Run end to end against copies of the real templates with no pointer files present, the hook loaded the work-item journal and the active node, and dropped the node notes once the status was set to done. Both existing test scripts still pass.

### Fix 4. Journal hook test: use the real templates

**Problem.** `scripts/test_journal_hook.py` writes its own fixtures with unbolded fields and always creates the legacy pointer file. It therefore passed while the hook could not read a real journal.

**Change.**

- Build the fixtures by copying `journals/_TEMPLATE/expert/` and `journals/work-items/_TEMPLATE/` and filling in the values, so that a template change that breaks the hook also breaks the test.
- Add a case with no pointer files, where the work item is found only from the expert journal line.
- Change the "done" case to edit the template's own `**Completion status:**` line.
- Delete the unused `HOOK` constant and the `_bash` and `_run` helpers, which point at the `.sh` wrapper that `hooks.json` does not use.

### Fix 5. Trigger classifier: one table, matching the vocabulary

**Problem.** The classifier in `.cursor/hooks/inject_rules_on_action.py` and the vocabulary in the skills disagree. I ran these:

| Action | Tokens today | Fault |
| --- | --- | --- |
| `git config user.name x` | `config:change` | Fires on any command containing "config" |
| Write `db/foo.sql` | `write:sql`, `sql:generate` | Keep generic extension tokens only; do not add path-specific deliverable tokens |
| Write any `.md` or `.html` | `write:doc` | Produced, but not in the vocabulary, so no rule can be tagged with it |
| `git -C repo push` | none | Only the exact text "git push" matches |

**Change, part 1.** Replace the `if` chain with two tables. The tables are the vocabulary. This scaffold is role-generic: keep only extension- and command-based triggers.

```diff
+HTML = (".html", ".htm")
+DOC = (".md", ".markdown") + HTML
+
+
+# One table per tool kind. This is the whole trigger vocabulary: a token that
+# is not listed here can never be surfaced, and build_trigger_index.py warns
+# about any rule tagged with one.
+WRITE_TRIGGERS = [
+    ("write:sql", lambda path: path.endswith(".sql")),
+    ("sql:generate", lambda path: path.endswith(".sql")),
+    ("write:doc", lambda path: path.endswith(DOC)),
+]
+SHELL_TRIGGERS = [
+    ("pr:open", re.compile(r"\bgh\s+pr\s+create\b")),
+    ("git:push", re.compile(r"\bgit\b[^;&|\n]*\bpush\b")),
+    ("git:commit", re.compile(r"\bgit\b[^;&|\n]*\bcommit\b")),
+]
+KNOWN_TOKENS = [token for token, _ in WRITE_TRIGGERS + SHELL_TRIGGERS]
+
+
 def classify(tool_name: str, file_path: str, command: str) -> list[str]:
     tokens: list[str] = []
     seen: set[str] = set()
-    path = file_path.lower()
     if tool_name in WRITE_TOOLS:
-        if path.endswith(".sql"):
-            _add(tokens, seen, "write:sql", "sql:generate")
-        if path.endswith(".html"):
-            _add(tokens, seen, "write:doc")
-        if path.endswith(".md") or path.endswith(".markdown"):
-            _add(tokens, seen, "write:doc")
+        path = file_path.lower()
+        for token, matches in WRITE_TRIGGERS:
+            if matches(path):
+                _add(tokens, seen, token)
     elif tool_name in SHELL_TOOLS:
-        if "gh pr create" in command:
-            _add(tokens, seen, "pr:open")
-        if "git push" in command:
-            _add(tokens, seen, "git:push")
-        if "git commit" in command:
-            _add(tokens, seen, "git:commit")
-        if "config" in command:
-            _add(tokens, seen, "config:change")
+        for token, pattern in SHELL_TRIGGERS:
+            if pattern.search(command):
+                _add(tokens, seen, token)
     return tokens
```

(Also add `import re` at the top.) The git patterns deliberately favour matching too often over missing: showing a rule when it was not needed costs a few lines of context, while missing it defeats the purpose.

**Change, part 2.** In `scripts/memory/build_trigger_index.py`, load `KNOWN_TOKENS` from the hook file and list every rule tagged with a token outside it, under a heading "Rules with a trigger the hook cannot produce", the same way it already lists rules with no `Triggers:` field. A mistyped or retired token then shows up in `TRIGGER-INDEX.md` instead of failing silently.

**Change, part 3.** Make the three places that list the vocabulary agree with the table: add `write:doc` and, if D5 is accepted, remove `config:change`.

| File | Lines |
| --- | --- |
| `.cursor/skills/remember/SKILL.md` | 128 to 136 (Question 4 vocabulary) |
| `.cursor/skills/promote-facts-rules/SKILL.md` | 73 (step b.5) |
| `facts/MEMORY-INDEX.md` | 133 (rule entry template) |

**Change, part 4.** Add the four rows of the table above to `scripts/test_rules_hook.py` as cases, plus `npm run build --config webpack.js` expecting no tokens.

**Verified.** With the patch, all eleven classifier cases I wrote return the expected tokens, and the existing rules-hook test passes.

### Fix 6. memory-optimize: count entries, and stop citing scripts that do not exist

**Problem.**

- The entry-count pattern is `^###\d{4}-\d{2}-\d{2}:` with no space after the hashes. On a sample with two entries it counted zero. It appears in `.cursor/skills/memory-optimize/scripts/analyze-memory.py` line 23 and again in a copy pasted into `SKILL.md`.
- `SKILL.md` embeds two long scripts (lines 54 to 121 and 134 to 276) that duplicate the real script, and tells the agent to save one as `facts/analyze-memory.py`.
- `SKILL.md` runs `facts/split-and-optimize.py`, `facts/update-index.py`, and a `validate-migration.py`, none of which exist.
- The metadata check only recognises `### 20` headers, while the remember skill writes `## YYYY-MM-DD` headers.

**Change.**

- In `analyze-memory.py`, use `^#{2,3} \d{4}-\d{2}-\d{2}:` for counting, the same pattern for duplicate detection, and a matching test in `check_workflow_metadata`. (`build_trigger_index.py` already accepts both header levels.)
- Take the file list from `facts/facts-*.md` and `facts/rules-*.md` on disk instead of six hard-coded names.
- In `SKILL.md`, delete both embedded scripts and replace them with one command: `py -3 .cursor/skills/memory-optimize/scripts/analyze-memory.py facts`.
- In `SKILL.md` section 4 and "Automation Scripts", remove the three nonexistent scripts and say plainly that the split and the index update are done by the agent by hand, with the entry count compared before and after.

**Verified.** Only the pattern: the current one counts 0 of 2 sample entries, the replacement counts 2.

## Group B: one journal location

### Fix 7. Make every skill and document use the current paths

**Problem.** Three generations of location coexist. The current design, from `AGENTS.md` rule 2 and the journal-keeper skill, is:

| What | Where |
| --- | --- |
| Active work item | `.cursor/active-context.txt`, one line, `work-item:<id>` |
| Expert journal | `journals/expert/progress.md` |
| Work-item journal (item-wide fields) | `journals/work-items/<id>/progress.md` |
| Branch map | `journals/work-items/<id>/state.json` |
| Step notes, open questions, next action | `journals/work-items/<id>/nodes/<node>.md` |
| Artifacts: spec, docs, TODOS, STATUS, facts, tests | `work-items/<id>/` |

Five skills (implement-feature, iterative-feature, refactor, scaffold-project, diagram-generator) say in a "Journal layer" paragraph not to write to the old path, and then name the old path as the journal a few lines later in a "Work Item Context" block.

**Change, part 1.** Replace the "Work Item Context" block in each skill below with this text:

```markdown
### 0. Work Item context

- Active work item: the line in `.cursor/active-context.txt`, formatted `work-item:<id>`.
- Artifacts (spec, docs, TODOS, STATUS, facts): `work-items/<id>/`.
- Journal: `journals/work-items/<id>/progress.md` for item-wide fields, `state.json` for the
  branch map, and `nodes/<active leaf>.md` for step notes, open questions, and the next action.
  Write through journal-keeper.
```

| Skill | Lines to replace | Other lines naming the old journal |
| --- | --- | --- |
| `spec-parser` | 41 to 44 | 62, 123 |
| `implement-feature` | 24 to 28 | 39 |
| `iterative-feature` | 26 to 30 | none |
| `refactor` | 22 to 25 | none |
| `scaffold-project` | 22 to 25 | none |
| `diagram-generator` | 23 to 26 | 30 (`journal/progress.md`) |
| `promote-facts-rules` | 32 | none |
| `journal-keeper` | 39 | none |

**Change, part 2.** Stop writing the legacy pointer (D6): remove the "also write to `.cursor/active-work-item.txt`" line from `continue` (line 41), `workflow-selector` (line 52), and `switch-context` (line 41). Keep the read fallback in `continue` line 35 and in the hook.

**Change, part 3.** Bring the descriptive documents into line.

| File | Lines | Change |
| --- | --- | --- |
| `.cursor/CONTEXT-SYSTEM.md` | 21, 36 to 45, 55 to 66 | Journal path, legacy file, the skill list (it names `continue.md`, `hld-writer.md`), and the parsing logic that builds `{root_path}/journal/progress.md` |
| `README.md` and `QUICK-START.md` | 74, 88, 103, 148, 227 | The work-item tree and four sentences that send the reader to `work-items\<WID>\journal\progress.md`, including the troubleshooting tip to edit Next action there |
| `work-items/_TEMPLATE/STATUS.md` | 12 to 19 | Turn the Quick Links list into real relative links, with Journal pointing to `../../journals/work-items/<id>/` |

`README.md` and `QUICK-START.md` are byte-identical, so every edit is made twice. Consider reducing one of them to a single line that points to the other.

**Change, part 4.** Remove `work-items/_TEMPLATE/journal/` (D7).

**Check.** Searching the repository for `active-work-item.txt` should find only the two read fallbacks. Searching for `work-items/<…>/journal/` should find nothing.

### Fix 8. Say which file holds each journal field

**Problem.** The journal-keeper skill lists about thirty fields under "Journal Schema" without saying where each lives. The templates hold four of them. Skills are told to "update the journal" with fields such as Commit strategy, Repo URL, and Artifacts that have no home, so each run decides for itself.

**Change.** Add this table to journal-keeper and extend the templates to match. The split follows journal-keeper's own rule (item-wide and slow-changing in the flat journal, step-specific in the node), and it keeps the flat journal short because the hook injects it before every tool call.

| File | Fields |
| --- | --- |
| `journals/work-items/<id>/progress.md` | Work item ID and description; Work item record; Workflow type and workflow-specific context; Spec file and version; Mode; Repo URL; Current branch; Commit strategy; PR URL; HLD profile, intake links, compliance review; Decisions and approvals that every branch inherits; Completion status |
| `journals/work-items/<id>/nodes/<node>.md` | Last completed; Next action; Open questions (blocking and deferred); Q&A resolved in this step; Blockers, pause reason, last failure; facts and rules loaded and applied; proactively detected facts and rules; step notes |
| `work-items/<id>/STATUS.md` | Last session summary; Artifacts list; links |
| Not stored | Current phase. It is the phase node on the `active` path in `state.json` |

This is my proposed split, not something the scaffold already states. Adjust it before applying if you see it differently.

### Fix 9. Stop, merge, and audit hooks: one implementation, in Python, on the real journal

**Problem.** I set up a work item in a test clone the way the continue skill describes, wrote a step note in `journals/work-items/WID-TEST/nodes/work-item.md`, dropped a background-agent note where the merge script looks for one, and ran both scripts.

- `merge-agent-notes.sh` printed `no branch map for WID-TEST - skip` and left the note pending. The branch map was there. The script treats a missing `jq` as a missing map, and the Python fallback a few lines below that check can never be reached.
- `post-journal-update.sh` contains a second, older merge. It appended the note to `work-items/WID-TEST/journal/progress.md`, the pointer file, and committed three files: that pointer, `STATUS.md`, and the archived note. The commit subject was `WI-WID-TEST:  → see the active node's note file`, with the phase blank. `journals/work-items/WID-TEST/`, where the real notes were, stayed uncommitted.
- The script reads the work item only from the legacy pointer file.
- The trigger-index staleness check in `on-stop.sh` names three rules files by hand.
- journal-keeper tells background agents to see "that folder's README" for the notes format. No such folder or README exists.

**Change.** Replace the five shell scripts with Python, and change `hooks.json` to call it the same way the journal hooks are already called (`py -3 .cursor/hooks/<name>.py`).

| New file | Replaces | Role |
| --- | --- | --- |
| `.cursor/hooks/journal_fields.py` | none | The `_field` reader from fix 3 and the active-context lookup, shared by all hooks |
| `.cursor/hooks/merge_agent_notes.py` | `merge-agent-notes.sh`, and the merge half of `post-journal-update.sh` | The only merge |
| `.cursor/hooks/journal_snapshot.py` | The commit half of `post-journal-update.sh` | The audit commit |
| `.cursor/hooks/on_stop.py` | `on-stop.sh`, `on-subagent-stop.sh` | Entry point for both events |

Delete `inject-journal-context.sh` and `inject-rules-on-action.sh` as well; `hooks.json` does not use them.

Behaviour to keep exactly:

- Always exit 0 and print `{}`, and skip the merge when the stop payload says a stop hook is already active.
- One lock per work item, so several subagents finishing together cannot interleave.
- A shared task merges only when every subtask in its manifest has a note; a note whose Status line says failed marks the task partial; a task past its deadline is escalated once.
- Processed notes move to `merged/`; partial and stalled tasks write `NEEDS-ATTENTION.md`.
- The commit names its own paths and never picks up anything else the user has staged; a journal that git ignores is merged on disk and not committed.

Behaviour to change:

- Notes folder: `journals/work-items/<id>/agent-notes/`, with a `README.md` in the template that documents the loose-note and shared-task formats.
- Merge target: the active leaf's node file, read from `state.json` with the standard library. No `jq`.
- Commit paths: `journals/expert/progress.md`, the whole of `journals/work-items/<id>/`, `work-items/<id>/STATUS.md`, and `NEEDS-ATTENTION.md`.
- Commit subject: phase from the `active` path in `state.json`, next action from the leaf node's `Next action` field.
- Work item: from `.cursor/active-context.txt`, with the legacy file as fallback.
- Trigger-index staleness: compare against every `facts/rules-*.md`.
- journal-keeper lines 137 and 146 to 147: update the script name, the notes folder, and the statement that merged notes "land in `progress.md`".

**Test to add.** `scripts/test_stop_hooks.py`, built from the scenario I ran: a loose note ends up in the active node file; a shared task with one subtask missing is left alone; the audit commit contains the `journals/` files and does not contain an unrelated staged file.

This fix is the largest piece of code in the plan: about 540 lines of shell to port (`merge-agent-notes.sh` 252, `post-journal-update.sh` 222, `on-stop.sh` 64, `on-subagent-stop.sh` 7). It is not written yet.

## Group C: content

### Fix 10. Write the four missing phase skills

**Problem.** `hld-writer`, `dd-writer`, `task-breakdown`, and `git-workflow` are named as skills in `AGENTS.md` (rule 17), `define-role` (question 6), `continue`, `journal-keeper`, `spec-parser`, `iterative-feature`, `implement-feature`, `scaffold-project`, `remember`, `MyRole.txt`, and the TODOS template. None has a folder. Their whole definition is three to eight bullets each in `.cursor/workflows/developer.md`. The README says this is intentional, but the result is that the design phases, the centre of the developer pipeline, have less instruction than the remember skill has for storing one fact.

**Change.** Create one `SKILL.md` for each (D1), in the same shape as `scaffold-project`: a "Journal layer" paragraph, the context block from fix 7, numbered instructions, and the next action to set. The requirements already exist, scattered; each skill gathers them.

| Skill | Must contain | Where the requirement comes from |
| --- | --- | --- |
| `hld-writer` | Read the requirements summary and loaded rules. Ask for a team template or example document first. Choose the HLD profile. Write `docs/design/hld.md` and its diagrams, and update `docs/diagrams/index.html`. List assumptions and open questions as blocking or deferred. Name likely blockers (downloads, credentials, access). Skip if the artifact exists and the journal says the phase is complete. Set next action to "wait for HLD approval". | `AGENTS.md` rules 7, 8, 10, 16, 18; `developer.md` lines 34 to 39; spec doc section 3 D to F |
| `dd-writer` | APIs, data models, interfaces, sequencing. State the run environment and set-up requirements explicitly, because task-breakdown depends on them. Diagrams as above. Set next action to "wait for DD approval". | Rules 8, 10, 17, 18; `developer.md` lines 41 to 46 |
| `task-breakdown` | Fill the sections of the TODOS template in order. Environment set-up tasks come before any package install. Add tasks to obtain any repository or download the design needs. Number the tasks so "implement-feature (task K/N)" has an N. Set next action to "run git-workflow (setup)". | Rule 17; `developer.md` lines 48 to 52; `work-items/_TEMPLATE/TODOS.md` |
| `git-workflow` | Three modes. Setup: check for uncommitted changes, fetch, create `feature/WID-<id>`, ask for the commit strategy, record Repo URL, Current branch, Commit strategy. Commit: one conventional commit per task when the strategy is incremental. Commit and PR: merge the latest remote, run the full suite, push, open the PR, record the PR URL. | Rule 11; `developer.md` lines 54 to 81; `implement-feature` lines 61 to 69; `iterative-feature` steps 6 and 9 |

Related edits in the same change:

- `developer.md` lines 76 to 77 tell the agent to ask the user to run the build and tests and wait for confirmation. `AGENTS.md` rules 11 and 14 say the agent runs them. Make `developer.md` say the agent runs the full suite and records the result, and asks the user only when it cannot run the suite itself.
- `implement-feature` line 59 defers to a `test-writer` skill that has never existed. Remove the clause; implement-feature already owns its tests.
- The phase sequence is written three ways. `MyRole.txt` line 20 and `journal-keeper` line 151 leave out diagram-generator and git-workflow. Use the sequence in `developer.md` line 7 everywhere.
- `README.md` and `QUICK-START.md` line 115 say these phases have no skill folders. Update the sentence and add the four folders to the tree at lines 44 to 61.
- The HLD profile documents (D2). If they are not supplied, remove the Part 1 and Extended profiles from `AGENTS.md` rule 8, `README.md` lines 161 to 165, `diagram-generator` line 30, and `journal-keeper` lines 96 to 98 and 108.

### Fix 11. Create the expert memory files, with one entry format

**Problem.**

- None of the six files the skills route to exists, and there is no template for them. The first capture will create a file with whatever header the agent chooses.
- Entry headers are `## YYYY-MM-DD` in `remember` and `promote-facts-rules`, and `### YYYY-MM-DD` in `MEMORY-INDEX.md` and `integrate-docs`. The two work-item templates disagree with each other in the same way.
- The rule format in `integrate-docs` (lines 177 to 194) has no `Triggers:` line. Rules imported in bulk from a document never reach the action hook.
- Entries marked `Workflows: all` are filed "in the developer file ... so every workflow's loader includes it". The loader in `continue` step 0f loads only the pair for the current workflow, so in any other workflow those entries are not loaded.
- Four files are stored with markdown escaped (`\#`, `\*\*`, `\[`, doubled blank lines): `facts/MEMORY-INDEX.md`, `facts/HOW-MEMORY-LOADING-WORKS.md`, and both files in `work-items/_TEMPLATE/facts/`. Headings do not render, and a new work item's facts files begin with syntax the entry parsers do not match. `docs/spec-to-artifacts-agent-skills-system.md` has the same damage.

**Change.**

- Create `facts/facts-developer.md`, `facts/rules-developer.md`, `facts/facts-shared.md`, and `facts/rules-shared.md` (D4), each with a title, one sentence on what belongs in it, and a link to the entry format in `MEMORY-INDEX.md`.
- In `continue` step 0f, `spec-parser` step 1, `implement-feature` step 0, and `iterative-feature` step 0: load the shared pair as well as the workflow pair. In `remember` (lines 20 to 23 and 204 to 205), `promote-facts-rules` (lines 23 to 26 and 77 to 79), and `integrate-docs` (the routing table at lines 203 to 208): route `Workflows: all` to the shared pair and replace "operations" with "shared".
- Use `### YYYY-MM-DD: Title` everywhere. Edit `remember` lines 142, 176, and 210, `promote-facts-rules` line 82, and the work-item rules template.
- Add `**Triggers:**` to the `integrate-docs` rule format, add the trigger question to its step 3, and add "regenerate the trigger index" to its step 6.
- In `build_trigger_index.py`, read every `facts/rules-*.md` instead of the three names on line 10.
- Rewrite the two work-item fact templates by hand (they are about 30 lines each). For the three longer files, strip the backslash before markdown punctuation outside code blocks, collapse the doubled blank lines, replace `&#x20;` with a space, and review the diff, since a mechanical pass can damage Windows paths.

### Fix 12. Remove leftovers, and make `AGENTS.md` agree with the skills

**Problem.** The scaffold was cut down from a populated expert for a different job, and pieces remain. The agent is told about files, workflows, dashboards, and history that do not exist here. `AGENTS.md`, the one file loaded on every turn, still describes the older layout in several rules.

**Change, part 1: `AGENTS.md`.**

| Rule | Line | Today | Change to |
| --- | --- | --- | --- |
| 3 | 9 | Artifact path `docs/facts/` | Remove; facts live in `facts/` and `work-items/<id>/facts/` |
| 15 | 33 | "structured markdown files (`facts/facts.md`, `facts/rules.md` ...)" | The workflow and shared files under `facts/`, or `work-items/<id>/facts/` |
| 16 | 35 | "folloWID-up" | "follow-up" |
| 19 | 41 | "All state (journal, design docs, diagrams, tasks) stored in `work-items/<work-item-id>/`", top-level `facts/facts.md, facts/rules.md`, and "Active Work Item ID stored in `.cursor/active-work-item.txt`" | Artifacts in `work-items/<id>/`, journal in `journals/work-items/<id>/` as rule 2 says, expert memory in `facts/`, active work item in `.cursor/active-context.txt` |
| 23 | 49 | "Commit Expert Role facts/rules.md" | "Commit the changed files under `facts/`" |

**Change, part 2: a search-and-replace that went wrong.** At some point "ID" was inserted between a "w" and a following hyphen across the files. Reverse it: `workflowID-` becomes `workflow-`, `WorkflowID-` becomes `Workflow-`, `newID-workflow` becomes `new-workflow`.

| File | Lines |
| --- | --- |
| `.cursor/workflows/README.md` | 7, 28, 38 to 40, 42, 56, 60, 62, 65, 69, 76, 78, 79, 100, 148, 167, 179 |
| `.cursor/CONTEXT-SYSTEM.md` | 42 |
| `scripts/memory/build_trigger_index.py` | 2 |

Line 7 of the workflows README matters most: it names the registry file as `workflowID-registry.json`, which does not exist.

**Change, part 3: documents that describe a memory this scaffold does not have.**

- `facts/HOW-MEMORY-LOADING-WORKS.md` (490 lines): replace with about 40 lines that describe the mechanism only. Today it reports line counts (3,423), timings ("7 min → 2 min"), an `incident-sessions/` folder, an `active-incident.txt` file, and a quotation of "AGENTS.md rule #21" that is not in `AGENTS.md`.
- `facts/MEMORY-INDEX.md`: remove the dashboard and team names (line 55), the NUnit and build-log paths (line 79), and the "typical context load" figures.
- `remember` lines 17 to 19: remove "since 2027-01-01", a date still in the future, and the two archive file names. Lines 279 to 280 still offer `docs/facts/captured.md`, which the README says is not used; delete them.
- `integrate-docs` lines 27 and 214 cite `domain-knowledge.md` and `scheduling-schema.md` as an existing pattern; neither exists. Lines 95 to 123 list the earlier role's domains.
- `memory-optimize` line 334 cites a lesson from `WID-22953979`.
- `spec-parser` line 34 and `.cursor/workflows/README.md` lines 17 and 120 to 137 name the earlier role's dashboards and teams.
- `.cursor/workflows/README.md` lines 46 to 52 describe `spec-parser.md` and `hld-writer.md` behaviour switches; line 151 loads `facts/facts.md` and `facts/rules.md`. `developer.md` lines 38, 45, 66, and 83 also name `facts/rules.md`, and line 83 is a heading with nothing under it.
- Three files name the rules hook as `inject-rules-on-action.sh`; it is `inject_rules_on_action.py`: `facts/MEMORY-INDEX.md` line 23, `remember` line 126, and `build_trigger_index.py` line 90 (which writes it into the generated `TRIGGER-INDEX.md`).

The examples in `remember` that mention T-SQL and `c:\projects\main_app` are only illustrations. Replacing them with neutral ones is optional.

**Change, part 4: the production-incident workflow (D3).**

- Write `.cursor/workflows/production-incident.md` with the phases, gates, and artifact paths already listed in `continue` lines 109 to 114. Do not add it to the registry.
- Make the other two phase lists match it: `MyRole.txt` line 38 and `define-role` question 5.
- Replace the incident questions in `spec-parser` lines 31 to 35 and `workflow-selector` lines 41 and 63 to 65 with neutral ones (what is affected, who has escalated, where the evidence is).

**Check.** Searching for `[a-z]wid-` (ignoring case), `2027-`, `facts/facts.md` outside `work-items/`, and `-operations.md` should find nothing. Today the first pattern finds 21 lines in four files.

## Group D: keeping it fixed

### Fix 13. An integrity check, run on every commit

**Problem.** Almost every item above is a reference that went stale when something was renamed or removed: a skill name, a path, a trigger token. Nothing detects that, so it will recur with the next change.

**Change.** Add `scripts/check_scaffold.py`, standard library only, exiting non-zero on any finding:

1. Every skill named in `AGENTS.md`, the skills, the workflow files, `MyRole.txt`, and the README has a folder under `.cursor/skills/`.
2. Every backticked repository path in those files exists, after treating `<id>`, `<WID>`, and similar placeholders as wildcards against the templates. Paths that are created at run time (for example `.cursor/role-skills.md`) go in a short allow-list inside the script.
3. Every `instruction_file` in `workflow-registry.json` exists.
4. Every trigger token that appears in a skill or in `MEMORY-INDEX.md` is in the hook's `KNOWN_TOKENS`.
5. No markdown file has a line that starts with an escaped `\#`.
6. The text patterns from the check in fix 12 are absent.
7. `README.md` and `QUICK-START.md` are identical, if both are kept.

Add `.github/workflows/scaffold.yml` (the remote is on GitHub) that runs the check and the test scripts on `windows-latest` and `ubuntu-latest`. Running on Windows from a fresh checkout is what would have caught fix 1.

## Order of work

| Step | Fixes | Depends on | Size |
| --- | --- | --- | --- |
| 1 | 1, 2, 3, 4, 6 | Nothing | Small. Two new files, two code files, one skill file |
| 2 | 5 | D5 | Small. Two code files, three documents, one test |
| 3 | 7, 8 | D6, D7 | Medium. Eleven skills, three documents, two templates. Text only |
| 4 | 9 | Step 3 | Large. About 540 lines of shell ported to Python, plus a new test |
| 5 | 11 | D4 | Medium. Four new files, seven skills, five files to un-escape |
| 6 | 10, 12 | D1, D2, D3 | Large. Four new skills, one new workflow file, edits across most documents |
| 7 | 13 | Steps 1 to 6 | Medium. One script, one CI file. It will fail until the earlier steps are done, which is the point |

Steps 3 and 6 both edit most of the skill files. Doing step 3 first keeps each change reviewable: paths only, then content.

## What was tested, and what was not

Tested in throwaway clones under the system temp folder, which I have since deleted:

- Fix 1: the failure on a fresh clone, and the same clone working after `.gitattributes` was added.
- Fix 3: the field reader on nine line formats, and the hook end to end on copies of the real templates.
- Fix 5: eleven classifier cases against the patched code.
- Fix 6: the counting pattern only.
- Fix 9: the faults in the current scripts, by running them. The replacement is not written.
- Both existing test scripts pass against the patched hooks.

Not tested, because not yet written: the Python port (fix 9), the four skills (fix 10), the memory files and un-escaping (fix 11), the clean-up edits (fixes 7, 8, 12), and the integrity check (fix 13). Line numbers are from the files as they are today and will shift as edits are applied; apply each file's edits from the bottom up, or re-search before each one.
