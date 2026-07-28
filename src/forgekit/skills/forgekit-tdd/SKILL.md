---
name: forgekit-tdd
version: 0.1.0
author: Forgekit
description: "When implementing features and you want strict test-driven development — RED, GREEN, REFACTOR cycle with progress tracking"
tags: [forgekit, execution, tdd, testing, implementation]
related_skills: [forgekit-plan, forgekit-implement, forgekit-review, forgekit-tasks]
---

# Forgekit TDD

Strict test-driven development cycle: RED → GREEN → REFACTOR. Use standalone for focused TDD work, or as the execution method within `/forgekit.implement`.

## When to Use

- When the plan calls for TDD-style implementation
- As the inner loop of `/forgekit.implement` for each task
- When you want to ensure test coverage before writing production code
- When refactoring existing code safely (write tests first, then refactor)
- Standalone: when you know what to build and want test-first discipline

## Steps

### RED Phase — Write a Failing Test

1. **Load context:**
   - The current task from `.forgekit/tasks.md` or `.forgekit/plan.md`
   - Relevant spec sections from `.forgekit/spec.md`
   - Existing test patterns from the project

2. **Write the smallest failing test** that proves the next behavior:
   - One assertion per test (ideally)
   - Name the test descriptively: `test_<what>_<when>_<expected>`
   - Place it in the correct test file per the plan's file structure

3. **Run the test.** Confirm it fails with the expected error (not a syntax error or import failure).

4. **If the test doesn't fail** (already passes):
   - The behavior already exists — skip to the next test
   - Or the test is wrong — fix it

### GREEN Phase — Make It Pass

5. **Write the minimal code** to make the failing test pass:
   - No extra features, no "while I'm here" additions
   - Just enough to turn red to green
   - Hardcoding is acceptable if it makes the test pass (you'll refactor next)

6. **Run the test.** Confirm it passes.

7. **Run ALL tests.** Confirm nothing else broke.

### REFACTOR Phase — Clean Up

8. **Refactor** the code you just wrote (and surrounding code):
   - Extract functions, rename variables, improve structure
   - Apply DRY, SOLID, project conventions
   - Run all tests after each refactor step — they must stay green

9. **Commit.** One commit per RED-GREEN-REFACTOR cycle:
   ```
   feat: add <behavior> — test-driven

   - RED: wrote test_<name>
   - GREEN: implemented <function/method>
   - REFACTOR: <what you cleaned up>
   ```

### Repeat

10. **Pick the next test** from the task's requirements. Go back to RED.

11. **Stop when the task is complete** — all behaviors tested and implemented.

## Output

For each TDD cycle:
- A new test in the test suite
- Minimal production code that passes the test
- A clean commit with the test + implementation

Track progress in `.forgekit/progress.md`:
```markdown
## Task 3: Config loader — TDD Progress
- [x] RED: test missing config file → error
- [x] GREEN: ConfigLoader.load() raises FileNotFoundError
- [x] REFACTOR: extract error message to constant
- [x] RED: test valid YAML → parsed dict
- [x] GREEN: ConfigLoader.load() parses YAML
- [ ] RED: test invalid YAML → descriptive error
```

## Connected Skills

- **← Prerequisite**: `/forgekit.plan` (know what to build and test)
- **→ Next**: `/forgekit.implement` (dispatch tasks), `/forgekit.review` (review the code)
- **→ Parallel**: Use within `/forgekit.implement` as the inner loop for each task

## Examples

### TDD for a validation function
```
Agent: TDD Cycle — validate_email()

RED: Writing test...
     def test_validate_email_rejects_empty_string():
         with pytest.raises(ValueError, match="Email cannot be empty"):
             validate_email("")

     Running: FAILED (NameError: validate_email not defined) ✓ expected

GREEN: Implementing...
     def validate_email(email: str) -> str:
         if not email:
             raise ValueError("Email cannot be empty")
         return email

     Running: PASSED ✓

REFACTOR: No cleanup needed yet — function is minimal.

Commit: feat: validate_email rejects empty input — test-driven
```

### TDD when test already passes
```
Agent: RED: Writing test...
       def test_user_has_default_role():
           user = User(name="Alice")
           assert user.role == "viewer"

       Running: PASSED — this behavior already exists.
       Skipping to next test.
```

## Pitfalls

- **Writing too many tests at once.** One test, one implementation, one commit. Batch RED phases only if the tests are truly independent assertions of the same behavior.
- **Testing implementation details.** Test behavior (inputs → outputs), not internal structure. If you rename a private method and tests break, the tests are too coupled.
- **Skipping REFACTOR.** The refactor phase is where code quality lives. Skipping it accumulates technical debt.
- **Not running all tests in GREEN.** A new implementation can break existing code. Always run the full suite.
- **Committing before GREEN.** Never commit red tests to main. Use a branch or stash if you need to pause.
