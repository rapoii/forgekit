# Forgekit Template: Constitution
# Used by /forgekit.constitution

# [PROJECT NAME] Constitution

> Governing principles for [PROJECT NAME]. All development should follow these guidelines.

## Code Quality
- Write clean, readable code
- DRY — Don't Repeat Yourself
- YAGNI — You Aren't Gonna Need It
- Meaningful names for variables, functions, and classes
- [Project-specific quality rule]

## Testing
- Test-driven development (TDD) when possible
- Write failing test first, then implement
- All tests must pass before marking a task complete
- [Project-specific testing rule]

## Architecture
- Keep it simple — prefer straightforward solutions
- Modular design — low coupling, high cohesion
- [Project-specific architecture rule]

## Git Workflow
- Descriptive commit messages: `type: description`
- Types: feat, fix, refactor, docs, chore, test
- One logical change per commit
- Branch naming: feature/*, fix/*, refactor/*

## Documentation
- README must be up-to-date
- API changes must be documented
- Complex logic needs inline comments

## Security
- Never commit secrets or API keys
- Validate all user input
- Use environment variables for configuration
- [Project-specific security rule]

## Review Standards
- [What reviewers should check]
- [Minimum approval requirements]


## Gates (Inspired by Spec Kit)

### Simplicity Gate (Article VII)
- Solution MUST use ≤ 3 distinct frameworks/libraries
- No "future-proofing" — build what's needed today
- No premature abstractions — duplicate code > wrong abstraction

### Anti-Abstraction Gate (Article VIII)
- Use framework features directly, don't wrap them
- Don't create helper utilities for one-time operations
- Custom code only when standard library doesn't exist
- Example: use `requests.get()` directly, don't wrap in a custom APIClient

### Test-First Gate (Article IX)
- Production code MUST have failing test first
- Test file created BEFORE source file
- All tests pass before claiming complete


### Complexity Tracking (Article X)

Track complexity decisions as they're made:
- New abstractions require justification
- Each new dependency gets a complexity score (1-5)
- Decisions over score 3 require explicit user approval
- Document all complexity decisions in constitution.md

Example format:
```markdown
| Decision | Score | Justification |
|---|---|---|
| Add PyYAML dependency | 2 | Replaces buggy hand-rolled parser |
| Custom workflow engine | 4 | Deferred to v0.3.0 — use external |
```
