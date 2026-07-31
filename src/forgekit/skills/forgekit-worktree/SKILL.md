---
name: forgekit-worktree
version: 0.1.0
author: Forgekit
description: "When git worktree isolation is needed — create isolated workspace for feature work"
tags: [forgekit, git, worktree, isolation, branching]
related_skills: [forgekit-finish, forgekit-specify, forgekit-implement, forgekit-parallel]
---

# forgekit-worktree

Create isolated Git workspaces for feature work. Prevents main branch pollution and enables parallel workstreams.

## When to Use

- Starting a new feature that needs isolation from main branch
- Running multiple features in parallel (one worktree per feature)
- Working on experiments without affecting current branch
- Before dispatching parallel subagents (each gets own worktree)
- Using git worktrees instead of branches when isolation is critical

## Steps

### 1. Check Current Isolation

Before creating a new worktree, check if already isolated:

```bash
# Check if in a worktree
git rev-parse --git-common-dir

# List existing worktrees
git worktree list
```

If already in a worktree, reuse it. Don't create unnecessary duplicates.

### 2. Create Worktree from Feature Branch

```bash
# Create worktree with new branch
git worktree add ../project-feature-001 -b feature/001-my-feature

# Or checkout existing branch in worktree
git worktree add ../project-feature-001 feature/existing-branch
```

Location: sibling directory (../project-<feature-name>/)

### 3. Do Work in Worktree

```bash
cd ../project-feature-001
# All forgekit phases run here
forgekit constitution
forgekit specify
# ... etc
```

### 4. Return and Verify

```bash
cd ../project-original
# Review worktree changes
git -C ../project-feature-001 log --oneline -5
```

### 5. Cleanup After Merge

After work is merged (via forgekit-finish), remove worktree:

```bash
git worktree remove ../project-feature-001
git branch -d feature/001-my-feature  # if merged
```

## Output

| Artifact | Description |
|---|---|
| Isolated worktree directory | Separate working directory for feature |
| Feature branch | Named branch for the feature |
| No main branch pollution | All work isolated until merge |

## Pitfalls

- **Don't create worktrees inside the main repo.** Always use sibling directories (../project-feature-X/).
- **Don't forget to remove worktrees after merge.** `git worktree list` shows all; clean up regularly.
- **Don't run git operations on the same branch in multiple worktrees.** One branch = one worktree.
- **Don't use worktrees for trivial features.** Only when isolation is truly needed (parallel work, risky experiments).
- **Handle detached HEAD carefully.** If worktree shows detached HEAD, create a named branch immediately.

## Connected Skills

- **`/forgekit.finish`** — Merge decision + worktree cleanup
- **`/forgekit.specify`** — Spec generation happens in worktree
- **`/forgekit.implement`** — Subagents can be dispatched to worktrees
- **`/forgekit.parallel`** — Each parallel domain gets own worktree

## Examples

### Example 1: Single feature worktree
```bash
git worktree add ../myapp-auth -b feature/auth
cd ../myapp-auth
forgekit constitution
forgekit specify
forgekit implement
cd ../myapp
git worktree remove ../myapp-auth
```

### Example 2: Parallel features
```bash
# Feature A
git worktree add ../myapp-auth -b feature/auth
# Feature B
git worktree add ../myapp-api -b feature/api

# Each subagent works in own worktree
# Merge sequentially when done
```
