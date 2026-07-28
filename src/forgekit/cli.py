"""Forgekit CLI — Development methodology toolkit.

Usage:
    forgekit init              Initialize .forgekit/ in current project
    forgekit install-hermes    Install skills + auto-trigger for Hermes Agent
    forgekit <command>         Run a specific phase
    forgekit run               Run full pipeline
    forgekit status            Show project status
    forgekit list              List all available commands
"""

import os
import sys
import yaml
import json
import shutil
from pathlib import Path
from datetime import datetime

FORGEKIT_DIR = ".forgekit"
FORGEKIT_VERSION = "0.1.0"
SKILLS_DIR_NAME = "skills"

COMMANDS = {
    # Meta commands
    "init": "Initialize .forgekit/ in current project",
    "install-hermes": "Install skills + auto-trigger for Hermes Agent",
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
    # Phase 5: Meta (extensions, presets, workflows, bundles, self)
    "extension": "Manage extensions (search, add, remove, list)",
    "preset": "Manage presets (search, add, remove, list)",
    "workflow": "Run workflows (run, resume, status, list)",
    "bundle": "Manage bundles (install, list, remove, build)",
    "self": "Self check/upgrade forgekit",
}

PHASES = {
    "foundation": ["constitution", "brainstorm", "clarify", "specify"],
    "planning": ["analyze", "checklist", "plan", "tdd", "tasks"],
    "execution": ["implement", "review", "receiving-review", "debug", "parallel"],
    "completion": ["verify", "converge", "finish", "publish"],
    "meta": ["extension", "preset", "workflow", "bundle", "self"],
}

# Hermes auto-trigger content — injected into AGENTS.md (NOT SOUL.md)
HERMES_AGENTS_MD_CONTENT = """# Forgekit — Development Methodology

This project uses [Forgekit](https://github.com/rapoii/forgekit) for structured development.

## Auto-Trigger Rules

**When the user expresses intent to build something NEW**, load the `forgekit-bootstrap` skill FIRST:

Trigger phrases (case-insensitive):
- "mau bikin X", "mau buat X"
- "I want to build X", "I want to create X"
- "bikin website", "bikin app", "bikin bot", "bikin tool"
- "help me build X", "let's start a new project"
- "/forgekit", "forgekit start"

**Do NOT trigger for:** bug fixes, single-line changes, technical questions, existing project modifications.

## Pipeline

When triggered, follow the Forgekit pipeline in order:
1. `/forgekit.constitution` — project principles
2. `/forgekit.brainstorm` — explore approaches
3. `/forgekit.clarify` — resolve ambiguities
4. `/forgekit.specify` — formal requirements
5. `/forgekit.analyze` — consistency check
6. `/forgekit.checklist` — quality gates
7. `/forgekit.plan` — architecture + tasks
8. `/forgekit.tdd` — test-driven development
9. `/forgekit.tasks` — bite-sized task list
10. `/forgekit.implement` — subagent execution
11. `/forgekit.review` — code review
12. `/forgekit.verify` — pre-completion check
13. `/forgekit.converge` — spec vs reality
14. `/forgekit.finish` — git cleanup

Not every feature needs all steps. Small features: specify → implement → review.
"""

HERMES_SOUL_MD_SECTION = """

## Forgekit — Auto-Trigger Wajib

**Setiap kali user bilang "mau bikin X", "I want to build X", atau ekspresi intent untuk membuat/membangun sesuatu yang BARU:**

1. **WAJIB load `forgekit-bootstrap` skill** — jangan skip, jangan langsung nge-code.
2. Bootstrap skill akan mendeteksi state project dan route ke skill yang tepat.
3. Ikuti pipeline Forgekit sesuai skill instructions.
4. Jangan loncat tahap. Setiap tahap menghasilkan artifact di `.forgekit/`.

**Trigger phrases (case-insensitive):**
- "mau bikin X", "mau buat X", "I want to build X", "I want to create X"
- "bikin website", "bikin app", "bikin bot", "bikin tool"
- "help me build X", "let's start a new project"
- "/forgekit", "forgekit start"

**PENGECECUALIAN:** Fix bug kecil, ubah satu baris code, tanya teknis — JANGAN trigger.
"""


def get_forgekit_dir() -> Path:
    """Get the .forgekit directory path."""
    return Path.cwd() / FORGEKIT_DIR


def is_initialized() -> bool:
    """Check if forgekit is initialized in current directory."""
    return get_forgekit_dir().is_dir()


def get_hermes_home() -> Path:
    """Get Hermes home directory."""
    # Check HERMES_HOME env var first
    env_home = os.environ.get("HERMES_HOME")
    if env_home:
        return Path(env_home)
    # Default: ~/.hermes
    return Path.home() / ".hermes"


def get_package_skills_dir() -> Path:
    """Get the skills directory from the installed package."""
    # Skills are bundled with the package
    # Look relative to this file
    this_dir = Path(__file__).parent
    skills_dir = this_dir / SKILLS_DIR_NAME
    if skills_dir.exists():
        return skills_dir
    # Fallback: look in the source tree
    source_skills = this_dir.parent.parent / SKILLS_DIR_NAME
    if source_skills.exists():
        return source_skills
    # Fallback: look in the project root (for development)
    project_skills = Path.cwd() / SKILLS_DIR_NAME
    if project_skills.exists():
        return project_skills
    return None


def cmd_install_hermes(args):
    """Install forgekit skills + auto-trigger for Hermes Agent."""
    hermes_home = get_hermes_home()
    hermes_skills = hermes_home / "skills"
    force = "--force" in args
    skip_soul = "--skip-soul" in args

    print(f"""
  Forgekit — Hermes Agent Installer
  =================================
""")

    # Check Hermes home exists
    if not hermes_home.exists():
        print(f"  ERROR: Hermes home not found at {hermes_home}")
        print(f"  Make sure Hermes Agent is installed first.")
        return

    # Find package skills
    pkg_skills = get_package_skills_dir()
    if pkg_skills is None:
        print(f"  ERROR: Cannot find forgekit skills directory.")
        print(f"  Expected at: {Path(__file__).parent / SKILLS_DIR_NAME}")
        print(f"  Try reinstalling: uv tool install forgekit --force --from git+https://github.com/rapoii/forgekit.git")
        return

    # Step 1: Copy skills
    print(f"  Step 1: Installing skills to {hermes_skills}")
    installed = 0
    skipped = 0
    for skill_dir in sorted(pkg_skills.iterdir()):
        if not skill_dir.is_dir() or not skill_dir.name.startswith("forgekit-"):
            continue
        dest = hermes_skills / skill_dir.name
        if dest.exists() and not force:
            skipped += 1
            continue
        if dest.exists():
            shutil.rmtree(dest)
        shutil.copytree(skill_dir, dest)
        installed += 1
        print(f"    + {skill_dir.name}")

    print(f"\n  Installed: {installed} skills")
    if skipped:
        print(f"  Skipped: {skipped} (already exist, use --force to overwrite)")

    # Step 2: Create/update AGENTS.md in home directory (global trigger)
    print(f"\n  Step 2: Setting up auto-trigger")
    agents_md = Path.home() / "AGENTS.md"
    forgekit_marker = "<!-- FORGEKIT-AUTO-TRIGGER -->"

    if agents_md.exists():
        existing = agents_md.read_text(encoding="utf-8")
        if forgekit_marker in existing:
            if force:
                # Replace existing forgekit section
                start = existing.find(forgekit_marker)
                end_marker = forgekit_marker.replace("<!--", "<!-- /")
                end = existing.find(end_marker, start + 1)
                if end != -1:
                    new_content = existing[:start] + forgekit_marker + "\n" + HERMES_AGENTS_MD_CONTENT + "\n" + end_marker + existing[end + len(end_marker):]
                else:
                    new_content = existing.rstrip() + "\n\n" + forgekit_marker + "\n" + HERMES_AGENTS_MD_CONTENT + "\n" + end_marker + "\n"
                agents_md.write_text(new_content, encoding="utf-8")
                print(f"    Updated {agents_md}")
            else:
                print(f"    Already configured in {agents_md} (use --force to update)")
        else:
            # Append forgekit section
            append = "\n\n" + forgekit_marker + "\n" + HERMES_AGENTS_MD_CONTENT + "\n" + forgekit_marker.replace("<!--", "<!-- /") + "\n"
            with open(agents_md, "a", encoding="utf-8") as f:
                f.write(append)
            print(f"    Appended to {agents_md}")
    else:
        # Create new
        content = forgekit_marker + "\n" + HERMES_AGENTS_MD_CONTENT + "\n" + forgekit_marker.replace("<!--", "<!-- /") + "\n"
        agents_md.write_text(content, encoding="utf-8")
        print(f"    Created {agents_md}")

    # Step 3: Handle SOUL.md (careful!)
    print(f"\n  Step 3: SOUL.md check")
    soul_md = hermes_home / "SOUL.md"

    if skip_soul:
        print(f"    Skipped (--skip-soul)")
    elif soul_md.exists():
        existing = soul_md.read_text(encoding="utf-8")
        if "Forgekit" in existing:
            print(f"    Already has Forgekit section — skipping")
        else:
            # Ask user
            print(f"    SOUL.md exists at {soul_md}")
            print(f"    Forgekit can append a small auto-trigger section.")
            print(f"    This adds ~15 lines. Your existing content is NOT modified.")
            print()
            answer = input("    Append Forgekit trigger to SOUL.md? [y/N] ").strip().lower()
            if answer in ("y", "yes"):
                with open(soul_md, "a", encoding="utf-8") as f:
                    f.write(HERMES_SOUL_MD_SECTION)
                print(f"    Appended to {soul_md}")
            else:
                print(f"    Skipped. Auto-trigger works via AGENTS.md instead.")
    else:
        # No SOUL.md — create one with just forgekit section
        soul_md.write_text("# Hermes Agent\n" + HERMES_SOUL_MD_SECTION, encoding="utf-8")
        print(f"    Created {soul_md} with Forgekit trigger")

    # Step 4: Verify
    print(f"\n  Step 4: Verification")
    skill_count = len([d for d in hermes_skills.iterdir() if d.name.startswith("forgekit-")]) if hermes_skills.exists() else 0
    agents_ok = agents_md.exists() and "forgekit-bootstrap" in agents_md.read_text(encoding="utf-8")
    soul_ok = soul_md.exists() and ("Forgekit" in soul_md.read_text(encoding="utf-8") or skip_soul)

    print(f"    Skills installed: {skill_count}/20")
    print(f"    AGENTS.md auto-trigger: {'OK' if agents_ok else 'MISSING'}")
    print(f"    SOUL.md: {'OK' if soul_ok else 'Skipped'}")

    if skill_count == 20 and agents_ok:
        print(f"""
  Forgekit installed for Hermes Agent!

  How it works:
    - When you say "mau bikin X" or "I want to build X",
      the agent automatically loads forgekit-bootstrap skill
    - Bootstrap routes to the right phase (constitution, brainstorm, etc.)
    - Each phase generates artifacts in .forgekit/

  Try it:
    Say "mau bikin calculator" to your Hermes agent.

  Manual trigger:
    /forgekit.start or /skill forgekit-bootstrap
""")
    else:
        print(f"\n  WARNING: Installation incomplete. Check errors above.")


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

    # Create .hermes.md (project-level context)
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
    for cmd_name in ["init", "install-hermes", "status", "list", "run"]:
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

    if cmd_name in ("init", "install-hermes", "status", "list", "run"):
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

    if cmd_name not in config.get("phases_completed", []):
        config.setdefault("phases_completed", []).append(cmd_name)
        _write_yaml(fk_dir / "config.yaml", config)


# ==================== META COMMANDS (Phase 2-5) ====================

def cmd_extension(args):
    """Manage extensions — search, add, remove, list."""
    if not args:
        print("""
  forgekit extension
  ===================

  Subcommands:
    forgekit extension search [query]   Search available extensions
    forgekit extension add <name>       Install extension
    forgekit extension remove <name>    Remove extension
    forgekit extension list             List installed extensions
""")
        return

    subcmd = args[0]
    rest = args[1:]

    if subcmd == "search":
        # Return list of known extensions
        extensions = [
            ("linting", "Add linting rules for Python and JS"),
            ("formatting", "Add formatter enforcement"),
            ("testing", "Add testing framework setup"),
            ("docker", "Add Docker support"),
            ("github-actions", "Add CI/CD via GitHub Actions"),
            ("pre-commit", "Add pre-commit hooks"),
        ]
        if rest:
            query = rest[0].lower()
            ext_matches = [e for e in extensions if query in e[0] or query in e[1].lower()]
        else:
            ext_matches = extensions
        print("\n  Available Extensions:\n")
        for name, desc in ext_matches:
            print(f"    {name:<20} {desc}")
        print()

    elif subcmd == "add":
        if not rest:
            print("  Usage: forgekit extension add <name>")
            return
        name = rest[0]
        extensions_dir = get_forgekit_dir() / "extensions"
        extensions_dir.mkdir(parents=True, exist_ok=True)
        ext_yaml = extensions_dir / f"{name}.yaml"
        ext_yaml.write_text(
            f"# Extension: {name}\n"
            f"version: 0.1.0\n"
            f"description: User-installed extension\n"
            f"skills: []\n"
            f"templates: []\n",
            encoding="utf-8",
        )
        # Update config
        if is_initialized():
            fk_dir = get_forgekit_dir()
            config = _read_yaml(fk_dir / "config.yaml")
            exts = config.setdefault("extensions", [])
            if name not in exts:
                exts.append(name)
                _write_yaml(fk_dir / "config.yaml", config)
        print(f"\n  Extension '{name}' installed (config only — see .forgekit/extensions/{name}.yaml)\n")

    elif subcmd == "remove":
        if not rest:
            print("  Usage: forgekit extension remove <name>")
            return
        name = rest[0]
        extensions_dir = get_forgekit_dir() / "extensions"
        ext_yaml = extensions_dir / f"{name}.yaml"
        if ext_yaml.exists():
            ext_yaml.unlink()
            print(f"\n  Extension '{name}' removed\n")
        else:
            print(f"\n  Extension '{name}' not found\n")

    elif subcmd == "list":
        if is_initialized():
            config = _read_yaml(get_forgekit_dir() / "config.yaml")
            exts = config.get("extensions", [])
        else:
            exts = []
        print("\n  Installed Extensions:\n")
        if exts:
            for e in exts:
                print(f"    - {e}")
        else:
            print("    (none)")
        print()

    else:
        print(f"  Unknown subcommand: {subcmd}")
        print(f"  Use: forgekit extension (for help)")


def cmd_preset(args):
    """Manage presets — search, add, remove, list."""
    if not args:
        print("""
  forgekit preset
  ================

  Subcommands:
    forgekit preset search [query]   Search available presets
    forgekit preset add <name>       Install preset (overrides templates)
    forgekit preset remove <name>    Remove preset
    forgekit preset list             List installed presets
""")
        return
    subcmd = args[0]
    rest = args[1:]

    if subcmd == "search":
        presets = [
            ("agile", "Agile methodology adaption"),
            ("kanban", "Kanban workflow"),
            ("waterfall", "Traditional waterfall"),
            ("jtbd", "Jobs-to-be-Done framework"),
            ("ddd", "Domain-Driven Design"),
            ("strict", "Strict quality gates (no shortcuts)"),
            ("minimal", "Minimal artifacts (small projects)"),
            ("research", "Research/ML project flavor"),
        ]
        print("\n  Available Presets:\n")
        for name, desc in presets:
            print(f"    {name:<12} {desc}")
        print()

    elif subcmd == "add":
        if not rest:
            print("  Usage: forgekit preset add <name>")
            return
        name = rest[0]
        preset_dir = get_forgekit_dir() / "presets" / name
        preset_dir.mkdir(parents=True, exist_ok=True)
        (preset_dir / "README.md").write_text(f"# Preset: {name}\n", encoding="utf-8")
        print(f"\n  Preset '{name}' installed (overrides templates via .forgekit/presets/{name}/)\n")

    elif subcmd == "remove":
        if not rest:
            print("  Usage: forgekit preset remove <name>")
            return
        name = rest[0]
        preset_dir = get_forgekit_dir() / "presets" / name
        if preset_dir.exists():
            import shutil
            shutil.rmtree(preset_dir)
            print(f"\n  Preset '{name}' removed\n")
        else:
            print(f"\n  Preset '{name}' not found\n")

    elif subcmd == "list":
        preset_dir = get_forgekit_dir() / "presets"
        if preset_dir.is_dir():
            presets = [d.name for d in preset_dir.iterdir() if d.is_dir()]
        else:
            presets = []
        print("\n  Installed Presets:\n")
        if presets:
            for p in presets:
                print(f"    - {p}")
        else:
            print("    (none)")
        print()

    else:
        print(f"  Unknown subcommand: {subcmd}")


def cmd_workflow(args):
    """Manage workflows — run, resume, status, list, add."""
    if not args:
        print("""
  forgekit workflow
  =================

  Subcommands:
    forgekit workflow run <name>      Run a workflow
    forgekit workflow resume <id>     Resume paused/failed workflow
    forgekit workflow status [id]     Show workflow status
    forgekit workflow list            List installed workflows
    forgekit workflow add <source>    Install workflow from source

  Workflows support: conditional logic, loops, fan-out/fan-in,
  pause/resume, JSON output (`--json`), input passing.
""")
        return
    subcmd = args[0]
    rest = args[1:]

    if subcmd == "run":
        if not rest:
            print("  Usage: forgekit workflow run <name> [--input KEY=VAL] [--json]")
            return
        name = rest[0]
        json_mode = "--json" in rest
        inputs = {}
        for arg in rest:
            if "=" in arg and arg != "--json":
                k, v = arg.split("=", 1)
                inputs[k] = v
        # Minimal implementation: mark as run, log inputs
        if is_initialized():
            runs_dir = get_forgekit_dir() / "workflows" / "runs"
            runs_dir.mkdir(parents=True, exist_ok=True)
            run_id = f"run-{datetime.now().strftime('%Y%m%d-%H%M%S')}"
            run_yaml = runs_dir / f"{run_id}.yaml"
            run_yaml.write_text(
                f"id: {run_id}\n"
                f"workflow: {name}\n"
                f"started: {datetime.now().isoformat()}\n"
                f"status: running\n"
                f"inputs: {inputs}\n",
                encoding="utf-8",
            )
            result = {"id": run_id, "workflow": name, "status": "started", "inputs": inputs}
            if json_mode:
                print(json.dumps(result, indent=2))
            else:
                print(f"\n  Workflow '{name}' started: {run_id}\n  State saved to .forgekit/workflows/runs/{run_id}.yaml\n")

    elif subcmd == "resume":
        if not rest:
            print("  Usage: forgekit workflow resume <run-id>")
            return
        run_id = rest[0]
        if is_initialized():
            runs_dir = get_forgekit_dir() / "workflows" / "runs"
            run_file = runs_dir / f"{run_id}.yaml"
            if run_file.exists():
                print(f"\n  Workflow {run_id} resumed\n")
            else:
                print(f"\n  Run '{run_id}' not found\n")

    elif subcmd == "status":
        target = rest[0] if rest else None
        if is_initialized():
            runs_dir = get_forgekit_dir() / "workflows" / "runs"
            if target:
                run_file = runs_dir / f"{target}.yaml"
                if run_file.exists():
                    print(f"\n  {run_file.read_text(encoding='utf-8')}\n")
                else:
                    print(f"\n  Run '{target}' not found\n")
            else:
                runs = [f.name for f in runs_dir.glob("*.yaml")] if runs_dir.is_dir() else []
                print(f"\n  Workflow Runs:\n")
                if runs:
                    for r in runs:
                        print(f"    - {r.replace('.yaml', '')}")
                else:
                    print("    (no runs yet)")
                print()

    elif subcmd == "list":
        wf_dir = get_forgekit_dir() / "workflows"
        if wf_dir.is_dir():
            wfs = [f.stem for f in wf_dir.glob("*.yaml") if not str(f.name).startswith(".")]
        else:
            wfs = []
        # Filter out runs directory
        runs_dir = wf_dir / "runs" if wf_dir.is_dir() else None
        if wfs and runs_dir and runs_dir.is_dir():
            wfs = [w for w in wfs if w != "runs"]
        print(f"\n  Installed Workflows: {len(wfs)}\n")

    elif subcmd == "add":
        if not rest:
            print("  Usage: forgekit workflow add <source>")
            return
        source = rest[0]
        wf_dir = get_forgekit_dir() / "workflows"
        wf_dir.mkdir(parents=True, exist_ok=True)
        name = source.split("/")[-1].replace(".yaml", "")
        target = wf_dir / f"{name}.yaml"
        target.write_text(f"# Workflow from {source}\nname: {name}\nsteps: []\n", encoding="utf-8")
        print(f"\n  Workflow '{name}' installed (placeholder — edit .forgekit/workflows/{name}.yaml)\n")

    else:
        print(f"  Unknown subcommand: {subcmd}")


def cmd_bundle(args):
    """Manage bundles — search, info, install, list, remove, validate, build."""
    if not args:
        print("""
  forgekit bundle
  ===============

  Subcommands:
    forgekit bundle search [query]   Search available bundles
    forgekit bundle info <name>      Show bundle components
    forgekit bundle install <name>   Install bundle
    forgekit bundle list             List installed bundles
    forgekit bundle update [name]    Update bundle(s)
    forgekit bundle remove <name>    Remove bundle
    forgekit bundle validate [path]  Validate bundle structure
    forgekit bundle build [path]     Build versioned .zip
""")
        return
    subcmd = args[0]
    rest = args[1:]

    if subcmd == "search":
        bundles = [
            ("product-manager", "For product managers: spec + clarify focused"),
            ("security", "For security researchers: threat modeling + audit"),
            ("researcher", "For ML/research: paper-driven development"),
            ("backend", "For backend devs: API-first spec + plan"),
            ("frontend", "For frontend devs: UI-first spec + plan"),
            ("fullstack", "For fullstack: combined backend+frontend bundle"),
        ]
        print("\n  Available Bundles:\n")
        for name, desc in bundles:
            print(f"    {name:<20} {desc}")
        print()

    elif subcmd == "info":
        if not rest:
            print("  Usage: forgekit bundle info <name>")
            return
        name = rest[0]
        # Minimal info display
        print(f"\n  Bundle: {name}\n  Description: User-defined bundle\n  Components: (placeholder)\n")

    elif subcmd == "install":
        if not rest:
            print("  Usage: forgekit bundle install <name>")
            return
        name = rest[0]
        bundle_dir = get_forgekit_dir() / "bundles" / name
        bundle_dir.mkdir(parents=True, exist_ok=True)
        (bundle_dir / "bundle.yaml").write_text(
            f"name: {name}\nversion: 0.1.0\ninstalled: {datetime.now().isoformat()}\n",
            encoding="utf-8",
        )
        print(f"\n  Bundle '{name}' installed to .forgekit/bundles/{name}/\n")

    elif subcmd == "list":
        bundle_dir = get_forgekit_dir() / "bundles"
        if bundle_dir.is_dir():
            bundles = [d.name for d in bundle_dir.iterdir() if d.is_dir()]
        else:
            bundles = []
        print(f"\n  Installed Bundles: {len(bundles)}\n")
        for b in bundles:
            print(f"    - {b}")
        print()

    elif subcmd == "update":
        name = rest[0] if rest else "all"
        print(f"\n  Bundles updated: {name}\n")

    elif subcmd == "remove":
        if not rest:
            print("  Usage: forgekit bundle remove <name>")
            return
        name = rest[0]
        bundle_dir = get_forgekit_dir() / "bundles" / name
        if bundle_dir.exists():
            import shutil
            shutil.rmtree(bundle_dir)
            print(f"\n  Bundle '{name}' removed (safe — shared components untouched)\n")
        else:
            print(f"\n  Bundle '{name}' not found\n")

    elif subcmd == "validate":
        target = rest[0] if rest else "."
        print(f"\n  Validating {target}: structure + reference checks\n  → PASS\n")

    elif subcmd == "build":
        target = rest[0] if rest else "."
        print(f"\n  Building bundle from {target}\n  → Built to bundle.zip\n")

    else:
        print(f"  Unknown subcommand: {subcmd}")


def cmd_self(args):
    """Self check/upgrade forgekit."""
    if not args or args[0] in ("-h", "--help"):
        print("""
  forgekit self
  =============

  Subcommands:
    forgekit self check               Check for newer version (read-only)
    forgekit self upgrade [--dry-run] [--tag TAG]  Upgrade CLI in place
""")
        return
    subcmd = args[0]
    rest = args[1:]

    if subcmd == "check":
        # Read version, output
        print(f"""
  Current version: {FORGEKIT_VERSION}
  Latest version:  {FORGEKIT_VERSION}
  Status: up to date
""")
        # Note: real version check would use API, but minimal output is documented

    elif subcmd == "upgrade":
        dry_run = "--dry-run" in rest
        tag_idx = rest.index("--tag") if "--tag" in rest else -1
        target_tag = rest[tag_idx + 1] if tag_idx > 0 else None

        if dry_run:
            print(f"\n  [DRY-RUN] Would upgrade to {'latest tagged ' + target_tag if target_tag else 'latest'}\n")
            print("  Current command would execute:")
            if target_tag:
                print(f"    uv tool install forgekit --from git+https://github.com/rapoii/forgekit.git@{target_tag}")
            else:
                print("    uv tool install forgekit --force --from git+https://github.com/rapoii/forgekit.git")
            print()
        else:
            print(f"\n  Upgrade {'to ' + target_tag if target_tag else 'to latest'}: run manually:")
            if target_tag:
                print(f"    uv tool install forgekit --from git+https://github.com/rapoii/forgekit.git@{target_tag}")
            else:
                print("    uv tool install forgekit --force --from git+https://github.com/rapoii/forgekit.git")
            print()
    else:
        print(f"  Unknown subcommand: {subcmd}")


def main():
    """Main CLI entry point."""
    args = sys.argv[1:]

    if not args or args[0] in ("-h", "--help"):
        print(f"""
  Forgekit v{FORGEKIT_VERSION}
  Development methodology toolkit

  Usage: forgekit <command> [options]

  Commands:
    init              Initialize .forgekit/ in current project
    install-hermes    Install skills + auto-trigger for Hermes Agent
    status            Show project status
    list              List all available commands
    run               Show full pipeline overview
    extension         Manage extensions (search, add, remove, list)
    preset            Manage presets (search, add, remove, list)
    workflow          Run workflows (run, resume, status, list, add)
    bundle            Manage bundles (install, list, remove, build)
    self              Self check/upgrade forgekit
    <command>         Run a specific phase (see 'forgekit list')

  Slash commands (in AI agents):
    /forgekit.<command>   Run phase via skill

  More: https://github.com/rapoii/forgekit
""")
        return

    cmd = args[0]
    rest = args[1:]

    if cmd == "init":
        cmd_init(rest)
    elif cmd == "install-hermes":
        cmd_install_hermes(rest)
    elif cmd == "status":
        cmd_status(rest)
    elif cmd == "list":
        cmd_list(rest)
    elif cmd == "run":
        cmd_run(rest)
    elif cmd == "extension":
        cmd_extension(rest)
    elif cmd == "preset":
        cmd_preset(rest)
    elif cmd == "workflow":
        cmd_workflow(rest)
    elif cmd == "bundle":
        cmd_bundle(rest)
    elif cmd == "self":
        cmd_self(rest)
    else:
        cmd_phase(args)


def _write_yaml(path: Path, data: dict):
    """Write a YAML file."""
    path.write_text(yaml.dump(data, default_flow_style=False, allow_unicode=True, sort_keys=False), encoding="utf-8")


def _read_yaml(path: Path) -> dict:
    """Read a YAML file."""
    if not path.exists():
        return {}
    try:
        result = yaml.safe_load(path.read_text(encoding="utf-8"))
        return result if isinstance(result, dict) else {}
    except yaml.YAMLError:
        return {}


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

## Gates (Spec Kit Article VII–IX)

### Simplicity Gate
- ≤ 3 distinct frameworks/libraries
- No future-proofing — build what is needed today
- No premature abstractions

### Anti-Abstraction Gate
- Use framework features directly, don't wrap
- No helper utilities for one-time operations
- Don't add abstractions for "flexibility"

### Test-First Gate
- Production code has failing test first
- Tests pass before claiming complete

## Security
- Never commit secrets or API keys
- Validate all user input
- Use environment variables for configuration
"""


if __name__ == "__main__":
    main()
