---
name: forgekit-receiving-review
version: 0.1.0
author: Forgekit
description: "When a human submits code review feedback — parse comments, categorize severity, auto-fix criticals, track review rounds"
tags: [forgekit, review, feedback, collaboration]
related_skills: [forgekit-review, forgekit-implement, forgekit-specify, forgekit-debug]
---

# Forgekit Receiving Review

Handle incoming code review feedback from humans. Parse review comments, categorize by severity, auto-fix critical issues, discuss suggestions, and track review rounds until approval.

## When to Use

- When a human reviewer leaves comments on a PR or code review
- After sharing `/forgekit.review` output with a team member
- When paste-dumping a review into the chat
- During iterative review rounds until approval

## Steps

1. **Parse the incoming review.** Accept review input in any format:
   - GitHub PR review comments (via API or paste)
   - Inline code comments (file:line — comment)
   - Free-form feedback paragraphs
   - Structured review (like `/forgekit.review` output from a human)

2. **Categorize each comment** into severity levels:

   ### 🔴 Critical (must fix)
   - Bugs or correctness issues
   - Security vulnerabilities
   - Data loss risks
   - Spec violations
   - Breaking changes

   ### 🟡 Suggestion (should consider)
   - Better approaches or patterns
   - Performance improvements
   - Readability improvements
   - Missing edge cases (non-critical)

   ### 🟢 Nit (optional)
   - Style preferences
   - Naming suggestions
   - Minor formatting

   ### ❓ Question (needs answer)
   - Reviewer asking for clarification
   - "Why did you do X this way?"
   - Architecture questions

3. **Load context** for each comment:
   - The source file and line referenced
   - The relevant spec section
   - The constitution principle (if any)
   - The original task spec from `.forgekit/tasks.md`

4. **Generate a response plan:**

   For **critical** issues:
   - Auto-fix immediately if the fix is clear
   - Show the diff to the user for approval
   - Run tests after fixing
   - Commit with message: `fix(review): <description> — from review round N`

   For **suggestions**:
   - Evaluate against the spec and constitution
   - If it improves the code without violating principles: apply
   - If it's a trade-off: present options to the user
   - If it conflicts with the spec: explain why and suggest a spec change instead

   For **nits**:
   - Apply if trivial (rename, format)
   - Skip if disruptive (major refactor for a naming preference)
   - Note in response: "Applied" or "Skipping because <reason>"

   For **questions**:
   - Answer with reference to spec, plan, or constitution
   - If the question reveals a gap in documentation, update the relevant forgekit file

5. **Apply fixes** following the same TDD approach:
   - Write/update test for the fix
   - Implement the fix
   - Run all tests
   - Commit

6. **Generate the review response:**

   ```markdown
   # Review Response — Round N
   Date: <date>

   ## Summary
   - 🔴 Critical: X items — all fixed
   - 🟡 Suggestions: Y items — Z applied, W discussed below
   - 🟢 Nits: V items — U applied, T skipped (reason below)
   - ❓ Questions: R items — answered below

   ## Resolved
   ### 🔴 [file:line] — <original comment>
   **Action**: Fixed in commit <hash>
   **What changed**: <description>

   ### 🟡 [file:line] — <original comment>
   **Action**: Applied — <explanation>

   ## Discussed
   ### 🟡 [file:line] — <original comment>
   **Response**: <explanation of why it wasn't changed, or alternative proposal>

   ### ❓ [file:line] — <original question>
   **Answer**: <answer with references>
   ```

7. **Save** the response to `.forgekit/review-round-N.md`.

8. **Track review rounds** in `.forgekit/review-tracker.md`:
   ```markdown
   | Round | Date | Criticals | Suggestions | Nits | Status |
   |-------|------|-----------|-------------|------|--------|
   | 1 | 2024-01-15 | 3 (3 fixed) | 5 (3 applied) | 8 (6 applied) | Changes pushed |
   | 2 | 2024-01-16 | 0 | 1 (1 applied) | 2 (1 applied) | Approved ✅ |
   ```

9. **Report status** to the user and indicate next step.

## Output

- `.forgekit/review-round-N.md` — response to each review round
- `.forgekit/review-tracker.md` — cumulative review progress
- Code fixes committed to the branch
- Clear status: "Changes pushed" or "Approved ✅"

## Connected Skills

- **← Prerequisite**: `/forgekit.review` (initial self-review) or human review request
- **← Context**: `/forgekit.specify` (for evaluating suggestions), `/forgekit.constitution`
- **→ Next**: `/forgekit.implement` (for applying fixes), then `/forgekit.review` (re-verify)
- **→ Parallel**: `/forgekit.debug` if review reveals bugs

## Examples

### Handling a GitHub PR review
```
User: Here's the review from Sarah:
      - auth.py:45 — "Use bcrypt, not plaintext passwords" (critical)
      - config.py:12 — "Consider using env vars instead of hardcoded" (suggestion)
      - utils.py:8 — "Rename x to retry_count" (nit)
      - "Why did you choose synchronous over async?" (question)

Agent: Categorizing review comments:
       🔴 Critical: 1 — auth.py:45 (security)
       🟡 Suggestion: 1 — config.py:12 (configurability)
       🟢 Nit: 1 — utils.py:8 (readability)
       ❓ Question: 1 — sync vs async architecture

       Applying critical fix:
       - auth.py:45: Replacing plaintext hash with bcrypt
       - Test: test_password_is_hashed_with_bcrypt → PASS
       - Commit: fix(auth): use bcrypt for password hashing — review round 1

       Applying nit:
       - utils.py:8: Renaming x → retry_count
       - Commit: chore: rename loop variable for clarity

       Discussing suggestion (env vars):
       → Constitution says "Explicit over implicit" — hardcoded defaults
         with env var overrides is more explicit than pure env vars.
         Suggesting: keep defaults, add env var override layer.
         User: "Good point, let's keep your approach."

       Answering question (sync vs async):
       → Spec section 2.3 defines request processing. Expected load is
         <100 req/s (spec NFR-001). Sync is simpler and meets requirements.
         If load exceeds spec, async migration is documented in plan.md.

       Review response saved to .forgekit/review-round-1.md
       Status: Changes pushed — awaiting Round 2
```

### Multi-round review until approval
```
Agent: Review Round 2 from Sarah:
       - No criticals
       - 1 suggestion: "Add retry logic for DB connection" (applied)
       - "LGTM, approved ✅"

       Status: ✅ Approved — all review rounds resolved
       Total rounds: 2
       Total fixes: 4 (1 critical, 2 suggestions, 1 nit)
```

## Pitfalls

- **Arguing with the reviewer.** Evaluate each comment objectively against the spec and constitution. If the reviewer is right, fix it. If not, explain with evidence — don't dismiss.
- **Auto-fixing suggestions without analysis.** Not every suggestion is an improvement. Some conflict with the spec or introduce complexity. Always evaluate first.
- **Losing review history.** Every round must be tracked. You need to know what was fixed in round 1 vs round 2 for accountability.
- **Not running tests after fixes.** A "fix" that breaks other tests isn't a fix. Always run the full suite.
- **Treating nits as criticals.** Nits are optional. Don't spend 20 minutes on a naming preference when there are real issues to address.
