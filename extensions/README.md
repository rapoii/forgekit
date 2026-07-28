# Extensions

Forgekit supports extensions that add new commands, templates, and workflows.

## Creating an Extension

Create a directory under `extensions/` with:

```
extensions/my-extension/
├── forgekit.yaml       # Extension metadata
├── skills/             # Skill files
│   └── forgekit-my-command/
│       └── SKILL.md
└── templates/          # Template files
    └── my-template.md
```

### forgekit.yaml

```yaml
name: my-extension
version: 0.1.0
description: "What this extension does"
author: Your Name
commands:
  - name: forgekit-my-command
    description: "What this command does"
    phase: planning  # foundation, planning, execution, completion
templates:
  - my-template.md
```

## Installing Extensions

```bash
# From local directory
forgekit extension add ./my-extension

# From GitHub
forgekit extension add https://github.com/user/forgekit-extension

# List installed
forgekit extension list

# Remove
forgekit extension remove my-extension
```

## Community Extensions

Browse community extensions at:
- [Forgekit Extensions](https://github.com/topics/forgekit-extension)

Submit your extension:
1. Create a repo with the structure above
2. Add topic `forgekit-extension`
3. Submit a PR to add to the community list
