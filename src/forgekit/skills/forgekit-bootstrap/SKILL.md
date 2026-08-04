---
name: forgekit-bootstrap
version: 0.1.0
author: Forgekit
description: "When user says 'I want to build X' or 'mau bikin X' — guide them through the SDD pipeline (Lite/Full mode)"
tags: [forgekit, routing, entrypoint]
---

# Forgekit Bootstrap (Router)

This is the entry point for Forgekit. When a user asks you to build something new, DO NOT start writing code immediately. Instead, guide them through the structured Spec-Driven Development (SDD) pipeline.

## 1. Ask for Pipeline Mode

Forgekit supports two modes:
- **Lite Mode (6 steps):** `constitution` → `specify` → `plan` → `implement` → `verify` → `finish`. (Best for small scripts, tools, or familiar projects < 2000 LOC)
- **Full Mode (14 steps):** Complete SDD lifecycle with deep review, verification, and debugging. (Best for production apps)

Ask the user: "Mau pakai mode Lite (6 tahap) atau Full (14 tahap)?"

## 2. Execute Initialization

Once the user chooses, run:
```bash
forgekit init
forgekit mode <lite|full>
forgekit status
```

## 3. Guide to the First Phase

The first phase is always **Constitution**. 
Tell the user what this phase does, then run the command to start it, and load the planning macro-skill:
- Run: `forgekit constitution` (in terminal, if CLI is used)
- Read: `skill_view(name='forgekit-planning')` to see instructions for constitution, brainstorming, and specifying.

## Pipeline Overview (Macro-Skills)

Instead of loading a new skill for every tiny step, Forgekit uses **Macro-Skills**. Load the appropriate skill for your current phase:

1. **`forgekit-planning`**
   - Constitution
   - Brainstorm
   - Clarify
   - Specify
   - Plan

2. **`forgekit-execution`**
   - Tasks
   - Implement
   - TDD
   - Parallel
   - Worktree
   - Debug

3. **`forgekit-quality`**
   - Review
   - Receiving Review
   - Verify
   - Converge
   - Analyze
   - Checklist
   - Complexity

4. **`forgekit-ops`**
   - Finish
   - Publish
   - Config
   - Writing Skills

If a phase needs to be skipped, run:
`forgekit skip <phase> --reason "..."`

Always check `forgekit status` to know your current phase and verdict status!