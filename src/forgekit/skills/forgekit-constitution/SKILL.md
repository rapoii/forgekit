---
name: forgekit-constitution
version: 0.1.0
author: Forgekit
description: "When starting a new project — establish project principles, coding standards, and architectural guidelines"
tags: [forgekit, constitution, principles, standards, foundation]
related_skills: [forgekit-config, forgekit-specify, forgekit-brainstorm]
---

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
