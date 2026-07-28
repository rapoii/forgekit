---
name: forgekit-brainstorm
version: 0.1.0
author: Forgekit
description: "When exploring ideas before specifying — generate approaches, trade-offs, and design options interactively"
tags: [forgekit, brainstorm, ideation, exploration, design]
related_skills: [forgekit-clarify, forgekit-specify, forgekit-constitution]
---

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
