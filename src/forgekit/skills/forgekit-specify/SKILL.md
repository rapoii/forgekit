---
name: forgekit-specify
version: 0.1.0
author: Forgekit
description: "When ready to define requirements — write structured specs with user stories, acceptance criteria, and non-functional requirements"
tags: [forgekit, spec, requirements, user-stories, acceptance-criteria]
related_skills: [forgekit-analyze, forgekit-plan, forgekit-brainstorm, forgekit-clarify, forgekit-constitution]
---

# forgekit-specify

Define WHAT to build — not HOW. Produces a structured specification with requirements, user stories, acceptance criteria, and non-functional requirements. This is the formalization phase where ideas become actionable specifications.

## When to Use

- User says "write a spec for X" or "specify X"
- After brainstorm + clarify, ready to formalize
- User has a clear idea and wants structured requirements
- Bootstrap skill routes here for clear ideas

**Do NOT use when:**
- No constitution exists → go to `/forgekit.constitution` first
- Idea is too vague → go to `/forgekit.brainstorm` first
- Significant ambiguities remain → go to `/forgekit.clarify` first

## Steps

### 1. Check Prerequisites

```bash
ls .forgekit/constitution.md 2>/dev/null
ls .forgekit/specs/*-brainstorm.md 2>/dev/null
ls .forgekit/specs/*-clarify.md 2>/dev/null
```

- Constitution MUST exist (warn if missing)
- Brainstorm/clarify notes are optional but helpful — read them if they exist

### 2. Gather Input Sources

Read in order:
1. `.forgekit/constitution.md` — for principles and constraints
2. `.forgekit/specs/{feature}-brainstorm.md` — for approach decisions
3. `.forgekit/specs/{feature}-clarify.md` — for resolved ambiguities
4. User's verbal description — for anything not yet captured

### 3. Write the Specification

Generate a structured spec. Ask clarifying questions as needed (one at a time), but aim to formalize efficiently.

```markdown
# Spec: [Feature Name]

> Version: 1.0
> Date: YYYY-MM-DD
> Status: draft | review | approved
> Author: [User] + Forgekit

## Overview

[2-3 sentence description of the feature and its purpose]

## Background

[Why this feature is needed. Reference brainstorm insights.]

## Requirements

### Functional Requirements

#### FR-1: [Requirement Name]
**Description:** [What the system must do]
**Priority:** Must Have | Should Have | Could Have | Won't Have
**Source:** [User story or business need]

#### FR-2: [Requirement Name]
...

### Non-Functional Requirements

#### NFR-1: Performance
[Response time, throughput, scale targets]

#### NFR-2: Security
[Auth, data protection, input validation]

#### NFR-3: Usability
[Accessibility, UX standards]

### User Stories

#### US-1: [Title]
**As a** [user type]
**I want to** [action]
**So that** [benefit]

**Acceptance Criteria:**
- [ ] [Testable criterion 1]
- [ ] [Testable criterion 2]
- [ ] [Testable criterion 3]

#### US-2: [Title]
...

### Data Model

[Key entities and relationships — what data is involved]

### API Contract

[Endpoints, request/response shapes — if applicable]

### Edge Cases

| Scenario | Expected Behavior |
|---|---|
| [Edge case 1] | [How system responds] |
| [Edge case 2] | [How system responds] |

### Out of Scope

[Explicitly list what this spec does NOT cover]

### Open Questions

[Remaining questions — ideally empty if clarify was thorough]

## Traceability

| Requirement | User Story | Acceptance Criteria |
|---|---|---|
| FR-1 | US-1 | AC-1, AC-2 |
| FR-2 | US-2 | AC-3 |
```

### 4. Review with User

Present the spec and ask for review:

> "Here's the spec for [feature]. Please review — especially the acceptance criteria. Any changes needed?"

### 5. Save Spec

Save to TWO locations:

1. **Active spec**: `.forgekit/spec.md` (the current working spec)
2. **History**: `.forgekit/specs/{feature}.md` (versioned copy)

### 6. Update Config

```yaml
active_spec: "{feature}"
phases:
  specify: true
```

### 7. Suggest Next Step

```
✅ Spec saved to .forgekit/spec.md and .forgekit/specs/{feature}.md

Next steps:
- /forgekit.analyze — validate spec against constitution and check for gaps
- /forgekit.plan — jump to technical architecture (if confident in the spec)
```

## Output

| File | Description |
|---|---|
| `.forgekit/spec.md` | Active specification (always the latest) |
| `.forgekit/specs/{feature}.md` | Versioned copy for history |
| `.forgekit/config.yaml` | Updated `active_spec` and phase |

## Connected Skills

- **`/forgekit.constitution`** — Prerequisite: spec must align with constitution
- **`/forgekit.brainstorm`** — Input: brainstorm notes inform the spec
- **`/forgekit.clarify`** — Input: clarification Q&A informs the spec
- **`/forgekit.analyze`** — Next step: validate spec consistency
- **`/forgekit.plan`** — Next step: create technical architecture
- **`/forgekit.config`** — Updates active_spec and phase tracking

## Examples

### Example 1: Spec from Brainstorm
```
User: "write a spec for the real-time notifications feature"
Agent: [reads brainstorm and clarify notes]
Agent: [drafts spec with FRs, user stories, acceptance criteria]
Agent: "Spec drafted with 5 functional requirements and 3 user stories. Please review."
User: "Add a requirement for notification preferences"
Agent: [adds FR-6: Notification Preferences]
Agent: "✅ Spec saved. Next: /forgekit.analyze to validate against your constitution."
```

### Example 2: Spec from Scratch
```
User: "spec: user authentication with OAuth2"
Agent: "I need a few details to write a complete spec."
Agent: "Which OAuth2 providers? Google, GitHub, both, or others?"
User: "Google and GitHub"
Agent: "Should users be able to link multiple providers to one account?"
User: "yes"
Agent: [writes spec]
```

## Pitfalls

- **Constitution is mandatory.** Never write a spec without checking the constitution. It defines the constraints.
- **Don't specify HOW.** Spec defines WHAT. Technical decisions (database choice, framework, architecture) belong in `/forgekit.plan`.
- **Acceptance criteria must be testable.** "System should be fast" → bad. "Response time < 200ms for 95th percentile" → good.
- **Active spec vs history.** Always save to both `.forgekit/spec.md` (active) and `.forgekit/specs/{feature}.md` (history). The active spec is what other skills read.
- **Out of scope is critical.** Explicitly listing what's NOT included prevents scope creep.
- **MoSCoW prioritization.** Use Must/Should/Could/Won't for requirement priorities.
