# Workflow Framework

The expert uses a workflow framework to support different types of work with specialized phase sequences, approval gates, and rules.

## Available Workflows

Enabled workflows are listed in `workflow-registry.json`. Until `define-role` changes it, the registry holds one entry:

1. **Developer Pipeline** (`developer`)
   - Full SDLC: spec → HLD → DD → implementation → testing
   - Use for: new features, greenfield projects, planned enhancements
   - Approval gates: HLD approval, DD approval, feature design approval
   - Artifacts: `docs/design/`, `docs/diagrams/`, `TODOS.md`

Defined but **not enabled** (not in the registry; `define-role` adds it only on an explicit yes):

2. **Production Incident Response** (`production-incident`) — see `production-incident.md`
   - Urgent response: assess → analyze → mitigate → monitor → resolve
   - Use for: production incidents, urgent bugs, escalations
   - No HLD/DD phases
   - Approval gates: fix approach approval, deployment approval
   - Artifacts: `docs/incident/`

## How It Works

### 1. Workflow Selection

When starting a new Work Item:
1. The `continue` skill calls the `workflow-selector` skill
2. The user selects a workflow by number or name
3. Workflow type is stored in the work item journal: `Workflow type: developer`
4. Initial phase is set from the registry (e.g. "spec" for developer)

### 2. Workflow Execution

During Work Item execution:
1. `continue` reads the workflow type from the journal
2. It loads the workflow instruction file (e.g. `.claude/workflows/developer.md`)
3. It executes phases according to the workflow-specific sequence
4. It applies the workflow-specific approval gates
5. It uses the workflow-specific artifact organization

### 3. Workflow-Aware Skills

Skills check the workflow type and adjust behavior:

**`spec-parser`:**
 - developer: write to `docs/design/requirements-summary.md`
 - production-incident: write to `docs/incident/assessment.md`, ask incident-specific questions

**`hld-writer`:**
 - developer: execute the HLD phase
 - production-incident: skip HLD, set next action to "run analyze-root-cause"

**`journal-keeper`:**
 - preserves the workflow type field across updates
 - tracks workflow-specific context fields

## Adding New Workflows

1. **Add to the registry** (`workflow-registry.json`):
```json
"new-workflow": {
  "name": "New Workflow Name",
  "description": "Brief description",
  "instruction_file": ".claude/workflows/new-workflow.md",
  "initial_phase": "first-phase"
}
```
2. **Create the workflow file** (`.claude/workflows/new-workflow.md`):
   - Phase sequence
   - Approval gates
   - Artifact organization
   - Phase behaviors
   - Rules to load

3. **Update workflow-aware skills** (if needed):
   - Add the new workflow to the skill's behavior switch
   - Define workflow-specific artifact paths
   - Add workflow-specific questions

4. **Add a memory pair** if the workflow has its own rules: `facts/facts-<workflow>.md` and `facts/rules-<workflow>.md`.

5. **Test:**
   - Start a new Work Item
   - Select the new workflow
   - Verify phases execute correctly
   - Verify artifacts are created in the correct locations

## Backward Compatibility

If the journal has an old "Pipeline" field but no "Workflow type":
 - Map "developer" → "developer"
 - Map "adhoc-incident" → "production-incident"
 - Map any other name → "developer" (default)

If the journal is missing both fields:
 - Default to the "developer" workflow
 - Prompt the user to confirm or change

---

## Workflow-Specific Facts and Rules

Facts and rules can be scoped to specific workflows using the **Workflows:** metadata field. Skills then load only the entries relevant to the current workflow.

### Metadata Format

```markdown
### YYYY-MM-DD: Title
**Scope:** expert-role
**Workflows:** production-incident
**Captured:** YYYY-MM-DD
**Source:** [Optional]
**Rule:** [content]
```

**Field values:**
 - `all` - applies to all workflows (default if the field is missing). Stored in the shared pair.
 - `developer` - only the developer workflow
 - `production-incident` - only the incident workflow
 - `production-incident, developer` - several workflows (comma-separated)

### Where Entries Are Stored

| Workflows | File pair |
| --- | --- |
| `all` | `facts/facts-shared.md`, `facts/rules-shared.md` |
| `developer` | `facts/facts-developer.md`, `facts/rules-developer.md` |
| `production-incident` | `facts/facts-incident-response.md`, `facts/rules-incident-response.md` (created with that workflow) |

### Filtering Behavior

Skills load facts and rules with workflow-based filtering:

1. Read the current workflow type from the journal (`Workflow type: developer`)
2. Load `facts/MEMORY-INDEX.md`, then the shared pair, then the pair for the current workflow
3. Load the work item pair: `work-items/<id>/facts/facts.md` and `rules.md` (not filtered)
4. For each Expert Role entry:
   - Extract the `**Workflows:**` field (default "all" if missing)
   - Parse the comma-separated list
   - Include the entry if "all" or the current workflow matches
   - Discard it otherwise
5. Internalize only the filtered entries
6. Log to the journal: "Loaded X facts (Y total) and Z rules (W total) for [workflow] workflow"

### When in Doubt

Default to `**Workflows:** all`. Loading a rule in every workflow is better than missing it where it is needed. Refine applicability later by editing the entry.

### Capturing Workflow-Specific Facts and Rules

When `remember` captures an Expert Role entry it asks which workflows it applies to:
 - Default to the current workflow (from the Work Item journal)
 - The user can override to "all", a specific workflow, or a comma-separated list

When `promote-facts-rules` runs:
 - Default to the parent Work Item's workflow
 - The user can generalize to "all" or specify other workflows

When `integrate-docs` runs:
 - Ask for workflow applicability during classification
 - Default to "all" unless the content is clearly workflow-specific
