---
name: forgekit-parallel
version: 0.1.0
author: Forgekit
description: "When a task list has multiple independent items — dispatch parallel subagents to work on them simultaneously"
tags: [forgekit, parallel, multi-agent, concurrency]
related_skills: [forgekit-plan, forgekit-implement, forgekit-review]
---

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
