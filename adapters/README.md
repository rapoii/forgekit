# Forgekit Platform Adapters

Install scripts for supported AI agent platforms.

## Supported Platforms

| Platform | Install Command |
|---|---|
| Hermes Agent | `forgekit install-hermes` |
| Claude Code | `bash adapters/claude-code/install.sh` |
| OpenCode | `bash adapters/opencode/install.sh` |
| Codex CLI | `bash adapters/codex/install.sh` |
| Cursor | `bash adapters/cursor/install.sh` |

## How It Works

Each adapter:
1. Copies 23 Forgekit skills to the platform's skills directory
2. Creates a platform-specific instructions file
3. Sets up auto-trigger for "mau bikin X" patterns

## Manual Installation

For any platform, you can:
1. Copy `skills/forgekit-*/SKILL.md` to your platform's skills directory
2. Add Forgekit trigger rules to your platform's instructions file
3. Ensure `forgekit-bootstrap` is loaded first for new project triggers
