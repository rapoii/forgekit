---
name: forgekit-planning
version: 0.1.0
author: Forgekit
description: "Macro-skill for forgekit-planning phase. Combines: constitution, brainstorm, clarify, specify, plan"
tags: [forgekit, planning]
---

# Forgekit Planning

This is a consolidated macro-skill for Forgekit to optimize context length.
It contains the instructions for multiple related phases. Read the specific section for your current phase.

## FORGEKIT-CONSTITUTION
# forgekit-constitution

Create or update the project constitution — the foundational document that defines HOW the project should be built. All subsequent Forgekit phases reference the constitution.

## When to Use

- New project setup (after `/forgekit.config init`)
- User says "set up project standards" or "define project rules"
- User wants to establish coding conventions
- User asks to create `.hermes.md` or `AGENTS.md` (redirect here first)
- Constitution doesn't exist but other Forgekit skills need it

## Steps

### 1. Check Prerequisites

```bash
ls .forgekit/config.yaml 2>/dev/null
```

If config doesn't exist → suggest `/forgekit.config init` first.

### 2. Gather Principles (Interactive, One Question at a Time)

Ask about each area ONE question at a time. Wait for the user's answer before asking the next.

**Area 1: Code Quality**
> "What are your code quality standards? For example:
> - Type safety (strict TypeScript, Python type hints, etc.)
> - Linting rules (ESLint strict, ruff, etc.)
> - Code review requirements
> - Naming conventions"

**Area 2: Testing**
> "What's your testing strategy?
> - TDD (tests first)?
> - Unit test coverage targets?
> - Integration/E2E testing?
> - Test framework preference?"

**Area 3: Architecture**
> "Any architectural preferences?
> - Patterns (Clean Architecture, MVC, hexagonal, etc.)
> - Module organization
> - Dependency injection style
> - Error handling approach"

**Area 4: Git Workflow**
> "How do you handle version control?
> - Branch strategy (trunk-based, gitflow, etc.)
> - Commit message format (conventional commits, etc.)
> - PR/merge requirements
> - Protected branches?"

**Area 5: Security**
> "Security considerations?
> - Secret management
> - Input validation
> - Authentication/authorization patterns
> - Dependency auditing?"

**Area 6: Documentation**
> "Documentation standards?
> - README requirements
> - API documentation (OpenAPI, etc.)
> - Inline comment style
> - Changelog format?"

**Area 7: AI Agent Conventions**
> "How should AI agents work on this project?
> - Always run tests before committing?
> - Require spec before coding?
> - Review checklist?
> - Branch naming for AI work?"

### 3. Generate Constitution

Compile answers into `.forgekit/constitution.md`:

```markdown
# [Project Name] Constitution

> Created: YYYY-MM-DD
> Last updated: YYYY-MM-DD

## Code Quality
[User's answers about type safety, linting, naming]

## Testing Strategy
[User's answers about TDD, coverage, frameworks]

## Architecture
[User's answers about patterns, organization, DI]

## Git Workflow
[User's answers about branches, commits, PRs]

## Security
[User's answers about secrets, validation, auth]

## Documentation
[User's answers about README, API docs, comments]

## AI Agent Conventions
[User's answers about agent behavior, test requirements]

## Non-Negotiables
[Extracted hard rules — things that MUST always be followed]
```

### 4. Update Config

Mark constitution phase as complete:

```yaml
phases:
  constitution: true
```

### 5. Generate Agent Configs

Ask: "Should I generate agent-specific config files (.hermes.md, AGENTS.md) from this constitution?"

If yes → delegate to `/forgekit.config agents`

### 6. Suggest Next Step

```
✅ Constitution created at .forgekit/constitution.md

This constitution will guide all future decisions. Every spec, plan, and implementation
will reference these principles.

Next: /forgekit.brainstorm to explore your first feature idea,
or /forgekit.specify if you already know what to build.
```

### 🛡️ Constitution Tracker Requirement
When generating this document, you MUST append a `## Constitution Compliance Notes` section at the very bottom.
In this section, briefly explain how your output aligns with the project's constitution (or note any deviations).
This ensures the constitution remains an active guardrail throughout development.

## Output

| File | Description |
|---|---|
| `.forgekit/constitution.md` | Project principles and guidelines |
| `.forgekit/config.yaml` | Updated with `phases.constitution: true` |
| `.hermes.md` | (optional) Hermes Agent config |
| `AGENTS.md` | (optional) Claude Code config |
| `CLAUDE.md` | (optional) Claude-specific config |

## Connected Skills

- **`/forgekit.config`** — Must run first to initialize; constitution updates config
- **`/forgekit.specify`** — Specs must align with constitution principles
- **`/forgekit.analyze`** — Checks spec-constitution consistency
- **`/forgekit.brainstorm`** — Next step after constitution
- **`/forgekit.plan`** — Architecture must respect constitution

## Examples

### Example 1: Fresh Project
```
User: "set up constitution for my new API project"
Agent: "Let's establish your project's principles. I'll ask one area at a time."
Agent: "First — code quality. What are your standards for type safety, linting, and naming?"
User: "strict TypeScript, ESLint strict, camelCase for variables, PascalCase for components"
Agent: "Got it. Next — testing. What's your testing strategy?"
...
Agent: [generates .forgekit/constitution.md]
Agent: "✅ Constitution saved. Want me to generate agent configs from this?"
```

### Example 2: Updating Existing Constitution
```
User: "update constitution — add a rule that all PRs need two approvals"
Agent: [reads .forgekit/constitution.md]
Agent: [patches the Git Workflow section]
Agent: "✅ Updated: PRs now require two approvals."
```

## Pitfalls

- **One question at a time.** This is critical. Don't dump all 7 areas at once — it overwhelms the user and produces shallow answers.
- **Don't be too prescriptive.** Offer examples as suggestions, not requirements. The user's project is unique.
- **Constitution is living.** It can be updated anytime. Don't treat it as immutable.
- **Non-negotiables matter.** Extract the hard rules from the user's answers. These become the guardrails that `/forgekit.analyze` checks against.
- **Agent configs are derived.** They should always reflect the constitution, not diverge from it.

## FORGEKIT-BRAINSTORM
# forgekit-brainstorm

Explore and expand ideas BEFORE committing to a specification. Generate multiple approaches, evaluate trade-offs, and help the user make informed decisions. This is the creative, divergent thinking phase.

## When to Use

- User has a vague idea and wants to explore options
- User says "brainstorm X" or "explore approaches for X"
- New feature needs design exploration before specifying
- User is unsure about technical approach
- Bootstrap skill routes here for vague ideas

**Do NOT use when:**
- User has a clear, well-defined requirement → go to `/forgekit.specify`
- User needs to clarify ambiguities in existing brainstorm → go to `/forgekit.clarify`
- No constitution exists → go to `/forgekit.constitution` first

## Steps

### 1. Check Prerequisites

```bash
ls .forgekit/constitution.md 2>/dev/null
```

If no constitution → warn and suggest `/forgekit.constitution` first. Proceed anyway if user insists.

### 2. Understand the Idea

Ask ONE question to understand the core idea:

> "Tell me about what you want to build. What problem does it solve?"

### 3. Explore Interactively (One Question at a Time)

Based on the user's description, ask targeted questions ONE AT A TIME to expand the idea:

**Expand the problem space:**
- "Who are the users? What's their workflow?"
- "What existing solutions have you seen? What do you like/dislike about them?"
- "What's the simplest version that would be useful?"

**Explore constraints:**
- "Any performance requirements? (latency, throughput, scale)"
- "Budget or timeline constraints?"
- "Must integrate with existing systems?"

**Probe for depth:**
- "What happens when [edge case]?"
- "How should it handle [failure scenario]?"
- "What would make this a 'nice to have' vs a 'must have'?"

### 4. Generate Approaches

After gathering enough context (typically 3-5 questions), present **2-4 distinct approaches**:

```markdown
## Approach A: [Name]
**Description:** [One-paragraph description]
**Pros:**
- [Pro 1]
- [Pro 2]
**Cons:**
- [Con 1]
- [Con 2]
**Effort:** [Low/Medium/High]
**Best for:** [When this approach shines]

## Approach B: [Name]
...

## Approach C: [Name]
...
```

### 5. Discuss Trade-offs

After presenting approaches, facilitate a discussion:

> "Which approach resonates with you? Or do you want to combine elements from multiple approaches?"

Help the user weigh trade-offs. Don't push a specific choice — facilitate.

### 6. Save Brainstorm Notes

Save the brainstorm session to `.forgekit/specs/{feature}-brainstorm.md`:

```markdown
# Brainstorm: [Feature Name]

> Date: YYYY-MM-DD
> Status: [explored | decided | needs-clarification]

## Problem Statement
[What we're solving]

## Key Insights
[Important discoveries during brainstorm]

## Approaches Considered

### Approach A: [Name]
[Description, pros, cons, effort]

### Approach B: [Name]
[Description, pros, cons, effort]

## Decision
[Which approach was chosen, or "pending"]

## Open Questions
[Questions that need answers before specifying]

## Next Steps
- [ ] Clarify: [specific question]
- [ ] Specify: Ready to move to /forgekit.specify
```

### 7. Suggest Next Step

```
✅ Brainstorm saved to .forgekit/specs/{feature}-brainstorm.md

Next steps:
- /forgekit.clarify — if there are open questions to resolve
- /forgekit.specify — if you're ready to formalize the requirements
```

### 🛡️ Constitution Tracker Requirement
When generating this document, you MUST append a `## Constitution Compliance Notes` section at the very bottom.
In this section, briefly explain how your output aligns with the project's constitution (or note any deviations).
This ensures the constitution remains an active guardrail throughout development.

## Output

| File | Description |
|---|---|
| `.forgekit/specs/{feature}-brainstorm.md` | Brainstorm notes with approaches and trade-offs |

## Connected Skills

- **`/forgekit.constitution`** — Prerequisite: constitution should exist to guide decisions
- **`/forgekit.clarify`** — Next step if brainstorm has open questions
- **`/forgekit.specify`** — Next step when ready to formalize
- **`/forgekit.bootstrap`** — Routes here for vague ideas
- **`/forgekit.config`** — Updates phase tracking

## Examples

### Example 1: New Feature Brainstorm
```
User: "brainstorm adding real-time notifications to my app"
Agent: "Tell me about the notification needs. What events should trigger notifications?"
User: "When someone assigns you a task or comments on your task"
Agent: "Good. What channels — in-app only, or also email/push?"
User: "In-app for now, maybe email later"
Agent: "Got it. Here are 3 approaches..."
[presents approaches with trade-offs]
```

### Example 2: Architecture Brainstorm
```
User: "mau bikin sistem recommendation, tapi bingung mau pakai approach apa"
Agent: "Let's explore this. What kind of recommendations — products, content, users?"
User: "Product recommendations for e-commerce"
Agent: "What data do you have? User behavior, product metadata, purchase history?"
...
```

## Pitfalls

- **One question at a time.** Never dump multiple questions. This is the most important rule.
- **Don't jump to solutions.** Brainstorming is about exploration, not implementation.
- **Don't bias toward your preferred approach.** Present trade-offs honestly.
- **Save everything.** Even rejected approaches — they might be useful later.
- **Feature slug naming.** Use kebab-case for feature names in file paths (e.g., `real-time-notifications-brainstorm.md`).
- **Brainstorm ≠ Spec.** Don't let brainstorming turn into specification. If the user starts writing acceptance criteria, suggest moving to `/forgekit.specify`.

## FORGEKIT-CLARIFY
# forgekit-clarify

Identify and resolve underspecified areas in brainstorm notes, rough specs, or feature ideas. Systematically finds gaps and asks targeted questions to fill them. This is the convergent thinking phase — narrowing from exploration to precision.

## When to Use

- After brainstorming, before specifying (brainstorm has open questions)
- User says "clarify this" or "I have questions about X"
- Existing spec has gaps or contradictions
- User's description is too vague to specify
- Bootstrap skill routes here for partially-defined ideas

**Do NOT use when:**
- No brainstorm or rough idea exists → go to `/forgekit.brainstorm` first
- Idea is already clear → go directly to `/forgekit.specify`
- Questions are about spec-constitution alignment → go to `/forgekit.analyze`

## Steps

### 1. Check Prerequisites

Look for existing brainstorm notes or rough spec:

```bash
ls .forgekit/specs/*-brainstorm.md 2>/dev/null
ls .forgekit/spec.md 2>/dev/null
```

If neither exists, ask: "Do you have a rough idea or brainstorm notes? Or should we start from scratch with `/forgekit.brainstorm`?"

### 2. Identify Underspecified Areas

Read the brainstorm notes or spec and categorize gaps:

| Gap Type | Description | Priority |
|---|---|---|
| **Functional** | Missing user stories, undefined behaviors | High |
| **Edge cases** | Error handling, boundary conditions | High |
| **Non-functional** | Performance, scale, security requirements | Medium |
| **Data** | Data models, relationships, validation rules | Medium |
| **Integration** | External services, APIs, auth flows | Medium |
| **UX** | User interactions, flows, feedback | Low-Medium |
| **Technical** | Infrastructure, deployment, monitoring | Low |

### 3. Ask Questions (One at a Time)

Prioritize HIGH gaps first. Ask ONE question at a time:

> "I noticed [gap description]. [Targeted question]?"

**Question format:**
- Be specific, not open-ended
- Offer options when possible
- Reference the constitution when relevant

**Good:**
> "Your brainstorm mentions 'user authentication' but doesn't specify the method. Should we use:
> a) JWT tokens (stateless, good for APIs)
> b) Session cookies (traditional, simpler)
> c) OAuth2 with existing providers (Google, GitHub)"

**Bad:**
> "How should authentication work?" (too open-ended)

### 4. Track Q&A

Maintain a running Q&A document during the session:

```markdown
## Q1: [Question]
**Answer:** [User's answer]
**Impact:** [What this clarifies / what changes]

## Q2: [Question]
**Answer:** [User's answer]
**Impact:** [What this clarifies / what changes]
```

### 5. Generate Clarification Document

Save to `.forgekit/specs/{feature}-clarify.md`:

```markdown
# Clarification: [Feature Name]

> Date: YYYY-MM-DD
> Source: [brainstorm | rough-spec | user-input]
> Status: [in-progress | complete]

## Original Gaps Identified
1. [Gap 1 — type: functional, priority: high]
2. [Gap 2 — type: edge-case, priority: high]
3. [Gap 3 — type: non-functional, priority: medium]

## Clarifications

### Q1: [Question]
**Answer:** [User's answer]
**Impact:** [What changes in the spec]

### Q2: [Question]
**Answer:** [User's answer]
**Impact:** [What changes in the spec]

## Resolved
- [x] [Gap 1 — resolved with answer to Q1]
- [x] [Gap 2 — resolved with answer to Q2]

## Remaining Gaps
- [ ] [Gap that still needs answers]

## Recommendation
[Ready to specify / needs more clarification]
```

### 6. Suggest Next Step

```
✅ Clarification complete for [feature]

Resolved [N] gaps. [M] minor questions remain but shouldn't block specification.

Next: /forgekit.specify to formalize the requirements
```

If major gaps remain:
```
⚠️ [N] high-priority gaps remain. Let's resolve these before specifying.
```

### 🛡️ Constitution Tracker Requirement
When generating this document, you MUST append a `## Constitution Compliance Notes` section at the very bottom.
In this section, briefly explain how your output aligns with the project's constitution (or note any deviations).
This ensures the constitution remains an active guardrail throughout development.

## Output

| File | Description |
|---|---|
| `.forgekit/specs/{feature}-clarify.md` | Q&A document with resolved gaps |

## Connected Skills

- **`/forgekit.brainstorm`** — Input: brainstorm notes feed into clarification
- **`/forgekit.specify`** — Output: clarified requirements feed into specification
- **`/forgekit.analyze`** — Later: checks if spec has remaining ambiguities
- **`/forgekit.constitution`** — Reference: constitution principles guide clarification priorities
- **`/forgekit.config`** — Updates phase tracking

## Examples

### Example 1: Clarifying a Brainstorm
```
User: "clarify the real-time notifications brainstorm"
Agent: [reads .forgekit/specs/real-time-notifications-brainstorm.md]
Agent: "I found 3 gaps in the brainstorm. Let's resolve them."
Agent: "Gap 1 (high priority): The brainstorm mentions 'WebSocket or SSE' but doesn't decide.
        Your app uses Next.js — WebSocket needs a separate server, SSE works with API routes.
        Which do you prefer?"
User: "SSE for simplicity"
Agent: "Got it. Gap 2: What should happen when a user is offline?"
...
```

### Example 2: Clarifying a Vague Request
```
User: "mau bikin admin panel"
Agent: "The admin panel idea needs clarification. Let me ask a few questions."
Agent: "First — what can admins manage? Users only, or also content and settings?"
User: "Users and content"
Agent: "Second — is this a separate app or part of the existing Next.js app?"
...
```

## Pitfalls

- **One question at a time.** Critical. Don't overwhelm.
- **Prioritize ruthlessly.** Don't ask about button colors when the data model is undefined.
- **Don't answer your own questions.** Present options, but let the user decide.
- **Track impact.** Each answer should note what it resolves — this builds confidence.
- **Don't create a spec here.** Clarification is about Q&A, not formalization. Save that for `/forgekit.specify`.
- **Feature slug consistency.** Use the same slug as the brainstorm file (e.g., if brainstorm is `real-time-notifications-brainstorm.md`, clarification is `real-time-notifications-clarify.md`).

## FORGEKIT-SPECIFY
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

### 🛡️ Constitution Tracker Requirement
When generating this document, you MUST append a `## Constitution Compliance Notes` section at the very bottom.
In this section, briefly explain how your output aligns with the project's constitution (or note any deviations).
This ensures the constitution remains an active guardrail throughout development.

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


## Auto Branch Creation

When specs are generated in a git repo, create a semantic branch:

```bash
# Auto-generate branch name from feature description
branch_name="001-$(echo "$FEATURE_NAME" | tr '[:upper:]' '[:lower:]' | tr ' ' '-')"
git checkout -b "$branch_name"
```

Rules:
- Feature numbering: `001`, `002`, `003` (auto-incrementing)
- Name from spec description (kebab-case)
- Auto-checkout new branch
- Save spec at `specs/<branch>/spec.md`

## FORGEKIT-PLAN
# Forgekit Plan

Create a technical implementation plan from the spec. Architecture decisions, tech stack choices, file structure, and bite-sized tasks (2–5 min each) with a TDD-first approach.

## When to Use

- After `/forgekit.specify` and `/forgekit.analyze` are complete
- When you're ready to transition from "what to build" to "how to build"
- Before dispatching implementation work to subagents
- After `/forgekit.checklist` passes (or blockers are resolved)

## Steps

1. **Load inputs:**
   - `.forgekit/spec.md` — the requirements
   - `.forgekit/analysis.md` — questions answered, trade-offs decided
   - `.forgekit/constitution.md` — project principles and constraints
   - `.forgekit/checklist.md` — if it exists, verify no blockers remain
   - If any critical file is missing, stop and run the prerequisite skill first.

2. **Make architecture decisions.** For each major component:
   - Choose tech stack (language, framework, libraries) with rationale
   - Define module boundaries and data flow
   - Pick patterns (MVC, event-driven, etc.) and justify
   - Document decisions in a `## Architecture` section

3. **Design file structure.** Create the project layout:
   ```
   project-root/
   ├── src/
   │   ├── module-a/
   │   └── module-b/
   ├── tests/
   │   ├── module-a/
   │   └── module-b/
   ├── .forgekit/
   └── ...
   ```
   Each file should have a single clear responsibility.

4. **Define the task sequence.** Break implementation into bite-sized tasks:
   - Each task: **2–5 minutes** of focused work
   - Each task: **one file or one concern** — not a kitchen sink
   - Each task: **verifiable** — you can confirm it's done
   - Order by dependency (foundations first, then layers on top)

5. **Apply TDD ordering.** For each task, specify:
   - 🔴 Write failing test first (what test, what file)
   - 🟢 Implement minimal code to pass
   - 🔵 Refactor if needed
   - ✅ Commit

6. **Identify risks and mitigations:**
   - Unknowns that could block progress
   - Third-party dependencies with version/availability risk
   - Performance-sensitive areas needing benchmarks

7. **Save** the plan to `.forgekit/plan.md`.

8. **Report** task count, estimated duration, and risk areas to the user.

## Output

`.forgekit/plan.md` containing:
- Architecture decisions with rationale
- File structure
- Ordered task list with TDD notes per task
- Risk register
- Estimated total effort

## Connected Skills

- **← Prerequisite**: `/forgekit.specify` (requirements), `/forgekit.analyze` (decisions)
- **← Optional**: `/forgekit.checklist` (validate spec completeness)
- **→ Next**: `/forgekit.tasks` (detailed task breakdown) or `/forgekit.tdd` (start TDD cycle)
- **→ Parallel**: `/forgekit.constitution` to validate against principles

## Examples

### Creating a plan for a CLI tool
```
User: /forgekit.plan
Agent: Loading spec, analysis, and constitution...

       Architecture Decision: CLI Tool
       ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
       Language: Python 3.11+
       CLI framework: Click
       Testing: pytest + pytest-cli
       Structure: src-layout with click groups

       Task Breakdown (14 tasks, ~45 min total):
       1. 🔴 Project scaffold + pyproject.toml (2 min)
       2. 🔴 CLI entry point with --help (3 min)
       3. 🔴 Config loader: test missing file → implement (3 min)
       4. 🔴 Config loader: test valid YAML → implement (3 min)
       ...

       Risks: None identified.
       Saved to .forgekit/plan.md
       Next: /forgekit.tasks for detailed task specs, or /forgekit.implement to start.
```

## Pitfalls

- **Tasks too large.** If a "task" takes more than 5 minutes, split it. Large tasks defeat the purpose of incremental progress.
- **Skipping TDD ordering.** Even if you don't write tests first, document what the test should be. Future subagents need this context.
- **Architecture without rationale.** Every decision needs a "why" — otherwise reviewers can't evaluate it.
- **Forgetting non-functional requirements.** Performance, security, and accessibility from the spec must appear as tasks.

