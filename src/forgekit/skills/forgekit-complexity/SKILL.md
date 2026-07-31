---
name: forgekit-complexity
version: 0.1.0
author: Forgekit
description: "Track and manage complexity decisions — new abstractions, dependencies, frameworks"
tags: [forgekit, complexity, yagni, simplicity, tracking]
related_skills: [forgekit-constitution, forgekit-brainstorm, forgekit-specify]
---

# forgekit-complexity

Track complexity decisions throughout the project lifecycle. Prevents premature abstraction and keeps the codebase lean.

## When to Use

- Adding a new dependency or framework
- Creating a new abstraction layer
- Making architectural decisions with complexity implications
- Reviewing whether existing complexity is justified
- Before merge — check if complexity grew unexpectedly

## Steps

### 1. Score the Decision

Rate each complexity addition on a 1-5 scale:

| Score | Meaning | Action |
|---|---|---|
| 1 | Trivial (config, utility) | Proceed freely |
| 2 | Minor (single library) | Proceed, document |
| 3 | Moderate (new pattern) | Document + consider alternatives |
| 4 | Significant (new subsystem) | Require user approval |
| 5 | Major (architectural change) | Require explicit justification + user approval |

### 2. Document in Constitution

Add to constitution.md complexity table:

```markdown
| Decision | Score | Justification | Status |
|---|---|---|---|
| Add PyYAML | 2 | Replaces buggy hand-rolled parser | Approved |
| Custom workflow engine | 4 | Deferred — use external | Deferred |
```

### 3. Review Periodically

Every 10 tasks or at the end of a feature:
- Are all abstractions still justified?
- Can any be simplified or removed?
- Have any score-4+ decisions become unnecessary?

## Output

| Artifact | Description |
|---|---|
| Complexity table in constitution.md | Running log of all complexity decisions |
| Simplification proposals | If over-complexity detected |

## Pitfalls

- **Don't add complexity "for the future."** YAGNI — build what's needed today.
- **Don't forget to track.** Untracked complexity grows silently.
- **Don't confuse score 2 with score 4.** A single library ≠ a new subsystem.
- **Don't skip periodic reviews.** Complexity compounds; review regularly.
- **Don't remove complexity without user consent.** Some complexity is justified; check before removing.

## Connected Skills

- **`/forgekit.constitution`** — Complexity table lives in constitution
- **`/forgekit.brainstorm`** — Design decisions with complexity trade-offs
- **`/forgekit.specify`** — Requirements may introduce complexity
- **`/forgekit.review`** — Review includes complexity audit
