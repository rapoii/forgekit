---
name: forgekit-review
version: 0.1.0
author: Forgekit
description: "When implementation is complete and you need a comprehensive review — check spec compliance AND code quality in two dimensions"
tags: [forgekit, review, quality, verification]
related_skills: [forgekit-implement, forgekit-specify, forgekit-constitution, forgekit-checklist, forgekit-receiving-review, forgekit-verify, forgekit-debug]
---

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
