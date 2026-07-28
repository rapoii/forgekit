---
name: forgekit-converge
version: 0.1.0
author: Forgekit
description: "When you need to check progress — compare spec requirements against actual implementation to find gaps, missing features, and incomplete work"
tags: [forgekit, convergence, gap-analysis, spec-compliance]
related_skills: [forgekit-specify, forgekit-implement, forgekit-verify, forgekit-plan]
---

# Forgekit Converge

Spec-vs-implementation gap analysis adapted from Spec Kit. Compares what the spec requires with what actually exists in code, then produces a gap report and appends any remaining work as new tasks.

## When to Use

- Midway through implementation — "how much is actually done?"
- After a long coding session — sanity check before going further
- Before `/forgekit.verify` — find gaps before the formal verification gate
- After merging parallel work — did anything get lost?
- When resuming work on a paused feature
- When you suspect scope creep or drift from the original spec

## Steps

### Step 1: Load the Spec

1. Read the feature spec from `.forgekit/specs/<feature>/spec.md`.
2. Extract every requirement into a checklist:
   - Functional requirements (what it must DO)
   - Non-functional requirements (performance, security, etc.)
   - Acceptance criteria (how to know it's done)
   - API contracts (endpoints, types, schemas)
   - Edge cases explicitly called out in the spec

### Step 2: Survey the Implementation

1. **Read the task list** from `.forgekit/tasks/` — what was planned?
2. **Read the actual code** — what exists?
3. For each spec requirement, find the corresponding code:
   - Which file(s) implement it?
   - Which tests verify it?
   - Is it complete or partial?

### Step 3: Build the Gap Report

Create `.forgekit/specs/<feature>/convergence.md`:

```markdown
# Convergence Report — <feature>

Generated: <date>

## Summary
- Spec requirements: N
- Implemented: N (X%)
- Partial: N
- Missing: N
- Extra (not in spec): N

## Detailed Analysis

### Fully Implemented ✅
| # | Requirement | Implementation | Tests |
|---|-------------|---------------|-------|
| 1 | User auth   | src/auth.ts  | auth.test.ts |

### Partially Implemented ⚠️
| # | Requirement | What exists | What's missing |
|---|-------------|------------|----------------|
| 2 | Rate limiting | Basic counter | Sliding window, per-IP |

### Missing ❌
| # | Requirement | Notes |
|---|-------------|-------|
| 3 | Audit logging | No code found |

### Extra (not in spec) ➕
| What | Location | Keep? |
|------|----------|-------|
| Cache layer | src/cache.ts | Yes — useful |

## Drift Detected
- <any scope creep, architectural deviations, or design changes from the spec>

## Recommended Actions
1. <prioritized list of what to implement next>
```

### Step 4: Create Missing Tasks

For each gap found:

1. Add a new task file in `.forgekit/tasks/`:
   ```
   [pending] Implement audit logging
   Spec ref: #3 — "All write operations must be logged to audit trail"
   Priority: high
   ```
2. Update the task list to include new items.
3. Re-prioritize if needed — missing security requirements usually outrank missing polish.

### Step 5: Decide Next Action

Based on the gap report:

- **Large gaps (>30% missing):** Return to `/forgekit.implement` with updated tasks
- **Small gaps (<10% missing):** Fix inline or create focused tasks
- **No gaps:** Proceed to `/forgekit.verify`
- **Spec itself is wrong:** Document the drift and ask the user whether to update the spec or the code

## Output

- Convergence report at `.forgekit/specs/<feature>/convergence.md`
- Updated task list with any missing work added
- Clear recommendation: continue implementing, fix inline, or verify

## Connected Skills

- **Before:** `/forgekit.specify` — needs a spec to compare against
- **Before:** `/forgekit.implement` — implementation must be underway or complete
- **If gaps found:** `/forgekit.implement` — implement the missing pieces
- **If gaps found:** `/forgekit.plan` — re-plan if significant work remains
- **If no gaps:** `/forgekit.verify` — proceed to formal verification
- **Related:** `/forgekit.debug` — if gaps are caused by bugs

## Pitfalls

- **Don't confuse "done" with "exists."** A file existing doesn't mean the requirement is met. Read the code.
- **Don't ignore partial implementations.** A function that handles happy path but not errors is not complete.
- **Don't skip non-functional requirements.** "Must handle 1000 req/s" is a real requirement — check if benchmarks exist.
- **Don't create tasks for out-of-scope items.** If the code does something extra that the spec doesn't require, flag it but don't create tasks to remove it (unless it violates the constitution).
- **Run this more than once.** Convergence isn't a one-shot check. Run it periodically during long implementations.
