---
name: forgekit-clarify
version: 0.1.0
author: Forgekit
description: "When brainstorm or spec has gaps — ask targeted questions to resolve ambiguities before specifying"
tags: [forgekit, clarify, questions, ambiguity, refinement]
related_skills: [forgekit-brainstorm, forgekit-specify, forgekit-analyze]
---

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
