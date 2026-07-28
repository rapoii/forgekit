# Forgekit

> Build software with structure. A development methodology toolkit that fuses [Spec-Driven Development](https://github.com/github/spec-kit) with [autonomous agent workflows](https://github.com/obra/superpowers).

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)

Forgekit gives your AI coding agent a structured development methodology — from brainstorming to specification, planning, implementation, review, and publication. It's not just a collection of prompts. It's a **complete workflow system** with CLI tools, skills, templates, and extension support.

## Why Forgekit?

Most AI coding agents jump straight into writing code. Forgekit makes them **think first**:

- **Brainstorm** before building — explore approaches, not just the first idea
- **Specify** before implementing — define what, not how
- **Plan** with bite-sized tasks — each 2-5 minutes, with exact file paths
- **Test-drive** development — red, green, refactor
- **Review** against spec and constitution — not just "does it work"
- **Converge** — find gaps between spec and implementation

## Quick Start

### Install

```bash
uv tool install forgekit --from git+https://github.com/rapoii/forgekit.git
```

### Initialize a project

```bash
cd my-project
forgekit init
```

This creates `.forgekit/` with constitution, spec, and config files.

### Use in your AI agent

Slash commands work in Hermes Agent, Claude Code, OpenCode, Codex, and more:

```
/forgekit.specify Build a photo album app with drag-and-drop
/forgekit.plan Use Vite + vanilla JS + SQLite
/forgekit.tasks
/forgekit.implement
```

Or just describe what you want — the bootstrap skill auto-activates:

```
I want to build a URL shortener with analytics
```

## Commands

### Foundation

| Command | What it does |
|---------|-------------|
| `forgekit init` | Initialize `.forgekit/` in your project |
| `/forgekit.constitution` | Define project principles and guidelines |
| `/forgekit.brainstorm` | Explore ideas before specifying |
| `/forgekit.clarify` | Resolve ambiguities in your spec |
| `/forgekit.specify` | Define what to build (requirements, user stories) |

### Planning

| Command | What it does |
|---------|-------------|
| `/forgekit.analyze` | Cross-artifact consistency check |
| `/forgekit.checklist` | Generate quality checklist from spec |
| `/forgekit.plan` | Create technical implementation plan |
| `/forgekit.tdd` | Test-driven development cycle |
| `/forgekit.tasks` | Break plan into bite-sized tasks |

### Execution

| Command | What it does |
|---------|-------------|
| `/forgekit.implement` | Subagent-driven execution |
| `/forgekit.review` | Code review + spec compliance |
| `/forgekit.receiving-review` | Handle incoming reviews |
| `/forgekit.debug` | Systematic debugging workflow |
| `/forgekit.parallel` | Dispatch parallel agents |

### Completion

| Command | What it does |
|---------|-------------|
| `/forgekit.verify` | Pre-completion verification |
| `/forgekit.converge` | Spec vs implementation gap analysis |
| `/forgekit.finish` | Git cleanup + branch finalization |
| `/forgekit.publish` | Tasks to GitHub Issues + deploy prep |

## Workflow

```
constitution → brainstorm → clarify → specify → analyze → checklist
     → plan → tdd → tasks → implement → review → debug
     → verify → converge → finish → publish
```

Not every feature needs all 18 steps. Forgekit is flexible:
- Small fix? Just `specify → implement → review`
- New feature? `brainstorm → specify → plan → tasks → implement → review → verify`
- Full project? Use the complete pipeline

## Project Structure

```
my-project/
├── .forgekit/
│   ├── config.yaml         Project config
│   ├── constitution.md     Project principles
│   ├── spec.md             Active specification
│   ├── plan.md             Technical plan
│   ├── tasks.md            Task breakdown
│   ├── analysis.md         Consistency analysis
│   ├── checklist.md        Quality checklist
│   ├── reviews/            Review history
│   └── specs/              Spec history per feature
├── .hermes.md              Auto-generated agent context
├── AGENTS.md               Universal agent context
└── src/                    Your code
```

## Extensions

Forgekit is extensible. Add domain-specific workflows:

```bash
forgekit extension add https://github.com/user/forgekit-web-extension
```

See [extensions/](extensions/) for details.

## Supported Agents

| Agent | Status |
|-------|--------|
| Hermes Agent | First-class support |
| Claude Code | Planned |
| OpenCode | Planned |
| Codex CLI | Planned |
| Cursor | Planned |
| Any agent with AGENTS.md | Works via AGENTS.md |

## Philosophy

Forgekit combines the best ideas from two projects:

- **[Spec Kit](https://github.com/github/spec-kit)** (GitHub) — Spec-Driven Development: define what to build before building it
- **[Superpowers](https://github.com/obra/superpowers)** (obra) — Autonomous agent workflows: subagent-driven development, TDD, systematic debugging

The result is a methodology that is:
- **Structured** — clear phases with defined inputs/outputs
- **Flexible** — use what you need, skip what you don't
- **Agent-native** — designed for AI coding agents, not humans manually following steps
- **Self-improving** — learns from each project, generates reusable skills

## License

MIT — see [LICENSE](LICENSE).

## Credits

Built by [Rafi Permana](https://github.com/rapoii).

Inspired by [Superpowers](https://github.com/obra/superpowers) by obra and [Spec Kit](https://github.com/github/spec-kit) by GitHub.
