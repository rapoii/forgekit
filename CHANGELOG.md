# Forgekit v0.1.0 — Initial Release

**Universal development methodology toolkit.** Fusion of [Superpowers](https://github.com/obra/superpowers) + [Spec Kit](https://github.com/github/spec-kit) for AI coding agents.

## What is Forgekit?

Forgekit is a structured development workflow that guides AI agents through a 18-phase pipeline — from brainstorming to shipping. It combines:

- **Spec-Driven Development** (from Spec Kit): constitution → specify → plan → tasks
- **Autonomous Agent Workflows** (from Superpowers): subagent dispatch, TDD, parallel execution
- **Deep Agent Integration**: auto-trigger, skill files, agent config generation

## Install

```bash
# For Hermes Agent users
uv tool install forgekit --from git+https://github.com/rapoii/forgekit.git
forgekit install-hermes

# For any AI agent (universal)
uv tool install forgekit --from git+https://github.com/rapoii/forgekit.git
forgekit init
```

## Features

### CLI Tool (18 commands)
- `forgekit init` — scaffold `.forgekit/` project workspace
- `forgekit install-hermes` — one-command Hermes Agent setup
- `forgekit list/status/run` — project management
- 18 phase commands (constitution → publish)

### 20 Skill Files
Auto-triggered workflow skills for AI agents:
- **Foundation:** constitution, brainstorm, clarify, specify
- **Planning:** analyze, checklist, plan, tdd, tasks
- **Execution:** implement, review, receiving-review, debug, parallel
- **Completion:** verify, converge, finish, publish
- **Meta:** bootstrap, config

### Auto-Trigger (4 Layers)
1. **SOUL.md** — global section (always loaded)
2. **AGENTS.md** — home directory trigger rules
3. **Skill description** — bootstrap matches "mau bikin X"
4. **Project .hermes.md** — per-project context

### Templates
5 reusable templates: spec, plan, constitution, checklist, tasks

### Extensions System
Extensible architecture for custom skills and workflows

## Tested

- 52/52 component tests PASS
- 20/20 skills YAML valid + sections complete
- 11/11 user scenarios PASS
- 25/25 CLI commands PASS
- 37/37 trigger mechanism tests PASS
- 8 bugs found and fixed
- All verified with concrete evidence

## Supported Platforms

- **Hermes Agent** (primary) — full integration with auto-trigger
- **Claude Code** — via AGENTS.md + skill files
- **OpenCode** — via AGENTS.md + skill files
- **Codex** — via AGENTS.md + skill files
- **Any AI agent** — via forgekit CLI + .forgekit/ artifacts

## Commits

```
99f5bdf fix: replace hand-rolled YAML parser with PyYAML
a56a89d fix: cross-reference 'forgekit-spec' → 'forgekit-specify'
337bddb fix: _write_yaml empty list/dict serialization
123cfc2 fix: add missing bootstrap trigger keywords
99398b3 feat: add install-hermes command + bundled skills
c55f72d feat: forgekit v0.1.0 — development methodology toolkit
```

## Links

- **Repo:** https://github.com/rapoii/forgekit
- **Issues:** https://github.com/rapoii/forgekit/issues
- **License:** MIT
