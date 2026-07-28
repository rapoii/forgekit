---
name: forgekit-bootstrap
version: 0.1.0
author: Forgekit
description: "When user says 'I want to build X' or 'mau bikin X' — guide them through the right Forgekit starting point"
tags: [forgekit, entry-point, onboarding, meta]
related_skills: [forgekit-config, forgekit-constitution, forgekit-brainstorm, forgekit-clarify, forgekit-specify, forgekit-analyze]
---

# forgekit-bootstrap

The universal entry point for Forgekit. Auto-triggers when a user expresses intent to build something, guiding them through the optimal starting workflow.

## When to Use

Trigger when the user says ANY of these (or similar):
- "I want to build X"
- "I want to create X"
- "mau bikin X" / "mau buat X"
- "bikin website", "bikin app", "bikin bot", "bikin tool"
- "let's start a new project"
- "help me build X"
- "new feature: X"
- "I need a X"
- Any expression of intent to create/build/design something

Also trigger when:
- User types `/forgekit` or `/forgekit.start` or `forgekit start`
- User asks "where do I start?"
- User is confused about which Forgekit command to use

## Steps

### 1. Detect Project State

Check if `.forgekit/` exists in the current working directory:

```bash
ls -la .forgekit/ 2>/dev/null
```

**If `.forgekit/` does NOT exist:**
- This is a NEW project. Suggest running `/forgekit.config` first to initialize.
- Ask: "Should I set up a Forgekit project here? I'll create `.forgekit/` with a basic config."
- If yes → run `/forgekit.config` with `init` action
- If user wants to skip → proceed to step 2

**If `.forgekit/` exists:**
- Read `.forgekit/config.yaml` to understand current state
- Check what phases are already completed
- Proceed to step 2

### 2. Understand What the User Wants

Ask ONE focused question to understand their goal:

> "What are you trying to build? Give me a rough description — we'll refine it together."

Based on the answer, categorize:

| User's State | Recommended Path |
|---|---|
| Vague idea, needs exploration | → `/forgekit.brainstorm` |
| Rough idea, needs clarity | → `/forgekit.clarify` |
| Clear idea, needs specification | → `/forgekit.specify` |
| Has a spec, needs validation | → `/forgekit.analyze` |
| Has analysis, needs architecture | → `/forgekit.plan` |
| Existing project, new feature | → `/forgekit.brainstorm` then `/forgekit.specify` |
| Just wants to code | → Check if spec exists, then `/forgekit.plan` or `/forgekit.tasks` |

### 3. Recommend and Route

Present the recommended path with a brief explanation:

```
Based on where you are, I recommend starting with /forgekit.brainstorm.

This will help us explore approaches and trade-offs before committing to a design.

Ready to begin? (or tell me if you'd prefer a different starting point)
```

### 4. Hand Off to the Recommended Skill

Once confirmed, load and execute the recommended skill. Pass along any context gathered during bootstrap.

## Output

No files created at this stage — this is a routing skill. The output is a recommendation and handoff to the appropriate Forgekit skill.

## Connected Skills

This is the **meta entry point** that connects to ALL other Forgekit skills:

| Skill | When to Route There |
|---|---|
| `/forgekit.config` | New project setup, config changes |
| `/forgekit.constitution` | No constitution exists yet |
| `/forgekit.brainstorm` | Vague idea, need to explore |
| `/forgekit.clarify` | Have ideas but gaps remain |
| `/forgekit.specify` | Ready to define requirements |
| `/forgekit.analyze` | Spec exists, need consistency check |
| `/forgekit.plan` | Spec validated, need architecture |
| `/forgekit.checklist` | Plan exists, need quality gates |
| `/forgekit.tasks` | Plan exists, need task breakdown |
| `/forgekit.tdd` | Tasks exist, ready to code with tests |
| `/forgekit.implement` | Tasks + tests ready, execute |
| `/forgekit.review` | Code exists, need spec compliance check |
| `/forgekit.debug` | Something is broken |
| `/forgekit.verify` | Near completion, final validation |
| `/forgekit.converge` | Check spec vs implementation alignment |
| `/forgekit.finish` | Ready for git cleanup |
| `/forgekit.publish` | Ready to ship |

## Examples

### Example 1: Brand New Project
```
User: "I want to build a task management CLI app"
Agent: [checks .forgekit/ — not found]
Agent: "I'll set up Forgekit for this project. Should I create .forgekit/ in the current directory?"
User: "yes"
Agent: [runs /forgekit.config init]
Agent: "Now let's establish your project's constitution — the principles that guide all decisions."
[proceeds to /forgekit.constitution]
```

### Example 2: Existing Project, New Feature
```
User: "mau bikin fitur export ke PDF"
Agent: [checks .forgekit/ — exists, constitution exists, no active spec]
Agent: "Let's brainstorm the PDF export feature first — there are several approaches with different trade-offs."
[proceeds to /forgekit.brainstorm]
```

### Example 3: User Knows What They Want
```
User: "I want to add OAuth2 login to my API"
Agent: [checks .forgekit/ — exists, constitution exists]
Agent: "Sounds clear enough. Let's write a spec for the OAuth2 login feature."
[proceeds to /forgekit.specify]
```

## Pitfalls

- **Don't skip the constitution.** If no constitution exists, always recommend `/forgekit.constitution` first. The constitution is the foundation that all other phases build on.
- **Don't assume the user's starting point.** Always ask or detect. A developer who says "I want to build X" might already have a spec somewhere.
- **One question at a time.** Don't overwhelm with multiple questions. Forgekit is designed for conversational flow.
- **Respect the user's choice.** If they want to skip brainstorm and go straight to specifying, let them. Forgekit recommends but doesn't enforce.
