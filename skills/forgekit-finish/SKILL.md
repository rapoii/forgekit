---
name: forgekit-finish
version: 0.1.0
author: Forgekit
description: "When verification passes — clean up git history, update docs, remove temp files, and finalize the branch for review or publish"
tags: [forgekit, git, cleanup, finalization, branching]
related_skills: [forgekit-verify, forgekit-review, forgekit-publish]
---

# Forgekit Finish

Git cleanup and branch finalization adapted from Superpowers. Squashes messy commits, updates project docs, removes dead code and temp files, and ensures the branch is clean and reviewable.

## When to Use

- After `/forgekit.verify` returns PASS
- Before `/forgekit.publish` — the branch must be clean
- When a feature is functionally complete but the git history is messy
- When temp files, debug logging, or TODO comments have accumulated

## Prerequisites

- `/forgekit.verify` must have passed (don't finish what hasn't been verified)
- All tasks in `.forgekit/tasks/` should be `done`

## Steps

### Step 1: Review Git History

1. View the branch's commit log:
   ```bash
   git log --oneline main..HEAD
   ```
2. Identify commits that should be squashed or reorganized:
   - "WIP" or "fix typo" commits
   - Multiple commits for the same logical change
   - Commits that break the build (even if later fixed)
3. Plan the reorganization — group commits by logical unit.

### Step 2: Clean Up Commits

**Option A: Interactive rebase** (preferred for clean history):
```bash
git rebase -i main
```
- Squash related commits
- Reorder for logical flow
- Rewrite commit messages to be descriptive

**Option B: Soft reset + recommit** (for messy branches):
```bash
git reset --soft main
git commit -m "feat: <feature description>

<summary of all changes>"
```

**Option C: No rebase** (if history is already clean or team prefers merge commits):
- Skip this step, proceed to cleanup.

### Step 3: Update Documentation

1. **README.md** — update if the feature changes usage, adds CLI commands, or modifies the public API:
   - Installation steps (if dependencies changed)
   - Usage examples
   - New configuration options

2. **CHANGELOG.md** — add entry for the feature:
   ```markdown
   ## [Unreleased]
   ### Added
   - <feature description> (#issue)
   ### Changed
   - <any breaking changes>
   ### Fixed
   - <any bugs fixed as part of this work>
   ```

3. **API docs / JSDoc / docstrings** — ensure all new public APIs are documented.

4. **Migration guide** — if there are breaking changes, document how to migrate.

### Step 4: Clean Up Code

1. **Remove dead code:**
   ```bash
   # Find unused exports (project-specific)
   # For JS/TS: npx ts-prune
   # For Python: vulture src/ --min-confidence 80
   ```

2. **Remove debug logging:**
   - Search for `console.log`, `print()`, `debugger`, `TODO: remove`
   - Remove or convert to proper logging

3. **Remove temp files:**
   ```bash
   git clean -fd --dry-run  # preview what would be removed
   ```

4. **Check .gitignore:**
   - Ensure build artifacts are ignored
   - Ensure IDE configs are ignored
   - Ensure temp/debug files are ignored
   - Add any new patterns needed

5. **Run lint one more time:**
   ```bash
   npm run lint -- --fix  # or equivalent
   ```

### Step 5: Update Task Status

1. Ensure all tasks in `.forgekit/tasks/` are marked `done`.
2. Archive completed tasks if the project uses task archival.
3. Update any progress tracking (if used).

### Step 6: Final Checks

1. **Branch is up to date with main:**
   ```bash
   git fetch origin
   git rebase origin/main
   ```

2. **No merge conflicts:**
   ```bash
   git status  # should be clean
   ```

3. **Build succeeds:**
   ```bash
   npm run build  # or equivalent
   ```

4. **Tests still pass** (one last time):
   ```bash
   npm test
   ```

## Output

- Clean git history with meaningful commit messages
- Updated README, CHANGELOG, and API docs
- No dead code, debug logging, or temp files
- .gitignore updated
- Branch rebased on latest main
- Build and tests passing
- Ready for `/forgekit.review` or `/forgekit.publish`

## Connected Skills

- **Before:** `/forgekit.verify` — must have passed
- **After:** `/forgekit.review` — submit for code review
- **After:** `/forgekit.publish` — prepare for release
- **If issues found:** `/forgekit.debug` — if cleanup reveals problems

## Pitfalls

- **Don't rebase published branches.** If others are working on this branch, coordinate first.
- **Don't squash too aggressively.** Keep logical boundaries — "add auth" and "add rate limiting" should be separate commits even if developed together.
- **Don't skip the final test run.** Cleanup operations can accidentally break things.
- **Don't forget the CHANGELOG.** Users and reviewers need to know what changed.
- **Don't leave TODO comments.** Either resolve them or convert to tracked issues.
