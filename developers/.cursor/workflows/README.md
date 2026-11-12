# Workflow Framework

The expert uses a workflow framework to support different types of work with specialized phase sequences, approval gates, and domain rules.

## Available Workflows

Defined in `workflow-registry.json` (only enabled workflows appear in workflow-selector):

1. **Developer Pipeline** (`developer`)
 - Full SDLC: spec → HLD → DD → implementation → testing
 - Use for: New features, greenfield projects, planned enhancements
 - Approval gates: HLD approval, DD approval
 - Artifacts: `docs/design/`, `docs/diagrams/`, `TODOS.md`
 - File: `.cursor/workflows/developer.md`

2. **Production Incident Response** (`production-incident`)
 - Urgent response: assess → analyze → mitigate → monitor → resolve
 - Use for: Production incidents, urgent bugs, hotfixes
 - NO HLD/DD phases (fast response required)
 - Approval gates: Fix approach approval, deployment approval
 - Artifacts: `docs/incident/`
 - File: `.cursor/workflows/production-incident.md` (exists; add to the registry only when define-role enables it)


## How It Works

### 1. Workflow Selection

When starting a new Work Item:
1. `continue` calls the `workflow-selector` skill
2. User selects workflow by number or name
3. Workflow type stored in journal: `Workflow type: developer | production-incident`
4. Initial phase set from registry (e.g., "spec" for developer)

### 2. Workflow Execution

During Work Item execution:
1. `continue` reads workflow type from journal
2. Loads workflow instruction file (e.g., `.cursor/workflows/developer.md`)
3. Executes phases according to workflow-specific sequence
4. Applies workflow-specific approval gates
5. Uses workflow-specific artifact organization

### 3. Workflow-Aware Skills

Skills check workflow type and adjust behavior:

**`spec-parser`:**
 - developer: Write to `docs/design/requirements-summary.md`
 - production-incident: Write to `docs/incident/assessment.md`, ask neutral incident questions (what is affected, who escalated, where the evidence is)

**`hld-writer`:**
 - developer: Execute HLD phase
 - production-incident: SKIP HLD → set next action to "run analyze-root-cause"

**`journal-keeper`:**
 - Preserves workflow type field across updates
 - Tracks workflow-specific context fields

## Adding New Workflows

1. **Add to registry** (`workflow-registry.json`):
```json
"new-workflow": {
"name": "New Workflow Name",
"description": "Brief description",
"instruction_file": ".cursor/workflows/new-workflow.md",
"initial_phase": "first-phase"
}
```
2. **Create workflow file** (`.cursor/workflows/new-workflow.md`):
 - Phase sequence
 - Approval gates
 - Artifact organization
 - Phase behaviors
 - Domain rules

3. **Update workflow-aware skills** (if needed):
 - Add new workflow to skill's behavior switch
 - Define workflow-specific artifact paths
 - Add workflow-specific questions

4. **Test:**
 - Start new Work Item
 - Select new workflow
 - Verify phases execute correctly
 - Verify artifacts created in correct locations

## Backward Compatibility

If journal has old "Pipeline" field but no "Workflow type":
 - Map "developer" → "developer"
 - Map "adhoc-incident" → "production-incident"
 - Map "custom-pipeline-name" → "developer" (default)

If journal missing both fields:
 - Default to "developer" workflow
 - Prompt user to confirm or change

---

## Workflow-Specific Facts and Rules

Facts and rules can be scoped to specific workflows using the **Workflows:** metadata field. Skills load the **shared** pair plus the pair for the current workflow.

### Metadata Format

```markdown
### YYYY-MM-DD: [Label/Title]
**Scope:** expert-role
**Workflows:** production-incident
**Triggers:** none
**Captured:** YYYY-MM-DD
**Source:** [Optional]
```

**Field values:**
 - `all` - Stored in the shared pair; loaded in every workflow
 - `production-incident` - Incident response workflow
 - `developer` - Feature development workflow
 - `production-incident, developer` - Multiple workflows (comma-separated); use the primary workflow file, or a shared/reference doc for large cross-cutting material

### Filtering Behavior

1. Read current workflow type from journal (`Workflow type: developer`)
2. Load `facts/facts-shared.md` + `facts/rules-shared.md`, then the workflow pair (e.g. `facts-developer.md` / `rules-developer.md`)
3. For each entry, include it when `Workflows:` is `all` or lists the current workflow
4. Log loaded labels to the journal via journal-keeper

**Backward compatibility:** Entries without `**Workflows:**` default to "all".

### Capturing Workflow-Specific Facts/Rules

When using `remember`, `promote-facts-rules`, or `integrate-docs`, ask which workflows apply. Default to the current workflow (or `all` when unclear). Route `all` to the shared pair.
