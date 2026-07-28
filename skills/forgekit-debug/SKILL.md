---
name: forgekit-debug
version: 0.1.0
author: Forgekit
description: "When something is broken or behaving unexpectedly — systematic 4-phase debugging workflow: understand → reproduce → diagnose → fix"
tags: [forgekit, debugging, root-cause, troubleshooting]
related_skills: [forgekit-implement, forgekit-verify, forgekit-review]
---

# Forgekit Debug

Systematic debugging workflow adapted from Superpowers. Enforces root-cause analysis before fixing so you don't apply band-aids that create new bugs.

## When to Use

- A test fails and the reason isn't obvious
- Runtime behavior doesn't match spec expectations
- An error or exception appears during development or verification
- Performance degrades unexpectedly
- You're tempted to "just try something" — stop and run this instead

## Steps

### Phase 1: Understand

1. **Read the error message carefully.** Copy the full traceback or error output. Don't skim.
2. **Identify what changed.** Run `git diff` or `git log --oneline -5` to see recent work.
3. **Read the relevant spec.** Load the feature spec from `.forgekit/specs/<feature>/spec.md` (if it exists) to understand intended behavior.
4. **Read the relevant code.** Locate the file(s) involved in the error. Read the full function/module, not just the failing line.
5. **Formulate a hypothesis.** Write down what you think is wrong and why. Be specific — "the parser fails on nested arrays because the recursion doesn't check for empty elements" is good; "something's wrong with the parser" is not.

### Phase 2: Reproduce

1. **Create a minimal reproduction.** Strip away everything unrelated. The smallest possible code that triggers the bug.
2. **Confirm the bug reproduces consistently.** Run the reproduction 2-3 times. If it's intermittent, note the conditions.
3. **Confirm the bug is in scope.** Check: is this a pre-existing issue or something your current work introduced? Use `git stash` to test on a clean state if needed.
4. **Document the reproduction steps** in your notes or as a failing test.

### Phase 3: Diagnose

1. **Isolate the root cause.** Use one or more of these techniques:
   - **Binary search:** comment out half the code, see if bug persists, narrow down.
   - **Print/log tracing:** add strategic logging to trace data flow.
   - **Rubber duck:** explain the code line by line (works even in your head).
   - **Compare working vs broken:** diff two versions — one that works, one that doesn't.
2. **Verify your hypothesis.** The root cause should explain ALL observed symptoms, not just one.
3. **Check for related issues.** If the root cause is a pattern (e.g., missing null checks), search the codebase for the same pattern elsewhere.

### Phase 4: Fix

1. **Write a test that fails** because of the bug (if one doesn't already exist).
2. **Make the minimal fix.** Change only what's necessary. Resist the urge to refactor while fixing.
3. **Run the test — confirm it passes.**
4. **Run the full test suite** — confirm no regressions.
5. **Clean up** any debug logging or temporary code you added during diagnosis.

## Output

- Root cause documented (what, where, why)
- Fix applied with a test that prevents regression
- No new failures in the test suite
- If the bug revealed a gap in the spec, note it for `/forgekit.converge`

## Connected Skills

- **Before:** `/forgekit.implement` — bug may have surfaced during implementation
- **After:** `/forgekit.verify` — run full verification after the fix
- **After:** `/forgekit.review` — have the fix reviewed if it was non-trivial
- **Related:** `/forgekit.converge` — if the bug reveals missing spec coverage

## Pitfalls

- **Don't skip Phase 1.** Jumping to "fixing" without understanding is how you introduce new bugs.
- **Don't fix symptoms.** If you're adding a null check somewhere, ask WHY it's null.
- **Don't refactor during a bug fix.** Separate concerns — fix first, refactor later.
- **Don't ignore intermittent bugs.** They're usually race conditions or order-dependent state. Document the conditions.
- **One fix at a time.** If you find multiple bugs, fix and verify each separately.

## Example

```
# Bug: API returns 500 on empty request body

## Phase 1: Understand
- Error: TypeError: Cannot read property 'name' of undefined
- Location: src/handlers/users.js:42
- Spec says: "API should return 400 for invalid input"
- Hypothesis: Request body parsing doesn't handle empty bodies, passes undefined to handler

## Phase 2: Reproduce
- curl -X POST http://localhost:3000/users -H "Content-Type: application/json" -d ''
- Confirmed: 500 every time with empty body

## Phase 3: Diagnose
- bodyParser returns undefined for empty bodies
- Handler assumes req.body is always an object
- Root cause: no validation middleware before handler

## Phase 4: Fix
- Added validation middleware: if (!req.body) return res.status(400).json({error: "Missing body"})
- Test: empty body now returns 400 with descriptive error
- Full suite: all passing
```
