---
name: forgekit-checklist
version: 0.1.0
author: Forgekit
description: "When spec exists and you need to validate requirements completeness — generate a quality checklist from the spec"
tags: [forgekit, planning, quality, checklist, requirements]
related_skills: [forgekit-spec, forgekit-analyze, forgekit-plan, forgekit-tasks]
---

# Forgekit Checklist

Generate a quality checklist FROM the spec — like "unit tests for English." This validates that your requirements are complete, consistent, and testable before you write a single line of code.

## When to Use

- After `/forgekit.spec` has been written and you want to validate it
- Before planning implementation (catch gaps early, fix cheap)
- When a stakeholder asks "is the spec complete?"
- After `/forgekit.analyze` has surfaced questions that need answers

## Steps

1. **Load the spec** from `.forgekit/spec.md`. If it doesn't exist, stop — run `/forgekit.spec` first.

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

- **← Prerequisite**: `/forgekit.spec` (need a spec to validate)
- **← Optional**: `/forgekit.analyze` (analysis questions inform checklist)
- **→ Next**: `/forgekit.plan` (once checklist is green or blockers resolved)
- **→ Parallel**: `/forgekit.spec` for reworking sections with failures

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
       Run /forgekit.spec to address blockers, then /forgekit.plan to proceed.
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
