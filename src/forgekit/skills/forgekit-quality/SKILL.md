---
name: forgekit-quality
version: 0.1.0
author: Forgekit
description: "Macro-skill for forgekit-quality phase. Combines: review, receiving-review, verify, converge, analyze, checklist, complexity"
tags: [forgekit, quality]
---

# Forgekit Quality

This is a consolidated macro-skill for Forgekit to optimize context length.
It contains the instructions for multiple related phases. Read the specific section for your current phase.

## FORGEKIT-REVIEW
# Forgekit Review

Comprehensive two-dimensional code review: (1) Does the code match the spec? (2) Is the code quality good? Cross-references the constitution and generates a structured review report.

## When to Use

- After `/forgekit.implement` completes all tasks
- Before merging or shipping
- After major refactors to verify nothing regressed
- When a human reviewer will review the PR — pre-review yourself first
- Periodically during long implementation sprints

## Steps

1. **Load all context:**
   - `.forgekit/spec.md` — the source of truth
   - `.forgekit/constitution.md` — project principles
   - `.forgekit/plan.md` — architecture decisions
   - `.forgekit/tasks.md` — what was supposed to be built
   - `.forgekit/progress.md` — what was actually built
   - The actual codebase

2. **Dimension 1 — Spec Compliance Review:**

   For each requirement in the spec:
   - [ ] Is it implemented? (not just planned)
   - [ ] Does the implementation match the acceptance criteria?
   - [ ] Are edge cases from the spec handled?
   - [ ] Are error cases from the spec handled?
   - [ ] Is the data model correct per the spec?
   - [ ] Are the non-functional requirements met (performance, security)?

   Cross-reference with `.forgekit/checklist.md` — did any previously-passing items regress?

3. **Dimension 2 — Code Quality Review:**

   ### Structure
   - [ ] Single responsibility per module/class/function
   - [ ] Clear module boundaries
   - [ ] No god files (>300 lines in a single module)
   - [ ] Consistent naming conventions

   ### Correctness
   - [ ] Error handling is present and meaningful
   - [ ] No silent failures (catching exceptions without handling)
   - [ ] Input validation at boundaries
   - [ ] No hardcoded values that should be configurable

   ### Testing
   - [ ] Tests exist for all public interfaces
   - [ ] Tests cover happy path AND error path
   - [ ] No flaky tests (random order, no shared state)
   - [ ] Test names describe behavior, not implementation

   ### Maintainability
   - [ ] Code is readable without comments (or comments explain WHY, not WHAT)
   - [ ] No dead code
   - [ ] No TODOs without tracking issues
   - [ ] Dependencies are pinned/documented

   ### Constitution Compliance
   - [ ] Every constitution principle is followed
   - [ ] Flag any violations with severity

4. **Generate the review report** in this format:

   ```markdown
   # Forgekit Review Report
   Generated: <date>
   Commit range: <first>..<last>

   ## Summary
   - Spec compliance: X/Y requirements met (Z%)
   - Code quality: X issues found (N critical, M warning, L nit)
   - Constitution: N violations

   ## Spec Compliance Details
   | Requirement | Status | Notes |
   |-------------|--------|-------|
   | REQ-001 | ✅ | Fully implemented |
   | REQ-002 | ⚠️ | Missing edge case: empty input |
   | REQ-003 | ❌ | Not implemented |

   ## Code Quality Issues
   ### 🔴 Critical (must fix)
   1. `src/auth.py:45` — Password stored in plaintext
      Fix: Use bcrypt for password hashing

   ### 🟡 Warning (should fix)
   1. `src/config.py:12` — Hardcoded timeout value
      Fix: Move to config

   ### 🟢 Nit (nice to fix)
   1. `src/utils.py:8` — Variable name `x` is too short
      Fix: Rename to `retry_count`

   ## Constitution Violations
   1. "Explicit over implicit" — `src/api.py:30` uses magic number 42

   ## Recommendations
   1. <actionable recommendation>
   2. <actionable recommendation>
   ```

5. **Save** the report to `.forgekit/review.md`.

6. **Report summary** to the user with pass/fail verdict:
   - ✅ **PASS** — Ready to ship (0 critical issues)
   - ⚠️ **CONDITIONAL PASS** — Ship after fixing criticals
   - ❌ **FAIL** — Significant gaps, needs rework

## Output

`.forgekit/review.md` — structured review report with:
- Spec compliance matrix
- Code quality issues (categorized by severity)
- Constitution violations
- Actionable recommendations
- Pass/fail verdict

## Connected Skills

- **← Prerequisite**: `/forgekit.implement` (code must exist to review)
- **← Context**: `/forgekit.specify`, `/forgekit.constitution`, `/forgekit.checklist`
- **→ Next**: `/forgekit.verify` (run verification suite) or `/forgekit.debug` (fix issues)
- **→ Parallel**: `/forgekit.receiving-review` if sharing with human reviewers

## Examples

### Clean review
```
Agent: Running forgekit review...

       Spec Compliance: 12/12 requirements met (100%)
       Code Quality: 0 critical, 1 warning, 3 nits
       Constitution: 0 violations

       Verdict: ✅ PASS — Ready to ship

       Report saved to .forgekit/review.md
```

### Review with issues
```
Agent: Running forgekit review...

       Spec Compliance: 10/12 requirements met (83%)
       - REQ-007: Missing error handling for timeout
       - REQ-011: Edge case not handled (null user)

       Code Quality: 2 critical, 4 warnings, 7 nits

       Verdict: ❌ FAIL — 2 critical issues, 2 missing requirements

       Recommended: /forgekit.debug to address criticals, then re-review.
```

## Pitfalls

- **Reviewing only code quality, not spec compliance.** Beautiful code that doesn't meet the spec is useless. Both dimensions matter equally.
- **Being too lenient.** The review exists to catch issues before humans do. Be thorough.
- **Not being actionable.** Every issue needs a specific fix suggestion, not just "this is bad."
- **Reviewing too late.** If you wait until the end of a 50-task sprint, the review will find systemic issues that could have been caught at task 10.
- **Ignoring constitution violations.** The constitution defines project identity. Violations are always at least warnings.

## FORGEKIT-RECEIVING-REVIEW
# Forgekit Receiving Review

Handle incoming code review feedback from humans. Parse review comments, categorize by severity, auto-fix critical issues, discuss suggestions, and track review rounds until approval.

## When to Use

- When a human reviewer leaves comments on a PR or code review
- After sharing `/forgekit.review` output with a team member
- When paste-dumping a review into the chat
- During iterative review rounds until approval

## Steps

1. **Parse the incoming review.** Accept review input in any format:
   - GitHub PR review comments (via API or paste)
   - Inline code comments (file:line — comment)
   - Free-form feedback paragraphs
   - Structured review (like `/forgekit.review` output from a human)

2. **Categorize each comment** into severity levels:

   ### 🔴 Critical (must fix)
   - Bugs or correctness issues
   - Security vulnerabilities
   - Data loss risks
   - Spec violations
   - Breaking changes

   ### 🟡 Suggestion (should consider)
   - Better approaches or patterns
   - Performance improvements
   - Readability improvements
   - Missing edge cases (non-critical)

   ### 🟢 Nit (optional)
   - Style preferences
   - Naming suggestions
   - Minor formatting

   ### ❓ Question (needs answer)
   - Reviewer asking for clarification
   - "Why did you do X this way?"
   - Architecture questions

3. **Load context** for each comment:
   - The source file and line referenced
   - The relevant spec section
   - The constitution principle (if any)
   - The original task spec from `.forgekit/tasks.md`

4. **Generate a response plan:**

   For **critical** issues:
   - Auto-fix immediately if the fix is clear
   - Show the diff to the user for approval
   - Run tests after fixing
   - Commit with message: `fix(review): <description> — from review round N`

   For **suggestions**:
   - Evaluate against the spec and constitution
   - If it improves the code without violating principles: apply
   - If it's a trade-off: present options to the user
   - If it conflicts with the spec: explain why and suggest a spec change instead

   For **nits**:
   - Apply if trivial (rename, format)
   - Skip if disruptive (major refactor for a naming preference)
   - Note in response: "Applied" or "Skipping because <reason>"

   For **questions**:
   - Answer with reference to spec, plan, or constitution
   - If the question reveals a gap in documentation, update the relevant forgekit file

5. **Apply fixes** following the same TDD approach:
   - Write/update test for the fix
   - Implement the fix
   - Run all tests
   - Commit

6. **Generate the review response:**

   ```markdown
   # Review Response — Round N
   Date: <date>

   ## Summary
   - 🔴 Critical: X items — all fixed
   - 🟡 Suggestions: Y items — Z applied, W discussed below
   - 🟢 Nits: V items — U applied, T skipped (reason below)
   - ❓ Questions: R items — answered below

   ## Resolved
   ### 🔴 [file:line] — <original comment>
   **Action**: Fixed in commit <hash>
   **What changed**: <description>

   ### 🟡 [file:line] — <original comment>
   **Action**: Applied — <explanation>

   ## Discussed
   ### 🟡 [file:line] — <original comment>
   **Response**: <explanation of why it wasn't changed, or alternative proposal>

   ### ❓ [file:line] — <original question>
   **Answer**: <answer with references>
   ```

7. **Save** the response to `.forgekit/review-round-N.md`.

8. **Track review rounds** in `.forgekit/review-tracker.md`:
   ```markdown
   | Round | Date | Criticals | Suggestions | Nits | Status |
   |-------|------|-----------|-------------|------|--------|
   | 1 | 2024-01-15 | 3 (3 fixed) | 5 (3 applied) | 8 (6 applied) | Changes pushed |
   | 2 | 2024-01-16 | 0 | 1 (1 applied) | 2 (1 applied) | Approved ✅ |
   ```

9. **Report status** to the user and indicate next step.

## Output

- `.forgekit/review-round-N.md` — response to each review round
- `.forgekit/review-tracker.md` — cumulative review progress
- Code fixes committed to the branch
- Clear status: "Changes pushed" or "Approved ✅"

## Connected Skills

- **← Prerequisite**: `/forgekit.review` (initial self-review) or human review request
- **← Context**: `/forgekit.specify` (for evaluating suggestions), `/forgekit.constitution`
- **→ Next**: `/forgekit.implement` (for applying fixes), then `/forgekit.review` (re-verify)
- **→ Parallel**: `/forgekit.debug` if review reveals bugs

## Examples

### Handling a GitHub PR review
```
User: Here's the review from Sarah:
      - auth.py:45 — "Use bcrypt, not plaintext passwords" (critical)
      - config.py:12 — "Consider using env vars instead of hardcoded" (suggestion)
      - utils.py:8 — "Rename x to retry_count" (nit)
      - "Why did you choose synchronous over async?" (question)

Agent: Categorizing review comments:
       🔴 Critical: 1 — auth.py:45 (security)
       🟡 Suggestion: 1 — config.py:12 (configurability)
       🟢 Nit: 1 — utils.py:8 (readability)
       ❓ Question: 1 — sync vs async architecture

       Applying critical fix:
       - auth.py:45: Replacing plaintext hash with bcrypt
       - Test: test_password_is_hashed_with_bcrypt → PASS
       - Commit: fix(auth): use bcrypt for password hashing — review round 1

       Applying nit:
       - utils.py:8: Renaming x → retry_count
       - Commit: chore: rename loop variable for clarity

       Discussing suggestion (env vars):
       → Constitution says "Explicit over implicit" — hardcoded defaults
         with env var overrides is more explicit than pure env vars.
         Suggesting: keep defaults, add env var override layer.
         User: "Good point, let's keep your approach."

       Answering question (sync vs async):
       → Spec section 2.3 defines request processing. Expected load is
         <100 req/s (spec NFR-001). Sync is simpler and meets requirements.
         If load exceeds spec, async migration is documented in plan.md.

       Review response saved to .forgekit/review-round-1.md
       Status: Changes pushed — awaiting Round 2
```

### Multi-round review until approval
```
Agent: Review Round 2 from Sarah:
       - No criticals
       - 1 suggestion: "Add retry logic for DB connection" (applied)
       - "LGTM, approved ✅"

       Status: ✅ Approved — all review rounds resolved
       Total rounds: 2
       Total fixes: 4 (1 critical, 2 suggestions, 1 nit)
```

## Pitfalls

- **Arguing with the reviewer.** Evaluate each comment objectively against the spec and constitution. If the reviewer is right, fix it. If not, explain with evidence — don't dismiss.
- **Auto-fixing suggestions without analysis.** Not every suggestion is an improvement. Some conflict with the spec or introduce complexity. Always evaluate first.
- **Losing review history.** Every round must be tracked. You need to know what was fixed in round 1 vs round 2 for accountability.
- **Not running tests after fixes.** A "fix" that breaks other tests isn't a fix. Always run the full suite.
- **Treating nits as criticals.** Nits are optional. Don't spend 20 minutes on a naming preference when there are real issues to address.

## FORGEKIT-VERIFY
# Forgekit Verify

Pre-completion verification gate. Runs the full test suite, checks every requirement against the spec, and validates constitution compliance. Nothing passes to `/forgekit.finish` without a clean verification report.

## When to Use

- After `/forgekit.implement` reports all tasks complete
- After `/forgekit.debug` fixes a bug and you need to confirm no regressions
- Before `/forgekit.finish` — this is the mandatory quality gate
- When you want to check progress against the spec at any point (partial verification)

## Steps

### Step 1: Run All Tests

1. **Unit tests:**
   ```bash
   # Adapt to project's test runner
   npm test          # Node.js
   pytest            # Python
   go test ./...     # Go
   cargo test        # Rust
   ```

2. **Integration tests** (if separate):
   ```bash
   npm run test:integration
   pytest tests/integration/
   ```

3. **Linting and formatting:**
   ```bash
   npm run lint
   npm run format:check
   # or
   ruff check .
   ruff format --check .
   ```

4. **Type checking** (if applicable):
   ```bash
   npx tsc --noEmit
   mypy .
   ```

5. **Record results.** Every test suite must pass. Failures here block everything.

### Step 2: Check Spec Requirements

1. Load the feature spec from `.forgekit/specs/<feature>/spec.md`.
2. For each requirement in the spec:
   - [ ] Does the implementation address it?
   - [ ] Is there a test covering it?
   - [ ] Does the behavior match the spec description?
3. Load the acceptance criteria (usually in the spec or `.forgekit/specs/<feature>/acceptance.md`).
4. For each criterion:
   - [ ] Can you demonstrate it passes?
   - [ ] Is there automated evidence (test output, screenshot, log)?

### Step 3: Check Constitution Compliance

If `.forgekit/constitution.md` exists:

1. **Code quality rules** — does the code follow the constitution's standards?
2. **Architecture rules** — are patterns and boundaries respected?
3. **Testing rules** — minimum coverage, required test types?
4. **Documentation rules** — are public APIs documented?
5. **Forbidden patterns** — anything the constitution explicitly bans?

### Step 4: Check Task Completion

1. Read `.forgekit/tasks/` — every task should be in `done` status.
2. For each completed task, verify its output exists and works.
3. Flag any tasks that are marked done but have incomplete output.

### Step 5: Generate Verification Report

Create `.forgekit/specs/<feature>/verification.md`:

```markdown
# Verification Report — <feature>

## Test Results
- Unit tests: X/Y passing
- Integration tests: X/Y passing
- Lint: clean / N warnings
- Type check: clean / N errors

## Spec Requirements
| # | Requirement | Status | Evidence |
|---|-------------|--------|----------|
| 1 | ...         | ✅     | test_x  |
| 2 | ...         | ✅     | test_y  |
| 3 | ...         | ❌     | missing |

## Acceptance Criteria
| # | Criterion | Status | Evidence |
|---|-----------|--------|----------|
| 1 | ...       | ✅     | ...     |

## Constitution Compliance
- [ ] Code quality
- [ ] Architecture
- [ ] Testing
- [ ] Documentation

## Tasks
- Total: N
- Done: N
- Remaining: N

## Verdict
PASS / FAIL — <summary>
```

## Output

- Verification report at `.forgekit/specs/<feature>/verification.md`
- Verdict: PASS (proceed to `/forgekit.finish`) or FAIL (return to `/forgekit.debug` or `/forgekit.implement`)
- If FAIL: specific items that need attention, with enough context to act on

## Connected Skills

- **Before:** `/forgekit.implement` — implementation must be complete
- **Before:** `/forgekit.debug` — bugs should be fixed before verifying
- **If FAIL:** `/forgekit.debug` — for test failures and bugs
- **If FAIL:** `/forgekit.converge` — for missing requirements
- **If PASS:** `/forgekit.finish` — proceed to cleanup and finalization
- **Alternative:** `/forgekit.converge` — run a gap analysis before full verification

## Pitfalls

- **Don't skip tests.** "It works on my machine" is not verification.
- **Don't ignore warnings.** Lint warnings today become bugs tomorrow.
- **Don't verify in isolation.** Run the FULL suite, not just the files you changed.
- **Don't accept partial pass.** Every requirement must be met. If something can't be met, document why and get explicit approval.
- **Don't forge evidence.** If a test doesn't exist for a requirement, add it — don't mark it as passing.

## FORGEKIT-CONVERGE
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

## FORGEKIT-ANALYZE
# forgekit-analyze

Cross-artifact consistency analysis. Validates the spec against the constitution, checks for gaps, contradictions, and missing requirements. This is the quality gate between specification and planning.

## When to Use

- After specifying, before planning
- User says "analyze spec" or "check spec consistency"
- User wants to validate requirements before implementation
- User suspects gaps in the specification
- Bootstrap skill routes here when spec exists but hasn't been validated

**Do NOT use when:**
- No spec exists → go to `/forgekit.specify` first
- No constitution exists → go to `/forgekit.constitution` first
- User wants to check code against spec → go to `/forgekit.converge`

## Steps

### 1. Check Prerequisites

```bash
ls .forgekit/constitution.md 2>/dev/null
ls .forgekit/spec.md 2>/dev/null
```

Both MUST exist. If either is missing, suggest the appropriate skill.

### 2. Load Artifacts

Read all relevant documents:

```bash
# Required
cat .forgekit/constitution.md
cat .forgekit/spec.md

# Optional context
ls .forgekit/specs/*-brainstorm.md 2>/dev/null
ls .forgekit/specs/*-clarify.md 2>/dev/null
```

### 3. Run Analysis Checks

Perform these checks systematically:

#### Check 1: Constitution Alignment
> Does the spec respect all constitution principles?

| Constitution Principle | Spec Compliance | Notes |
|---|---|---|
| [Principle 1] | ✅ / ⚠️ / ❌ | [Details] |
| [Principle 2] | ✅ / ⚠️ / ❌ | [Details] |

#### Check 2: Requirement Completeness
> Are all necessary requirements present?

- [ ] All user stories have acceptance criteria
- [ ] All acceptance criteria are testable
- [ ] Non-functional requirements are specified
- [ ] Edge cases are addressed
- [ ] Error handling is defined
- [ ] Data model covers all entities
- [ ] API contract covers all endpoints

#### Check 3: Internal Consistency
> Do requirements contradict each other?

- [ ] No conflicting requirements
- [ ] No circular dependencies
- [ ] Priority assignments are consistent
- [ ] User stories don't overlap in scope

#### Check 4: Scope Analysis
> Is the scope well-defined?

- [ ] Out-of-scope items are listed
- [ ] No scope creep from brainstorm → spec
- [ ] MVP is distinguishable from nice-to-haves
- [ ] MoSCoW priorities are reasonable

#### Check 5: Feasibility Flags
> Any red flags for implementation?

- [ ] Requirements aren't contradictory with tech stack
- [ ] Performance targets are realistic
- [ ] Integration points are achievable
- [ ] No undefined external dependencies

#### Check 6: Traceability
> Can every requirement be traced to a user need?

| Requirement | User Story | Business Need | Traceable? |
|---|---|---|---|
| FR-1 | US-1 | [Need] | ✅ |
| FR-2 | US-2 | [Need] | ✅ |
| FR-3 | — | — | ❌ Orphan |

### 4. Compile Analysis Report

Save to `.forgekit/analysis.md`:

```markdown
# Analysis: [Feature Name]

> Date: YYYY-MM-DD
> Spec Version: [version]
> Constitution Version: [version or date]

## Summary

| Check | Status | Issues |
|---|---|---|
| Constitution Alignment | ✅ Pass | 0 issues |
| Requirement Completeness | ⚠️ Warning | 2 gaps |
| Internal Consistency | ✅ Pass | 0 issues |
| Scope Analysis | ✅ Pass | 0 issues |
| Feasibility | ⚠️ Warning | 1 concern |
| Traceability | ❌ Fail | 1 orphan |

**Overall: ⚠️ 3 issues found (1 critical, 2 minor)**

## Issues

### Critical Issues (must fix before planning)

#### Issue C1: [Title]
**Type:** [alignment | completeness | consistency | scope | feasibility | traceability]
**Location:** [Which requirement/user story]
**Description:** [What's wrong]
**Recommendation:** [How to fix]

### Warnings (should fix, not blocking)

#### Issue W1: [Title]
**Type:** [type]
**Location:** [location]
**Description:** [What's wrong]
**Recommendation:** [How to fix]

### Observations (informational)

#### Issue O1: [Title]
**Description:** [Note]

## Detailed Findings

### Constitution Alignment
[Detailed table from Check 1]

### Requirement Completeness
[Detailed findings from Check 2]

### Internal Consistency
[Detailed findings from Check 3]

### Scope Analysis
[Detailed findings from Check 4]

### Feasibility
[Detailed findings from Check 5]

### Traceability
[Detailed table from Check 6]

## Recommendations

1. [Fix critical issue C1]
2. [Address warning W1]
3. [Consider observation O1]

## Next Steps

- [ ] Fix critical issues → update spec
- [ ] /forgekit.analyze (re-run after fixes)
- [ ] /forgekit.plan (when analysis passes)
```

### 5. Present Findings

Summarize to the user:

```
📊 Analysis Complete

✅ Constitution Alignment: Pass
⚠️ Requirement Completeness: 2 gaps found
✅ Internal Consistency: Pass
⚠️ Feasibility: 1 concern
❌ Traceability: 1 orphan requirement

Critical: FR-3 has no user story (orphan requirement)

Fix the critical issue and re-run /forgekit.analyze, or proceed to /forgekit.plan if you
want to address these during planning.
```

### 6. Suggest Next Step

**If critical issues found:**
```
Fix the critical issues first:
1. Update the spec at .forgekit/spec.md
2. Re-run /forgekit.analyze

Or /forgekit.checklist to generate quality gates.
```

**If only warnings/observations:**
```
✅ Analysis passed with minor warnings.

Next steps:
- /forgekit.checklist — generate quality checklist
- /forgekit.plan — create technical architecture
```

### 🛡️ Constitution Tracker Requirement
When generating this document, you MUST append a `## Constitution Compliance Notes` section at the very bottom.
In this section, briefly explain how your output aligns with the project's constitution (or note any deviations).
This ensures the constitution remains an active guardrail throughout development.

## Output

| File | Description |
|---|---|
| `.forgekit/analysis.md` | Full analysis report |

## Connected Skills

- **`/forgekit.specify`** — Input: spec is analyzed
- **`/forgekit.constitution`** — Input: constitution is the reference standard
- **`/forgekit.clarify`** — May need to go back if analysis finds ambiguities
- **`/forgekit.checklist`** — Next step: generate quality gates from analysis
- **`/forgekit.plan`** — Next step: create architecture (when analysis passes)
- **`/forgekit.config`** — Updates phase tracking
- **`/forgekit.converge`** — Later: checks implementation against spec

## Examples

### Example 1: Clean Analysis
```
User: "analyze the spec"
Agent: [reads constitution and spec]
Agent: [runs all 6 checks]
Agent: "📊 Analysis: All checks passed. Spec is ready for planning."
Agent: "Next: /forgekit.plan to create the technical architecture."
```

### Example 2: Issues Found
```
User: "analyze spec"
Agent: [reads constitution and spec]
Agent: "📊 Analysis found 2 issues:"
Agent: "❌ Critical: FR-5 'rate limiting' contradicts constitution's 'no request throttling' rule"
Agent: "⚠️ Warning: US-3 has no acceptance criteria"
Agent: "Should I fix these, or do you want to update the spec manually?"
```

## Pitfalls

- **Both artifacts required.** Analysis without a constitution is just spell-checking. The constitution IS the standard.
- **Don't auto-fix.** Analysis identifies issues — it doesn't rewrite the spec. The user decides how to fix.
- **Be specific about locations.** "Issue in requirements" → bad. "Issue in FR-3, line about authentication" → good.
- **Re-analyze after fixes.** Always suggest re-running analysis after the user updates the spec.
- **Analysis is not a review.** Analysis checks formal consistency. `/forgekit.review` checks implementation compliance. Different things.
- **Keep it structured.** The analysis report should be scannable — tables, checkmarks, clear issue hierarchy.

## FORGEKIT-CHECKLIST
# Forgekit Checklist

Generate a quality checklist FROM the spec — like "unit tests for English." This validates that your requirements are complete, consistent, and testable before you write a single line of code.

## When to Use

- After `/forgekit.specify` has been written and you want to validate it
- Before planning implementation (catch gaps early, fix cheap)
- When a stakeholder asks "is the spec complete?"
- After `/forgekit.analyze` has surfaced questions that need answers

## Steps

1. **Load the spec** from `.forgekit/spec.md`. If it doesn't exist, stop — run `/forgekit.specify` first.

2. **Load the constitution** from `.forgekit/constitution.md` if it exists. Include its principles as checklist constraints.

3. **Load analysis** from `.forgekit/analysis.md` if it exists. Flag any open questions as checklist items that block implementation.

4. **Generate checklist categories.** For each major section of the spec, create these checks:

   ### Clarity
   - [ ] Every requirement uses unambiguous language
   - [ ] No vague terms ("should be fast", "user-friendly", "reasonable")
   - [ ] All referenced entities/concepts are defined
   - [ ] Acceptance criteria use measurable thresholds

   ### Consistency
   - [ ] No contradictions between requirements
   - [ ] Terminology is consistent throughout
   - [ ] Data models don't conflict
   - [ ] Business rules don't contradict each other

   ### Completeness
   - [ ] All user stories have acceptance criteria
   - [ ] All happy paths are described
   - [ ] All error/edge cases are addressed (or explicitly deferred)
   - [ ] All external dependencies are identified
   - [ ] Non-functional requirements are specified (performance, security, etc.)

   ### Testability
   - [ ] Every requirement can be verified by a test
   - [ ] Acceptance criteria produce binary pass/fail
   - [ ] State transitions are defined
   - [ ] Input/output boundaries are specified

   ### Edge Cases
   - [ ] Empty/null inputs handled
   - [ ] Boundary values specified
   - [ ] Concurrent access scenarios considered
   - [ ] Failure/recovery paths defined
   - [ ] What happens when external services are down?

   ### Constitution Compliance
   - [ ] All constitution principles addressed in spec
   - [ ] No violations of project constraints

5. **Score each category** with a pass/fail/needs-work rating. Count unchecked items per category.

6. **Prioritize gaps.** Mark each unchecked item:
   - 🔴 **Blocker** — must resolve before planning
   - 🟡 **Warning** — should resolve before implementation
   - 🟢 **Nice-to-have** — can resolve during implementation

7. **Save** the checklist to `.forgekit/checklist.md`.

8. **Report summary** to the user: total items, pass rate, blockers count.

## Output

`.forgekit/checklist.md` — a structured checklist with:
- Per-category checks (pass/fail)
- Priority ratings for failures
- Suggested resolutions for blockers
- Overall spec readiness score

## Connected Skills

- **← Prerequisite**: `/forgekit.specify` (need a spec to validate)
- **← Optional**: `/forgekit.analyze` (analysis questions inform checklist)
- **→ Next**: `/forgekit.plan` (once checklist is green or blockers resolved)
- **→ Parallel**: `/forgekit.specify` for reworking sections with failures

## Examples

### Generating a checklist after spec creation
```
User: /forgekit.checklist
Agent: Loading spec from .forgekit/spec.md...
       Loading constitution from .forgekit/constitution.md...

       Checklist Summary:
       ━━━━━━━━━━━━━━━━━━
       Clarity:      8/10 pass (2 blockers)
       Consistency:  9/10 pass (1 warning)
       Completeness: 7/12 pass (3 blockers, 2 warnings)
       Testability:  6/8 pass (2 blockers)
       Edge Cases:   5/10 pass (3 blockers, 2 warnings)
       Constitution: 4/4 pass
       ━━━━━━━━━━━━━━━━━━
       Overall: 70% ready — 10 blockers to resolve

       Saved to .forgekit/checklist.md
       Run /forgekit.specify to address blockers, then /forgekit.plan to proceed.
```

### Checklist with no issues
```
User: /forgekit.checklist
Agent: Spec quality: 100% pass — all 44 checks green.
       Ready for /forgekit.plan.
```

## Pitfalls

- **Don't rush past blockers.** A blocker in the checklist will become a bug or rework later. Fix the spec.
- **Don't over-engineer the checklist.** For simple projects, some "nice-to-have" edge cases can be deferred. Mark them explicitly.
- **Re-run after spec changes.** If the spec is updated, regenerate the checklist — old passes may have regressed.
- **Open questions from analysis are automatic blockers.** If `/forgekit.analyze` flagged unknowns and they're still unresolved, they're blockers by definition.

## FORGEKIT-COMPLEXITY
# forgekit-complexity

Track complexity decisions throughout the project lifecycle. Prevents premature abstraction and keeps the codebase lean.

## When to Use

- Adding a new dependency or framework
- Creating a new abstraction layer
- Making architectural decisions with complexity implications
- Reviewing whether existing complexity is justified
- Before merge — check if complexity grew unexpectedly

## Steps

### 1. Score the Decision

Rate each complexity addition on a 1-5 scale:

| Score | Meaning | Action |
|---|---|---|
| 1 | Trivial (config, utility) | Proceed freely |
| 2 | Minor (single library) | Proceed, document |
| 3 | Moderate (new pattern) | Document + consider alternatives |
| 4 | Significant (new subsystem) | Require user approval |
| 5 | Major (architectural change) | Require explicit justification + user approval |

### 2. Document in Constitution

Add to constitution.md complexity table:

```markdown
| Decision | Score | Justification | Status |
|---|---|---|---|
| Add PyYAML | 2 | Replaces buggy hand-rolled parser | Approved |
| Custom workflow engine | 4 | Deferred — use external | Deferred |
```

### 3. Review Periodically

Every 10 tasks or at the end of a feature:
- Are all abstractions still justified?
- Can any be simplified or removed?
- Have any score-4+ decisions become unnecessary?

## Output

| Artifact | Description |
|---|---|
| Complexity table in constitution.md | Running log of all complexity decisions |
| Simplification proposals | If over-complexity detected |

## Pitfalls

- **Don't add complexity "for the future."** YAGNI — build what's needed today.
- **Don't forget to track.** Untracked complexity grows silently.
- **Don't confuse score 2 with score 4.** A single library ≠ a new subsystem.
- **Don't skip periodic reviews.** Complexity compounds; review regularly.
- **Don't remove complexity without user consent.** Some complexity is justified; check before removing.

## Connected Skills

- **`/forgekit.constitution`** — Complexity table lives in constitution
- **`/forgekit.brainstorm`** — Design decisions with complexity trade-offs
- **`/forgekit.specify`** — Requirements may introduce complexity
- **`/forgekit.review`** — Review includes complexity audit

