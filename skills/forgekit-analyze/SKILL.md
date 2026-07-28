---
name: forgekit-analyze
version: 0.1.0
author: Forgekit
description: "When spec exists — cross-check consistency with constitution, find gaps, contradictions, and missing requirements"
tags: [forgekit, analyze, validation, consistency, quality-gates]
related_skills: [forgekit-specify, forgekit-constitution, forgekit-checklist, forgekit-plan]
---

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
