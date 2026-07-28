"""Forgekit CLI — Development methodology toolkit.

Usage:
    forgekit init              Initialize .forgekit/ in current project
    forgekit <command>         Run a specific phase
    forgekit run               Run full pipeline
    forgekit status            Show project status
    forgekit list              List all available commands
"""

import os
import sys
import json
from pathlib import Path
from datetime import datetime

FORGEKIT_DIR = ".forgekit"
FORGEKIT_VERSION = "0.1.0"

COMMANDS = {
    # Meta commands
    "init": "Initialize .forgekit/ in current project",
    "status": "Show project forgekit status",
    "list": "List all available commands",
    "run": "Run full pipeline (interactive)",
    # Phase 1: Foundation
    "constitution": "Create project principles and guidelines",
    "brainstorm": "Explore ideas before specifying",
    "clarify": "Identify and resolve ambiguities",
    "specify": "Define what to build",
    # Phase 2: Planning
    "analyze": "Cross-artifact consistency check",
    "checklist": "Generate quality checklist from spec",
    "plan": "Create technical implementation plan",
    "tdd": "Test-driven development cycle",
    "tasks": "Break plan into bite-sized tasks",
    # Phase 3: Execution
    "implement": "Subagent-driven execution",
    "review": "Code review + spec compliance",
    "receiving-review": "Handle incoming code reviews",
    "debug": "Systematic debugging workflow",
    "parallel": "Dispatch parallel agents",
    # Phase 4: Completion
    "verify": "Pre-completion verification",
    "converge": "Spec vs implementation gap analysis",
    "finish": "Git cleanup + branch finalization",
    "publish": "Convert tasks to issues + deploy prep",
}

PHASES = {
    "foundation": ["constitution", "brainstorm", "clarify", "specify"],
    "planning": ["analyze", "checklist", "plan", "tdd", "tasks"],
    "execution": ["implement", "review", "receiving-review", "debug", "parallel"],
    "completion": ["verify", "converge", "finish", "publish"],
}


def get_forgekit_dir() -> Path:
    """Get the .forgekit directory path."""
    return Path.cwd() / FORGEKIT_DIR


def is_initialized() -> bool:
    """Check if forgekit is initialized in current directory."""
    return get_forgekit_dir().is_dir()


def cmd_init(args):
    """Initialize .forgekit/ in current project."""
    fk_dir = get_forgekit_dir()
    project_name = Path.cwd().name

    if fk_dir.exists() and not (args and "--force" in args):
        print(f"  Forgekit already initialized in {Path.cwd()}")
        print(f"  Use --force to reinitialize")
        return

    # Create directory structure
    dirs = [
        fk_dir,
        fk_dir / "reviews",
        fk_dir / "specs",
    ]
    for d in dirs:
        d.mkdir(parents=True, exist_ok=True)

    # Create config.yaml
    config = {
        "project": project_name,
        "version": FORGEKIT_VERSION,
        "initialized": datetime.now().isoformat(),
        "tech_stack": {},
        "phases_completed": [],
        "active_spec": None,
        "extensions": [],
    }
    config_path = fk_dir / "config.yaml"
    _write_yaml(config_path, config)

    # Create constitution.md from template
    constitution_path = fk_dir / "constitution.md"
    if not constitution_path.exists():
        constitution_path.write_text(_constitution_template(project_name), encoding="utf-8")

    # Create empty spec.md
    spec_path = fk_dir / "spec.md"
    if not spec_path.exists():
        spec_path.write_text("# Specification\n\nNo active specification yet. Run `/forgekit.specify` to create one.\n", encoding="utf-8")

    # Create .hermes.md (Hermes Agent project context)
    hermes_md = Path.cwd() / ".hermes.md"
    if not hermes_md.exists():
        hermes_md.write_text(
            f"# {project_name}\n\n"
            f"Project managed with [Forgekit](https://github.com/rapoii/forgekit).\n"
            f"Constitution: see `.forgekit/constitution.md`\n"
            f"Active spec: see `.forgekit/spec.md`\n\n"
            f"## Guidelines\n"
            f"- Follow the project constitution\n"
            f"- Use forgekit skills for structured development\n"
            f"- Test before marking tasks complete\n",
            encoding="utf-8",
        )

    # Create AGENTS.md (universal agent context)
    agents_md = Path.cwd() / "AGENTS.md"
    if not agents_md.exists():
        agents_md.write_text(
            f"# {project_name}\n\n"
            f"Managed with Forgekit methodology.\n"
            f"See `.forgekit/` for project specs, plans, and tasks.\n\n"
            f"## Development Workflow\n"
            f"1. Constitution first — follow project principles\n"
            f"2. Specify before implementing\n"
            f"3. Test-driven development\n"
            f"4. Review before merging\n",
            encoding="utf-8",
        )

    print(f"""
  Forgekit initialized!

  Project: {project_name}
  Location: {fk_dir}

  Created:
    .forgekit/           Project workspace
    .forgekit/config.yaml  Project config
    .forgekit/constitution.md  Project principles (edit this!)
    .forgekit/spec.md    Active specification
    .hermes.md           Hermes Agent context
    AGENTS.md            Universal agent context

  Next steps:
    1. Edit .forgekit/constitution.md with your project principles
    2. Use /forgekit.specify in your AI agent to define features
    3. Or run: forgekit specify
""")


def cmd_status(args):
    """Show project forgekit status."""
    if not is_initialized():
        print("  Forgekit not initialized. Run: forgekit init")
        return

    fk_dir = get_forgekit_dir()
    config = _read_yaml(fk_dir / "config.yaml")

    print(f"""
  Forgekit Status
  ===============
  Project: {config.get('project', 'unknown')}
  Version: {config.get('version', 'unknown')}
  Initialized: {config.get('initialized', 'unknown')}

  Phases completed: {', '.join(config.get('phases_completed', [])) or 'none yet'}
  Active spec: {config.get('active_spec', 'none')}

  Files:
    constitution.md  {'exists' if (fk_dir / 'constitution.md').exists() else 'missing'}
    spec.md          {'exists' if (fk_dir / 'spec.md').exists() else 'missing'}
    plan.md          {'exists' if (fk_dir / 'plan.md').exists() else 'missing'}
    tasks.md         {'exists' if (fk_dir / 'tasks.md').exists() else 'missing'}
    analysis.md      {'exists' if (fk_dir / 'analysis.md').exists() else 'missing'}
    checklist.md     {'exists' if (fk_dir / 'checklist.md').exists() else 'missing'}
""")


def cmd_list(args):
    """List all available commands."""
    print("""
  Forgekit Commands
  =================
""")
    for phase_name, commands in PHASES.items():
        print(f"  {phase_name.upper()}")
        for cmd_name in commands:
            desc = COMMANDS.get(cmd_name, "")
            print(f"    forgekit {cmd_name:<20s} {desc}")
        print()
    print(f"  META")
    for cmd_name in ["init", "status", "list", "run"]:
        desc = COMMANDS.get(cmd_name, "")
        print(f"    forgekit {cmd_name:<20s} {desc}")
    print()


def cmd_run(args):
    """Run full pipeline interactively."""
    if not is_initialized():
        print("  Forgekit not initialized. Run: forgekit init")
        return

    print("""
  Forgekit Full Pipeline
  ======================

  Foundation
    1. constitution  - Project principles
    2. brainstorm    - Explore ideas
    3. clarify       - Resolve ambiguities
    4. specify       - Define what to build

  Planning
    5. analyze       - Consistency check
    6. checklist     - Quality checklist
    7. plan          - Technical plan
    8. tdd           - Test-driven development
    9. tasks         - Break into tasks

  Execution
   10. implement     - Build it
   11. review        - Code review
   12. debug         - Fix issues

  Completion
   13. verify        - Pre-completion check
   14. converge      - Spec vs reality
   15. finish        - Git cleanup
   16. publish       - Deploy prep

  In your AI agent, use: /forgekit.<command>
  For auto-pilot, just describe what you want to build.
""")


def cmd_phase(args):
    """Run a specific phase command."""
    cmd_name = args[0] if args else None

    if not cmd_name:
        print("  Usage: forgekit <command>")
        print("  Run 'forgekit list' to see all commands")
        return

    if cmd_name not in COMMANDS:
        print(f"  Unknown command: {cmd_name}")
        print(f"  Run 'forgekit list' to see all commands")
        return

    if cmd_name in ("init", "status", "list", "run"):
        # Handled by dedicated functions
        return

    if not is_initialized():
        print("  Forgekit not initialized. Run: forgekit init")
        return

    fk_dir = get_forgekit_dir()
    config = _read_yaml(fk_dir / "config.yaml")

    print(f"""
  forgekit {cmd_name}
  {'=' * (len(cmd_name) + 10)}

  Phase: {COMMANDS[cmd_name]}

  To execute this phase, use the corresponding skill in your AI agent:
    /forgekit.{cmd_name}

  Or load the skill:
    /skill forgekit-{cmd_name}
""")

    # Update config with phase tracking
    if cmd_name not in config.get("phases_completed", []):
        config.setdefault("phases_completed", []).append(cmd_name)
        _write_yaml(fk_dir / "config.yaml", config)


def main():
    """Main CLI entry point."""
    args = sys.argv[1:]

    if not args or args[0] in ("-h", "--help"):
        print(f"""
  Forgekit v{FORGEKIT_VERSION}
  Development methodology toolkit

  Usage: forgekit <command> [options]

  Commands:
    init        Initialize .forgekit/ in current project
    status      Show project status
    list        List all available commands
    run         Show full pipeline overview
    <command>   Run a specific phase (see 'forgekit list')

  Slash commands (in AI agents):
    /forgekit.<command>   Run phase via skill

  More: https://github.com/rapoii/forgekit
""")
        return

    cmd = args[0]
    rest = args[1:]

    if cmd == "init":
        cmd_init(rest)
    elif cmd == "status":
        cmd_status(rest)
    elif cmd == "list":
        cmd_list(rest)
    elif cmd == "run":
        cmd_run(rest)
    else:
        cmd_phase(args)


def _write_yaml(path: Path, data: dict):
    """Write a simple YAML file (no external dependency)."""
    lines = []
    for key, value in data.items():
        if isinstance(value, list):
            lines.append(f"{key}:")
            for item in value:
                if isinstance(item, dict):
                    lines.append(f"  - {json.dumps(item)}")
                else:
                    lines.append(f"  - {item}")
        elif isinstance(value, dict):
            lines.append(f"{key}:")
            for k, v in value.items():
                lines.append(f"  {k}: {v}")
        elif value is None:
            lines.append(f"{key}: null")
        else:
            lines.append(f"{key}: {value}")
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def _read_yaml(path: Path) -> dict:
    """Read a simple YAML file (no external dependency)."""
    if not path.exists():
        return {}
    result = {}
    current_key = None
    current_list = None
    for line in path.read_text(encoding="utf-8").splitlines():
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            continue
        if stripped.endswith(":") and not stripped.startswith("-"):
            if current_list is not None and current_key:
                result[current_key] = current_list
            current_key = stripped[:-1].strip()
            current_list = []
            continue
        if stripped.startswith("- "):
            if current_list is not None:
                item = stripped[2:].strip()
                try:
                    item = json.loads(item)
                except (json.JSONDecodeError, ValueError):
                    pass
                current_list.append(item)
            continue
        if ":" in stripped and current_list is not None:
            # This means the list is done, we're in a new key
            if current_key and current_list is not None:
                result[current_key] = current_list
                current_list = None
            key, _, val = stripped.partition(":")
            result[key.strip()] = val.strip()
            current_key = None
        elif ":" in stripped:
            key, _, val = stripped.partition(":")
            result[key.strip()] = val.strip()
    if current_key and current_list is not None:
        result[current_key] = current_list
    return result


def _constitution_template(project_name: str) -> str:
    return f"""# {project_name} Constitution

> This document defines the governing principles for {project_name}.
> Edit this to match your project's values and standards.

## Code Quality
- Write clean, readable code
- Follow DRY (Don't Repeat Yourself) principles
- Follow YAGNI (You Aren't Gonna Need It) — build only what's needed
- Meaningful names for variables, functions, and classes

## Testing
- Test-driven development (TDD) when possible
- Write failing test first, then implement
- All tests must pass before marking a task complete
- Aim for meaningful coverage, not 100% for the sake of it

## Architecture
- Keep it simple — prefer straightforward solutions
- Modular design — low coupling, high cohesion
- Document non-obvious decisions with comments

## Git Workflow
- Descriptive commit messages (type: description)
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
"""


if __name__ == "__main__":
    main()
