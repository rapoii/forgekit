---
name: forgekit-implement
version: 0.1.0
author: Forgekit
description: "When tasks are ready and you need to execute — dispatch subagents per task, review each output, commit frequently"
tags: [forgekit, execution, implementation, subagents]
related_skills: [forgekit-tasks, forgekit-tdd, forgekit-review, forgekit-parallel, forgekit-spec, forgekit-constitution]
---

# Forgekit Implement

Subagent-driven execution. For each task: dispatch a fresh subagent, review its output against the spec, commit, then move to the next task. Inspired by Superpowers' approach to autonomous coding.

## When to Use

- After `/forgekit.tasks` has produced a detailed task list
- When you're ready to write actual code
- When you want autonomous execution with quality gates
- For medium-to-large projects where one-shot generation is risky

## Steps

### Setup

1. **Load the task list** from `.forgekit/tasks.md`. If missing, run `/forgekit.tasks` first.

2. **Load supporting context:**
   - `.forgekit/spec.md` — for spec compliance review
   - `.forgekit/constitution.md` — for principle compliance
   - `.forgekit/plan.md` — for architecture context
   - Project's existing code — for style/pattern reference

3. **Verify prerequisites:**
   - All dependencies for Task 1 are satisfied
   - Test framework is set up
   - Project builds/runs (baseline)

### Execution Loop

For each task in `.forgekit/tasks.md`:

4. **Prepare the subagent prompt.** Include:
   - The exact task spec (files, code, verification steps)
   - Relevant spec sections for context
   - Constitution principles to follow
   - Previous task outputs if there are dependencies
   - TDD instructions: RED → GREEN → REFACTOR → COMMIT

5. **Dispatch the subagent.** Each subagent gets:
   - Fresh context (no conversation history pollution)
   - Clear success criteria (verification checklist)
   - Time limit aligned with task estimate
   - Access to the project directory

6. **Wait for completion.** If the subagent fails or times out:
   - Log the failure
   - Analyze what went wrong
   - Retry with adjusted prompt OR mark for human review

7. **Two-stage review** of subagent output:

   **Stage 1 — Spec Compliance:**
   - Does the implementation match the spec requirements?
   - Are all acceptance criteria from the task met?
   - Does it handle edge cases the spec defines?
   - Check against `.forgekit/spec.md` directly

   **Stage 2 — Code Quality:**
   - Does the code follow project conventions?
   - Is the test meaningful (not just "it runs")?
   - Does it violate any constitution principles?
   - Are there obvious issues (hardcoded values, missing error handling)?

8. **If review passes:** Commit with a descriptive message:
   ```
   <type>(<scope>): <description> — forgekit task <N>

   - Implemented: <what>
   - Tests: <test file> passing
   - Spec: <spec section addressed>
   ```

9. **If review fails:**
   - Fix minor issues directly
   - Re-dispatch to a new subagent for medium issues
   - Log blockers and skip for major issues (return later)

10. **Update progress** in `.forgekit/progress.md`:
    ```markdown
    - [x] Task 1: Project scaffold — completed
    - [x] Task 2: CLI entry point — completed
    - [ ] Task 3: Config loader — in progress
    - [ ] Task 4: Config validation — pending
    ```

### Completion

11. **After all tasks:** Run the full test suite one final time.
12. **Generate implementation summary** — what was built, what's next.
13. **Suggest** `/forgekit.review` for a comprehensive review.

## Output

- Implemented code in the project directory
- Tests passing for each task
- Git commits after each task
- `.forgekit/progress.md` tracking completion
- Final implementation summary

## Connected Skills

- **← Prerequisite**: `/forgekit.tasks` (detailed task list)
- **← Context**: `/forgekit.spec`, `/forgekit.plan`, `/forgekit.constitution`
- **→ Next**: `/forgekit.review` (comprehensive review)
- **→ Optional**: `/forgekit.tdd` as inner loop, `/forgekit.parallel` for fan-out
- **→ Optional**: `/forgekit.debug` if issues arise

## Examples

### Dispatching a subagent for a task
```
Agent: Implementing Task 5/14: Parse config YAML

       Dispatching subagent with:
       - Task spec from .forgekit/tasks.md#task-5
       - Spec section 3.2 (Configuration)
       - Constitution: "Explicit over implicit"

       Subagent running...

       Subagent completed. Reviewing:
       ✓ Spec compliance: Config loader matches spec 3.2
       ✓ Code quality: Clean, typed, follows conventions
       ✓ Tests: 2 tests passing (valid + missing file)
       ✓ Commit: feat(config): add YAML config parser

       Progress: 5/14 tasks complete (36%)
```

### Handling a failed subagent
```
Agent: Implementing Task 8/14: Database migrations

       Subagent failed: timeout after 5 min.

       Analysis: Task was too large — contains 3 separate migrations.
       Splitting into 8a, 8b, 8c and re-dispatching Task 8a...

       Subagent 8a completed. Reviewing... ✓
```

## Pitfalls

- **Subagent context pollution.** Each subagent gets fresh context. Never pass the entire conversation history.
- **Skipping the review.** "The subagent said it works" is not enough. Always verify against spec and quality criteria.
- **Not committing frequently.** Commit after EVERY task. This is your safety net — you can always revert.
- **Monolithic tasks.** If a task takes more than 5 minutes for a subagent, it's too big. Split and retry.
- **Ignoring test failures.** If the full test suite regresses after a task, STOP. Fix before proceeding.
- **Running all tasks without pausing.** After every 3-5 tasks, do a quick sanity check: does the app still build? Do tests still pass?
