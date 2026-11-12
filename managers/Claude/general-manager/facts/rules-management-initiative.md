# Rules: Management Initiative

### 2026-10-08: A decision names the decider and the date

**Scope:** expert-role

**Workflows:** management-initiative

**Triggers:** decision:log

**Captured:** 2026-10-08

**Source:** starter pack

**Rule:** Every decision records who decided and the date.

**Why:** An undated, unowned decision will be reopened.

**How to apply:** Write the decider and the date in the decision log before calling the action done.

### 2026-10-08: Status states the outcome, the risk, and the ask

**Scope:** expert-role

**Workflows:** management-initiative

**Triggers:** status:update

**Captured:** 2026-10-08

**Source:** starter pack

**Rule:** A status update states the outcome, the risk, and the ask.

**Why:** A narrative without an ask does not move the work.

**How to apply:** Use those three parts in that order.

### 2026-10-08: Charter and plan gates are not skipped

**Scope:** expert-role

**Workflows:** management-initiative

**Triggers:** cadence:review

**Captured:** 2026-10-08

**Source:** starter pack

**Rule:** Do not start kickoff or execute actions until the charter and the operating plan are approved or the operator explicitly skips that gate.

**Why:** A cadence built on an unapproved outcome wastes attention.

**How to apply:** If the next action is a wait, re-prompt. Continue is not approval.

### 2026-10-08: People notes stay on the work item

**Scope:** expert-role

**Workflows:** management-initiative

**Triggers:** stakeholder:update

**Captured:** 2026-10-08

**Source:** starter pack

**Rule:** People notes stay on the work item unless the operator explicitly says to store them in expert-role memory.

**Why:** Private topics must not become standing memory by accident.

**How to apply:** Keep the note on the work item. Ask before any expert-role copy.

### 2026-10-08: One owner per action

**Scope:** expert-role

**Workflows:** management-initiative

**Triggers:** decision:log

**Captured:** 2026-10-08

**Source:** starter pack

**Rule:** Each action in the tracker has one owner.

**Why:** Shared ownership hides who will do the work.

**How to apply:** Name one owner. If unknown, record an open question.
