# Forgekit Template: Implementation Plan
# Used by /forgekit.plan

# [Feature Name] Implementation Plan

> **For agents:** Use `/forgekit.implement` with subagent-driven development to execute this plan.

**Goal:** [One sentence]

**Architecture:** [2-3 sentences about approach]

**Tech Stack:** [Key technologies/libraries]

---

## Task 1: [Descriptive Name]

**Objective:** What this task accomplishes (one sentence)

**Files:**
- Create: `exact/path/to/new_file.py`
- Modify: `exact/path/to/existing.py:45-67`
- Test: `tests/path/to/test_file.py`

**Step 1: Write failing test**
```python
def test_specific_behavior():
    result = function(input)
    assert result == expected
```

**Step 2: Run test to verify failure**
```
pytest tests/path/test.py::test_specific_behavior -v
```
Expected: FAIL — "function not defined"

**Step 3: Write minimal implementation**
```python
def function(input):
    return expected
```

**Step 4: Run test to verify pass**
```
pytest tests/path/test.py::test_specific_behavior -v
```
Expected: PASS

**Step 5: Commit**
```
git add tests/path/test.py src/path/file.py
git commit -m "feat: add specific feature"
```

---

## Task 2: [Next Task]

[Same structure as above]

---

## Verification Checklist
- [ ] All tests pass
- [ ] No linting errors
- [ ] Documentation updated
- [ ] Constitution principles followed
- [ ] Spec acceptance criteria met
