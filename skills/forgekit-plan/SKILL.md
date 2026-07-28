---
name: forgekit-plan
version: 0.1.0
author: Forgekit
description: "When spec and analysis exist and you need a technical implementation plan — create architecture decisions, tech stack, and bite-sized tasks"
tags: [forgekit, planning, architecture, implementation]
related_skills: [forgekit-spec, forgekit-analyze, forgekit-checklist, forgekit-tasks, forgekit-tdd]
---

# Forgekit Plan

Create a technical implementation plan from the spec. Architecture decisions, tech stack choices, file structure, and bite-sized tasks (2–5 min each) with a TDD-first approach.

## When to Use

- After `/forgekit.spec` and `/forgekit.analyze` are complete
- When you're ready to transition from "what to build" to "how to build"
- Before dispatching implementation work to subagents
- After `/forgekit.checklist` passes (or blockers are resolved)

## Steps

1. **Load inputs:**
   - `.forgekit/spec.md` — the requirements
   - `.forgekit/analysis.md` — questions answered, trade-offs decided
   - `.forgekit/constitution.md` — project principles and constraints
   - `.forgekit/checklist.md` — if it exists, verify no blockers remain
   - If any critical file is missing, stop and run the prerequisite skill first.

2. **Make architecture decisions.** For each major component:
   - Choose tech stack (language, framework, libraries) with rationale
   - Define module boundaries and data flow
   - Pick patterns (MVC, event-driven, etc.) and justify
   - Document decisions in a `## Architecture` section

3. **Design file structure.** Create the project layout:
   ```
   project-root/
   ├── src/
   │   ├── module-a/
   │   └── module-b/
   ├── tests/
   │   ├── module-a/
   │   └── module-b/
   ├── .forgekit/
   └── ...
   ```
   Each file should have a single clear responsibility.

4. **Define the task sequence.** Break implementation into bite-sized tasks:
   - Each task: **2–5 minutes** of focused work
   - Each task: **one file or one concern** — not a kitchen sink
   - Each task: **verifiable** — you can confirm it's done
   - Order by dependency (foundations first, then layers on top)

5. **Apply TDD ordering.** For each task, specify:
   - 🔴 Write failing test first (what test, what file)
   - 🟢 Implement minimal code to pass
   - 🔵 Refactor if needed
   - ✅ Commit

6. **Identify risks and mitigations:**
   - Unknowns that could block progress
   - Third-party dependencies with version/availability risk
   - Performance-sensitive areas needing benchmarks

7. **Save** the plan to `.forgekit/plan.md`.

8. **Report** task count, estimated duration, and risk areas to the user.

## Output

`.forgekit/plan.md` containing:
- Architecture decisions with rationale
- File structure
- Ordered task list with TDD notes per task
- Risk register
- Estimated total effort

## Connected Skills

- **← Prerequisite**: `/forgekit.spec` (requirements), `/forgekit.analyze` (decisions)
- **← Optional**: `/forgekit.checklist` (validate spec completeness)
- **→ Next**: `/forgekit.tasks` (detailed task breakdown) or `/forgekit.tdd` (start TDD cycle)
- **→ Parallel**: `/forgekit.constitution` to validate against principles

## Examples

### Creating a plan for a CLI tool
```
User: /forgekit.plan
Agent: Loading spec, analysis, and constitution...

       Architecture Decision: CLI Tool
       ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
       Language: Python 3.11+
       CLI framework: Click
       Testing: pytest + pytest-cli
       Structure: src-layout with click groups

       Task Breakdown (14 tasks, ~45 min total):
       1. 🔴 Project scaffold + pyproject.toml (2 min)
       2. 🔴 CLI entry point with --help (3 min)
       3. 🔴 Config loader: test missing file → implement (3 min)
       4. 🔴 Config loader: test valid YAML → implement (3 min)
       ...

       Risks: None identified.
       Saved to .forgekit/plan.md
       Next: /forgekit.tasks for detailed task specs, or /forgekit.implement to start.
```

## Pitfalls

- **Tasks too large.** If a "task" takes more than 5 minutes, split it. Large tasks defeat the purpose of incremental progress.
- **Skipping TDD ordering.** Even if you don't write tests first, document what the test should be. Future subagents need this context.
- **Architecture without rationale.** Every decision needs a "why" — otherwise reviewers can't evaluate it.
- **Forgetting non-functional requirements.** Performance, security, and accessibility from the spec must appear as tasks.
