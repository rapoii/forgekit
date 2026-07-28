---
name: forgekit-verify
version: 0.1.0
author: Forgekit
description: "When implementation is complete — run exhaustive verification: all tests pass, all requirements met, constitution compliant"
tags: [forgekit, verification, testing, quality-gate]
related_skills: [forgekit-implement, forgekit-debug, forgekit-finish, forgekit-converge]
---

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
