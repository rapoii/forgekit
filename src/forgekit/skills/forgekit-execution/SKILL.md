---
name: forgekit-execution
version: 0.1.0
author: Forgekit
description: "Macro-skill for forgekit-execution phase. Combines: tasks, implement, tdd, parallel, worktree, debug"
tags: [forgekit, execution]
---

# Forgekit Execution

This is a consolidated macro-skill for Forgekit to optimize context length.
It contains the instructions for multiple related phases. Read the specific section for your current phase.

## FORGEKIT-TASKS
# Forgekit Tasks

Break the implementation plan into a precise, actionable task list. Each task is 2–5 minutes of work, specifies exact file paths, includes complete code snippets, and has verification steps. Ready for subagent dispatch or direct execution.

## When to Use

- After `/forgekit.plan` produces architecture and task outlines
- Before `/forgekit.implement` — subagents need precise task specs
- When the plan's tasks are too vague for autonomous execution
- When converting work to GitHub Issues via `/forgekit.publish`

## Steps

1. **Load the plan** from `.forgekit/plan.md`. If it doesn't exist, run `/forgekit.plan` first.

2. **Load the spec** from `.forgekit/spec.md` for acceptance criteria.

3. **Load the constitution** from `.forgekit/constitution.md` for constraints.

4. **For each plan task**, expand into a detailed task spec:

   ```markdown
   ### Task N: <descriptive title>

   **Goal**: <one sentence — what this task achieves>
   **Files**: <exact paths to create/modify>
   **Dependencies**: <which tasks must complete first>
   **Estimated time**: <2-5 min>

   #### Test (RED)
   ```<lang>
   <complete test code — not pseudocode>
   ```

   #### Implementation (GREEN)
   ```<lang>
   <complete implementation code>
   ```

   #### Refactor Notes
   - <specific refactoring to consider after green>

   #### Verification
   - [ ] Test file created at <path>
   - [ ] Test fails without implementation (RED confirmed)
   - [ ] Implementation at <path> makes test pass
   - [ ] All existing tests still pass
   - [ ] Commit message: `<suggested message>`
   ```

5. **Validate task ordering:**
   - Each task only depends on tasks that come before it
   - No circular dependencies
   - Foundation tasks (config, models, utilities) come first
   - Integration/wiring tasks come after unit tasks

6. **Check task size:**
   - If a task exceeds 5 min of work, split it
   - If a task is under 2 min, consider merging with an adjacent task
   - Target: 2–5 min per task, ~20-30 tasks for a medium project

7. **Add task metadata** for subagent dispatch:
   - `complexity`: low/medium/high
   - `can_parallelize`: true/false (can run alongside other tasks?)
   - `test_only`: true/false (is this a test-writing task?)

8. **Save** to `.forgekit/tasks.md`.

9. **Report** total task count, estimated duration, and parallelization opportunities.

## Output

`.forgekit/tasks.md` containing:
- Ordered task list with full specs
- Each task: goal, files, code, verification
- Dependency graph notes
- Parallelization hints
- Total estimated effort

## Connected Skills

- **← Prerequisite**: `/forgekit.plan` (architecture and task outlines)
- **← Optional**: `/forgekit.specify` (acceptance criteria), `/forgekit.checklist` (validated requirements)
- **→ Next**: `/forgekit.implement` (execute tasks) or `/forgekit.publish` (convert to GitHub Issues)
- **→ Parallel**: `/forgekit.tdd` as the execution method for each task

## Examples

### Task spec for a simple function
```markdown
### Task 5: Parse config YAML

**Goal**: Load and parse a YAML config file into a validated dict
**Files**: `src/config/parser.py`, `tests/config/test_parser.py`
**Dependencies**: Task 4 (project scaffold)
**Estimated time**: 3 min

#### Test (RED)
```python
# tests/config/test_parser.py
import pytest
from src.config.parser import parse_config

def test_parse_config_valid_yaml(tmp_path):
    config_file = tmp_path / "config.yml"
    config_file.write_text("name: test\nversion: 1\n")
    result = parse_config(str(config_file))
    assert result == {"name": "test", "version": 1}

def test_parse_config_missing_file():
    with pytest.raises(FileNotFoundError):
        parse_config("/nonexistent/config.yml")
```

#### Implementation (GREEN)
```python
# src/config/parser.py
import yaml

def parse_config(path: str) -> dict:
    with open(path) as f:
        return yaml.safe_load(f)
```

#### Verification
- [ ] `tests/config/test_parser.py` created
- [ ] RED: tests fail (module not found)
- [ ] GREEN: `parse_config` passes both tests
- [ ] All tests pass
- [ ] Commit: `feat(config): add YAML config parser — TDD`
```

## Pitfalls

- **Vague verification steps.** "Make sure it works" is not a verification step. Specify exact commands: `pytest tests/config/test_parser.py -v`.
- **Missing test code.** Subagents can't infer what to test. Write complete, runnable test code.
- **Tasks with hidden dependencies.** If Task 7 imports from Task 9's output, the order is wrong.
- **Too many parallel tasks.** Just because tasks CAN be parallelized doesn't mean they SHOULD be. Parallel tasks create merge conflicts. Use sparingly.

## FORGEKIT-IMPLEMENT
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
- **← Context**: `/forgekit.specify`, `/forgekit.plan`, `/forgekit.constitution`
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

## FORGEKIT-TDD
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

## FORGEKIT-PARALLEL
# Forgekit Parallel

Dispatch multiple subagents to work on independent tasks simultaneously. Dramatically reduces wall-clock time for large features with separable work items.

## When to Use

- The task list (`.forgekit/tasks/`) has 3+ independent items with no cross-dependencies
- A feature naturally splits into isolated modules (e.g., separate API endpoints, independent UI components, distinct test suites)
- You've confirmed with `/forgekit.plan` that items can be worked in parallel
- Time is a constraint and sequential execution would be too slow

## Steps

### Step 1: Analyze Dependencies

1. Read the current task list from `.forgekit/tasks/`.
2. Build a dependency graph:
   - Which tasks depend on others?
   - Which tasks share files or modules?
   - Which tasks are truly independent?
3. Identify parallelizable groups — sets of tasks with zero shared file modifications.

### Step 2: Prepare Isolation

For code-level parallelism, isolate each agent's work:

1. **Git worktrees** (preferred for multi-file changes):
   ```bash
   git worktree add ../forgekit-agent-1 -b feature/agent-1
   git worktree add ../forgekit-agent-2 -b feature/agent-2
   git worktree add ../forgekit-agent-3 -b feature/agent-3
   ```

2. **Separate directories** (for new files only):
   ```
   src/
     module-a/   ← Agent 1
     module-b/   ← Agent 2
     module-c/   ← Agent 3
   ```

3. **Shared dependencies** must be resolved BEFORE dispatching agents. If agents need a shared interface or types file, create it first.

### Step 3: Dispatch Agents

For each parallel agent, provide:

1. **The specific task** — one item from the task list, with full context.
2. **The working directory** — worktree path or module directory.
3. **The spec excerpt** — only the relevant section of the spec for this task.
4. **The constraints** — shared interfaces, naming conventions, output format.
5. **The completion criteria** — what "done" looks like (tests pass, files created, etc.).

Agent dispatch template:
```
You are working on a forgekit parallel task.

TASK: <task description>
SPEC: <relevant spec section>
WORKDIR: <path>
CONSTRAINTS: <shared interfaces, conventions>
DONE WHEN: <completion criteria>
```

### Step 4: Coordinate Results

As agents complete:

1. **Collect outputs** — each agent reports what it created/modified.
2. **Check for conflicts** — do any agents' changes overlap?
3. **Merge changes** — if using worktrees:
   ```bash
   git merge feature/agent-1 --no-ff
   git merge feature/agent-2 --no-ff
   git merge feature/agent-3 --no-ff
   ```
4. **Resolve conflicts** if any. Conflicts should be rare if Step 1 was done correctly.
5. **Run integration tests** — the individual pieces may work alone but break together.

### Step 5: Finalize

1. Remove worktrees:
   ```bash
   git worktree remove ../forgekit-agent-1
   git worktree remove ../forgekit-agent-2
   git worktree remove ../forgekit-agent-3
   ```
2. Delete merged branches.
3. Proceed to `/forgekit.review` for the combined result.

## Output

- All parallel tasks completed
- Changes merged cleanly into the main working branch
- Integration tests passing
- Ready for `/forgekit.review`

## Connected Skills

- **Before:** `/forgekit.plan` — confirms which items can be parallelized
- **Before:** `/forgekit.specify` — spec must exist with clear per-task requirements
- **During:** `/forgekit.implement` — each agent uses implement logic for its task
- **After:** `/forgekit.review` — review the combined result
- **After:** `/forgekit.verify` — full verification after merge

## Pitfalls

- **Don't parallelize dependent tasks.** If Task B needs Task A's output, they must be sequential.
- **Don't skip shared interface setup.** Agents will create incompatible APIs if you don't define the contract first.
- **Don't forget integration testing.** Individual pass ≠ combined pass.
- **Watch for file-level conflicts.** Even "independent" tasks can collide on config files, package.json, etc.
- **Keep agent count reasonable.** 3-5 agents is practical. More than 7 creates coordination overhead that outweighs the parallelism benefit.

## Example

```
# Feature: E-commerce API with 4 endpoints

## Dependency Analysis
- GET /products    — independent, read-only
- GET /cart        — independent, read-only
- POST /cart       — depends on cart types (shared)
- POST /checkout   — depends on cart + products (sequential, last)

## Parallel Group 1 (with shared types pre-created)
- Agent 1: GET /products (worktree: ../forgekit-agent-1)
- Agent 2: GET /cart (worktree: ../forgekit-agent-2)
- Agent 3: POST /cart (worktree: ../forgekit-agent-3)

## After merge:
- Agent 4 (sequential): POST /checkout (depends on all above)
```

## FORGEKIT-WORKTREE
# forgekit-worktree

Create isolated Git workspaces for feature work. Prevents main branch pollution and enables parallel workstreams.

## When to Use

- Starting a new feature that needs isolation from main branch
- Running multiple features in parallel (one worktree per feature)
- Working on experiments without affecting current branch
- Before dispatching parallel subagents (each gets own worktree)
- Using git worktrees instead of branches when isolation is critical

## Steps

### 1. Check Current Isolation

Before creating a new worktree, check if already isolated:

```bash
# Check if in a worktree
git rev-parse --git-common-dir

# List existing worktrees
git worktree list
```

If already in a worktree, reuse it. Don't create unnecessary duplicates.

### 2. Create Worktree from Feature Branch

```bash
# Create worktree with new branch
git worktree add ../project-feature-001 -b feature/001-my-feature

# Or checkout existing branch in worktree
git worktree add ../project-feature-001 feature/existing-branch
```

Location: sibling directory (../project-<feature-name>/)

### 3. Do Work in Worktree

```bash
cd ../project-feature-001
# All forgekit phases run here
forgekit constitution
forgekit specify
# ... etc
```

### 4. Return and Verify

```bash
cd ../project-original
# Review worktree changes
git -C ../project-feature-001 log --oneline -5
```

### 5. Cleanup After Merge

After work is merged (via forgekit-finish), remove worktree:

```bash
git worktree remove ../project-feature-001
git branch -d feature/001-my-feature  # if merged
```

## Output

| Artifact | Description |
|---|---|
| Isolated worktree directory | Separate working directory for feature |
| Feature branch | Named branch for the feature |
| No main branch pollution | All work isolated until merge |

## Pitfalls

- **Don't create worktrees inside the main repo.** Always use sibling directories (../project-feature-X/).
- **Don't forget to remove worktrees after merge.** `git worktree list` shows all; clean up regularly.
- **Don't run git operations on the same branch in multiple worktrees.** One branch = one worktree.
- **Don't use worktrees for trivial features.** Only when isolation is truly needed (parallel work, risky experiments).
- **Handle detached HEAD carefully.** If worktree shows detached HEAD, create a named branch immediately.

## Connected Skills

- **`/forgekit.finish`** — Merge decision + worktree cleanup
- **`/forgekit.specify`** — Spec generation happens in worktree
- **`/forgekit.implement`** — Subagents can be dispatched to worktrees
- **`/forgekit.parallel`** — Each parallel domain gets own worktree

## Examples

### Example 1: Single feature worktree
```bash
git worktree add ../myapp-auth -b feature/auth
cd ../myapp-auth
forgekit constitution
forgekit specify
forgekit implement
cd ../myapp
git worktree remove ../myapp-auth
```

### Example 2: Parallel features
```bash
# Feature A
git worktree add ../myapp-auth -b feature/auth
# Feature B
git worktree add ../myapp-api -b feature/api

# Each subagent works in own worktree
# Merge sequentially when done
```

## FORGEKIT-DEBUG
# Forgekit Debug

Systematic debugging workflow adapted from Superpowers. Enforces root-cause analysis before fixing so you don't apply band-aids that create new bugs.

## When to Use

- A test fails and the reason isn't obvious
- Runtime behavior doesn't match spec expectations
- An error or exception appears during development or verification
- Performance degrades unexpectedly
- You're tempted to "just try something" — stop and run this instead

## Steps

### Phase 1: Understand

1. **Read the error message carefully.** Copy the full traceback or error output. Don't skim.
2. **Identify what changed.** Run `git diff` or `git log --oneline -5` to see recent work.
3. **Read the relevant spec.** Load the feature spec from `.forgekit/specs/<feature>/spec.md` (if it exists) to understand intended behavior.
4. **Read the relevant code.** Locate the file(s) involved in the error. Read the full function/module, not just the failing line.
5. **Formulate a hypothesis.** Write down what you think is wrong and why. Be specific — "the parser fails on nested arrays because the recursion doesn't check for empty elements" is good; "something's wrong with the parser" is not.

### Phase 2: Reproduce

1. **Create a minimal reproduction.** Strip away everything unrelated. The smallest possible code that triggers the bug.
2. **Confirm the bug reproduces consistently.** Run the reproduction 2-3 times. If it's intermittent, note the conditions.
3. **Confirm the bug is in scope.** Check: is this a pre-existing issue or something your current work introduced? Use `git stash` to test on a clean state if needed.
4. **Document the reproduction steps** in your notes or as a failing test.

### Phase 3: Diagnose

1. **Isolate the root cause.** Use one or more of these techniques:
   - **Binary search:** comment out half the code, see if bug persists, narrow down.
   - **Print/log tracing:** add strategic logging to trace data flow.
   - **Rubber duck:** explain the code line by line (works even in your head).
   - **Compare working vs broken:** diff two versions — one that works, one that doesn't.
2. **Verify your hypothesis.** The root cause should explain ALL observed symptoms, not just one.
3. **Check for related issues.** If the root cause is a pattern (e.g., missing null checks), search the codebase for the same pattern elsewhere.

### Phase 4: Fix

1. **Write a test that fails** because of the bug (if one doesn't already exist).
2. **Make the minimal fix.** Change only what's necessary. Resist the urge to refactor while fixing.
3. **Run the test — confirm it passes.**
4. **Run the full test suite** — confirm no regressions.
5. **Clean up** any debug logging or temporary code you added during diagnosis.

## Output

- Root cause documented (what, where, why)
- Fix applied with a test that prevents regression
- No new failures in the test suite
- If the bug revealed a gap in the spec, note it for `/forgekit.converge`

## Connected Skills

- **Before:** `/forgekit.implement` — bug may have surfaced during implementation
- **After:** `/forgekit.verify` — run full verification after the fix
- **After:** `/forgekit.review` — have the fix reviewed if it was non-trivial
- **Related:** `/forgekit.converge` — if the bug reveals missing spec coverage

## Pitfalls

- **Don't skip Phase 1.** Jumping to "fixing" without understanding is how you introduce new bugs.
- **Don't fix symptoms.** If you're adding a null check somewhere, ask WHY it's null.
- **Don't refactor during a bug fix.** Separate concerns — fix first, refactor later.
- **Don't ignore intermittent bugs.** They're usually race conditions or order-dependent state. Document the conditions.
- **One fix at a time.** If you find multiple bugs, fix and verify each separately.

## Example

```
# Bug: API returns 500 on empty request body

## Phase 1: Understand
- Error: TypeError: Cannot read property 'name' of undefined
- Location: src/handlers/users.js:42
- Spec says: "API should return 400 for invalid input"
- Hypothesis: Request body parsing doesn't handle empty bodies, passes undefined to handler

## Phase 2: Reproduce
- curl -X POST http://localhost:3000/users -H "Content-Type: application/json" -d ''
- Confirmed: 500 every time with empty body

## Phase 3: Diagnose
- bodyParser returns undefined for empty bodies
- Handler assumes req.body is always an object
- Root cause: no validation middleware before handler

## Phase 4: Fix
- Added validation middleware: if (!req.body) return res.status(400).json({error: "Missing body"})
- Test: empty body now returns 400 with descriptive error
- Full suite: all passing
```

