---
name: forgekit-tasks
version: 0.1.0
author: Forgekit
description: "When plan exists and you need a detailed actionable task list — break into 2-5 min tasks with exact file paths, code, and verification steps"
tags: [forgekit, planning, tasks, execution]
related_skills: [forgekit-plan, forgekit-spec, forgekit-implement, forgekit-tdd, forgekit-publish]
---

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
- **← Optional**: `/forgekit.spec` (acceptance criteria), `/forgekit.checklist` (validated requirements)
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
