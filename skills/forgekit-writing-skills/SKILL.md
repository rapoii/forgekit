---
name: forgekit-writing-skills
version: 0.1.0
author: Forgekit
description: "When creating new Forgekit skills or modifying existing ones — follow TDD-applied-to-process methodology (RED-GREEN-REFACTOR)"
tags: [forgekit, meta, skills, authoring, tdd, process]
related_skills: [forgekit-tdd, forgekit-brainstorm, forgekit-bootstrap, forgekit-config]
---

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
