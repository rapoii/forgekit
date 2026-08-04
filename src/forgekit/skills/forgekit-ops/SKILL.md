---
name: forgekit-ops
version: 0.1.0
author: Forgekit
description: "Macro-skill for forgekit-ops phase. Combines: finish, publish, config, writing-skills"
tags: [forgekit, ops]
---

# Forgekit Ops

This is a consolidated macro-skill for Forgekit to optimize context length.
It contains the instructions for multiple related phases. Read the specific section for your current phase.

## FORGEKIT-FINISH
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

## FORGEKIT-PUBLISH
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

## FORGEKIT-CONFIG
# forgekit-config

Manage the Forgekit project configuration. Handles initialization, tech stack tracking, phase completion status, extensions, and agent-specific config generation.

## When to Use

- User says "init forgekit" or "set up forgekit"
- User wants to update tech stack or project settings
- User wants to see current project status
- User asks about extensions or presets
- User needs agent-specific configs generated (`.hermes.md`, `AGENTS.md`, `CLAUDE.md`)
- Bootstrap skill routes here for new project setup

## Steps

### Action: `init`

Initialize a new Forgekit project:

1. Create `.forgekit/` directory
2. Create `.forgekit/config.yaml` with defaults:

```yaml
# Forgekit Project Configuration
version: "0.1.0"
project:
  name: ""  # Filled from user input
  description: ""
  created: "YYYY-MM-DD"

# Tech stack (auto-detected or user-specified)
tech_stack:
  language: ""
  framework: ""
  runtime: ""
  package_manager: ""
  test_framework: ""
  linter: ""

# Phase tracking
phases:
  constitution: false
  brainstorm: false
  clarify: false
  specify: false
  analyze: false
  checklist: false
  plan: false
  tdd: false
  tasks: false
  implement: false
  review: false
  debug: false
  verify: false
  converge: false
  finish: false
  publish: false

# Active spec (current feature being worked on)
active_spec: ""

# Extensions (optional modules)
extensions: []

# Agent preferences
agent:
  name: "hermes"  # hermes, claude-code, opencode, codex
  conventions: "default"
```

3. Auto-detect tech stack from existing files:
   - `package.json` → Node.js project
   - `requirements.txt` / `pyproject.toml` / `setup.py` → Python project
   - `Cargo.toml` → Rust project
   - `go.mod` → Go project
   - `pom.xml` / `build.gradle` → Java project
   - `.csproj` → C# project

4. Ask user for project name and description if not obvious
5. Print summary of detected configuration

### Action: `show` / `status`

Display current project state:

```
📋 Forgekit Project: my-app
━━━━━━━━━━━━━━━━━━━━━━━━━━
Tech: Python / FastAPI / pytest
Active Spec: user-auth

Phases Completed:
  ✅ constitution
  ✅ brainstorm
  ✅ clarify
  ✅ specify
  ⬜ analyze
  ⬜ plan
  ...

Next recommended: /forgekit.analyze
```

### Action: `set`

Update a config value:

```
/forgekit.config set tech_stack.framework=FastAPI
/forgekit.config set project.description="Task management API"
/forgekit.config set active_spec=user-auth
```

### Action: `phase`

Mark a phase as completed or pending:

```yaml
# Mark phase complete
/forgekit.config phase constitution done
# Mark phase pending (reset)
/forgekit.config phase plan pending
```

### Action: `agents`

Generate agent-specific configuration files from the Forgekit constitution:

1. Read `.forgekit/constitution.md`
2. Generate:

**`.hermes.md`** (for Hermes Agent):
```markdown
# Project Conventions

[Extracted from constitution — coding standards, git workflow, testing requirements]

## Forgekit

This project uses Forgekit for spec-driven development.
Available commands: /forgekit.bootstrap, /forgekit.specify, /forgekit.plan, etc.
```

**`AGENTS.md`** (for Claude Code):
```markdown
# Agent Instructions

[Extracted from constitution]

## Workflow

This project follows Forgekit spec-driven development.
Before coding, ensure a spec exists in .forgekit/spec.md.
```

**`CLAUDE.md`** (for Claude-specific):
```markdown
# Claude Instructions

[Extracted from constitution + Claude-specific conventions]
```

3. Only overwrite if user confirms (these may have manual edits)

### Action: `extension`

Manage Forgekit extensions:

```
/forgekit.config extension add github-integration
/forgekit.config extension remove ci-cd
/forgekit.config extension list
```

Extensions are stored in `config.yaml` under `extensions: []`.

## Output

| Action | File(s) Created/Modified |
|---|---|
| `init` | `.forgekit/config.yaml` |
| `set` | `.forgekit/config.yaml` |
| `phase` | `.forgekit/config.yaml` |
| `agents` | `.hermes.md`, `AGENTS.md`, `CLAUDE.md` |
| `extension` | `.forgekit/config.yaml` |

## Connected Skills

- **`/forgekit.constitution`** — Constitution feeds into agent config generation
- **`/forgekit.bootstrap`** — Bootstrap checks config to determine project state
- **`/forgekit.specify`** — Updates `active_spec` in config
- All other skills — Read `config.yaml` to check prerequisites

## Examples

### Example 1: New Project Init
```
User: "init forgekit"
Agent: [detects package.json → Node.js project]
Agent: "Detected: Node.js project with Express. What's the project name?"
User: "taskflow"
Agent: [creates .forgekit/config.yaml]
Agent: "✅ Forgekit initialized for 'taskflow' (Node.js / Express / Jest)"
Agent: "Next: /forgekit.constitution to define your project principles"
```

### Example 2: Generate Agent Configs
```
User: "generate agent configs"
Agent: [reads .forgekit/constitution.md]
Agent: [generates .hermes.md, AGENTS.md, CLAUDE.md]
Agent: "Generated 3 agent config files from your constitution."
```

## Pitfalls

- **Don't overwrite agent configs silently.** Always check if `.hermes.md` / `AGENTS.md` / `CLAUDE.md` exist and ask before overwriting.
- **Tech stack detection is best-effort.** If ambiguous (e.g., both `package.json` and `requirements.txt`), ask the user.
- **Phase tracking is advisory, not enforced.** Skills can still run even if prerequisite phases aren't marked complete — but they should warn.
- **Config is YAML.** Be careful with special characters, use proper YAML syntax.

## FORGEKIT-WRITING-SKILLS
# forgekit-writing-skills

How to create new Forgekit skills using TDD applied to process documentation. The same RED-GREEN-REFACTOR discipline that applies to code applies to skills.

## When to Use

- Adding new skills to the Forgekit skill pack
- Modifying existing skills based on observed gaps
- Adapting skills for new AI agents or platforms
- Auditing whether a skill actually works (compliance test)

## Steps

### 1. Write Pressure Scenario Tests (RED — Baseline)

Before writing a skill, write a scenario that exposes the gap:

```markdown
## Pressure Scenario 1: Vague request

User: "mau bikin sesuatu tapi ga tau apa"
Agent: [skips /forgekit.brainstorm, jumps to coding]

Expected: Agent should load forgekit-brainstorm FIRST
```

Create 2-3 scenarios that test the EXACT behavior you want.

### 2. Write the Skill Document (GREEN)

Write the skill in SKILL.md format:

```yaml
---
name: forgekit-YOUR-SKILL
version: 0.1.0
description: "[Exact trigger phrase]"
tags: [forgekit, ...]
related_skills: [...]
---

# forgekit-YOUR-SKILL

## When to Use
[Specific, testable conditions]

## Steps
[Numbered, actionable steps]

## Output
[What artifacts to produce]

## Pitfalls
[What NOT to do]

## Connected Skills
[How this skill chains]
```

### 3. Verify Agent Compliance (GREEN Test)

Run the pressure scenarios and verify the agent now follows the skill:

```bash
# Test 1: Vague request
You: "mau bikin sesuatu tapi ga tau apa"
Expected: Agent loads forgekit-brainstorm, NOT jumps to coding

# Test 2: Trigger phrase match
You: "[exact phrase from description]"
Expected: Agent loads the skill
```

### 4. Close Loopholes (REFACTOR)

If agent finds rationalizations or corner cases:

- Add explicit prohibitions in Pitfalls section
- Tighten the Steps with more specificity
- Add Examples section showing correct behavior
- Test again until scenarios pass

## Output

| Artifact | Description |
|---|---|
| `skills/forgekit-{name}/SKILL.md` | New skill file |
| Pressure scenarios | Documented test cases |
| Compliance evidence | Screenshots/logs showing skill activation |

## Pitfalls

- **Don't write skills for problems that don't exist yet.** Use skills when there's repeated behavior you want to enforce.
- **Don't include too many steps.** 3-7 steps is the sweet spot. More than that and agents skip them.
- **Don't be vague in the description.** The description is what triggers the skill — be specific about phrases.
- **Don't skip the RED phase.** Writing scenarios first ensures the skill actually solves something.
- **Don't make skills mandatory for everything.** Some work is fine without a skill. Over-applying skills creates bureaucracy.

## Connected Skills

- **`/forgekit.bootstrap`** — Bootstrap signals when writing-skills is needed
- **`/forgekit.tdd`** — RED-GREEN-REFACTOR same methodology
- **`/forgekit.config`** — Register new skills in project config
- **`/forgekit.brainstorm`** — New skills may need to be brainstormed first if scope is unclear

## Examples

### Example 1: Creating a new skill
```
Scenario: User keeps asking about logging best practices
1. Write RED scenario: "agent suggests print() instead of using logging library"
2. Write skill: forgekit-logging with trigger "logging best practices"
3. Test: Run scenario, verify agent loads forgekit-logging
4. Close loopholes: Add Pitfalls about print statements, test again
```

### Example 2: Improving an existing skill
```
Scenario: forgekit-review is too slow
1. Write RED scenario: "review takes 3 hours for trivial PR"
2. Read existing skill, find bottleneck
3. Add step about scope-based review (small/medium/large PR)
4. Test: Verify review time reduced, quality maintained
```

