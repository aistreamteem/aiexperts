# Rules: Team Escalation

### 2026-10-08: Name who is affected today

**Scope:** expert-role

**Workflows:** team-escalation

**Triggers:** escalation:open

**Captured:** 2026-10-08

**Source:** starter pack

**Rule:** An escalation assessment names who is affected, the decision needed today, and what is watched next.

**Why:** Urgent team issues drift when the decision is vague.

**How to apply:** Fill those three points before asking for response approval.

### 2026-10-08: Response waits for approval

**Scope:** expert-role

**Workflows:** team-escalation

**Triggers:** escalation:open

**Captured:** 2026-10-08

**Source:** starter pack

**Rule:** Do not carry out the response until the operator says I approve the response or Skip response approval.

**Why:** An urgent people or delivery move still needs an explicit yes.

**How to apply:** Set the next action to wait for response approval and stop.

### 2026-10-08: Separate the lasting staffing change

**Scope:** expert-role

**Workflows:** team-escalation

**Triggers:** hiring:loop

**Captured:** 2026-10-08

**Source:** starter pack

**Rule:** A lasting staffing change discovered during an escalation is a change request, not part of the immediate response.

**Why:** Urgent response and standing staffing are different decisions.

**How to apply:** Write the immediate step in the escalation file. Open a change request for the lasting change.

### 2026-10-08: Tell stakeholders in the same step

**Scope:** expert-role

**Workflows:** team-escalation

**Triggers:** status:update

**Captured:** 2026-10-08

**Source:** starter pack

**Rule:** The response includes what is communicated and to whom.

**Why:** Silence is a decision.

**How to apply:** Name the audience and the message in the response before monitoring starts.

### 2026-10-08: Record what is watched

**Scope:** expert-role

**Workflows:** team-escalation

**Triggers:** escalation:open

**Captured:** 2026-10-08

**Source:** starter pack

**Rule:** Monitoring names the signal and the next check time.

**Why:** A response without a watch item looks finished when it is not.

**How to apply:** Write the signal and the time into the escalation file.
