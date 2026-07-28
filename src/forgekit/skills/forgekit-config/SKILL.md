---
name: forgekit-config
version: 0.1.0
author: Forgekit
description: "Manage .forgekit/config.yaml — project setup, tech stack, phase tracking, extensions, and agent config generation"
tags: [forgekit, config, setup, initialization, meta]
related_skills: [forgekit-constitution, forgekit-bootstrap]
---

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
