---
name: forgekit-publish
version: 0.1.0
author: Forgekit
description: "When the feature branch is finalized — create GitHub Issues from tasks, prepare release notes, tag a version, and run the deploy checklist"
tags: [forgekit, publishing, github, release, deployment]
related_skills: [forgekit-finish, forgekit-verify, forgekit-brainstorm]
---

# Forgekit Publish

Final publishing workflow: convert remaining task tracking to GitHub Issues, generate release notes, tag the version, and run the deployment checklist. The last step in a Forgekit feature cycle.

## When to Use

- After `/forgekit.finish` — the branch is clean and ready
- When a feature is complete and needs to be released or merged
- When converting local task tracking to permanent GitHub Issues
- When preparing a versioned release

## Prerequisites

- `/forgekit.finish` must have completed
- Branch is clean, rebased, tests passing
- CHANGELOG is updated

## Steps

### Step 1: Create GitHub Issues from Tasks

1. Read all tasks from `.forgekit/tasks/`.
2. For each completed task, create a GitHub Issue (if one doesn't already exist):
   ```bash
   gh issue create \
     --title "feat: <task title>" \
     --body "Implemented in <branch>. Spec: .forgekit/specs/<feature>/spec.md" \
     --label "feature,forgekit"
   ```
3. For any remaining/future tasks (from `/forgekit.converge` gaps):
   ```bash
   gh issue create \
     --title "<task title>" \
     --body "Remaining work from <feature>. Priority: <high/medium/low>" \
     --label "enhancement,forgekit"
   ```
4. Link issues to the PR or milestone as appropriate.

### Step 2: Prepare Release Notes

Generate or refine release notes for the version:

```markdown
# v<version> — <feature name>

## What's New
- <high-level description of the feature>

## Changes
- <specific change 1>
- <specific change 2>

## Breaking Changes (if any)
- <breaking change + migration steps>

## Bug Fixes (if any)
- <bug fix>

## Internal
- <refactoring, tooling, etc.>

## Issues Closed
- Closes #N
- Refs #M
```

Save to:
- `.forgekit/specs/<feature>/release-notes.md` (project-local)
- Update `CHANGELOG.md` with the versioned entry

### Step 3: Tag the Version

1. Determine the version number:
   - **Major** (X.0.0): breaking changes
   - **Minor** (0.X.0): new features, backward-compatible
   - **Patch** (0.0.X): bug fixes only
   - Follow the project's existing versioning scheme

2. Create the tag:
   ```bash
   git tag -a v<version> -m "Release v<version>: <feature name>"
   ```

3. Verify the tag:
   ```bash
   git tag -v v<version>  # or just git log --oneline v<version>
   ```

### Step 4: Deploy Prep Checklist

Run through the deployment readiness checklist:

- [ ] **All tests pass** in CI (not just locally)
- [ ] **No secrets in code** — run a scan:
  ```bash
  # Check for common secret patterns
  git secrets --scan  # if git-secrets is installed
  # or manual grep for API keys, tokens, passwords
  ```
- [ ] **Dependencies are up to date** — no known vulnerabilities:
  ```bash
  npm audit          # Node.js
  pip-audit          # Python
  ```
- [ ] **Environment variables documented** — any new config is listed in README or `.env.example`
- [ ] **Database migrations** (if any) are backward-compatible and tested
- [ ] **Feature flags** (if any) are set to the correct default
- [ ] **Monitoring/alerting** (if applicable) is configured for new endpoints
- [ ] **Rollback plan** is documented if the deploy goes wrong
- [ ] **Stakeholders notified** — team knows a release is coming

### Step 5: Open Pull Request

If the feature is on a branch:

```bash
gh pr create \
  --title "feat: <feature name>" \
  --body "$(cat .forgekit/specs/<feature>/release-notes.md)" \
  --label "feature" \
  --milestone "v<version>"
```

Include in the PR body:
- Link to the spec
- Link to the verification report
- Link to release notes
- Screenshots or demos (if applicable)

### Step 6: Push and Deploy

1. Push the branch and tags:
   ```bash
   git push origin HEAD --tags
   ```

2. Wait for CI to pass on the PR.

3. Merge the PR:
   ```bash
   gh pr merge --squash  # or --merge, per team convention
   ```

4. Deploy (project-specific):
   ```bash
   # Examples:
   # npm run deploy
   # gh workflow run deploy.yml
   # fly deploy
   ```

5. Verify the deployment:
   ```bash
   # Health check, smoke test, etc.
   curl https://<production-url>/health
   ```

## Output

- GitHub Issues created for all tasks
- Release notes published
- Version tagged in git
- Deploy checklist completed
- PR opened, CI passed, merged
- Feature deployed (or deployment initiated)
- Project ready for the next cycle

## Connected Skills

- **Before:** `/forgekit.finish` — branch must be finalized
- **Before:** `/forgekit.verify` — verification must have passed
- **After:** `/forgekit.brainstorm` — start the next feature!
- **After:** Done! 🎉

## Pitfalls

- **Don't skip the secret scan.** One leaked API key in a commit is a security incident.
- **Don't tag before CI passes.** Tags should only point at verified commits.
- **Don't forget to push tags.** `git push` doesn't push tags by default — use `--tags`.
- **Don't deploy on Friday.** Plan deployments for when the team is available to handle issues.
- **Don't skip the rollback plan.** Know how to undo the deploy before you do it.
- **Don't create duplicate issues.** Check if GitHub Issues already exist before creating new ones.

## Example

```bash
# After /forgekit.finish for "user-auth" feature:

# 1. Create issues
gh issue create --title "feat: Implement JWT auth" --body "Done in PR #42" --label "feature"
gh issue create --title "feat: Add refresh token rotation" --body "Future work from convergence report" --label "enhancement"

# 2. Tag
git tag -a v1.2.0 -m "Release v1.2.0: User Authentication"

# 3. PR
gh pr create --title "feat: User Authentication" --body "..." --milestone "v1.2.0"

# 4. Push & merge
git push origin HEAD --tags
gh pr merge --squash
```
