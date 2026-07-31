#!/bin/bash
# Install Forgekit skills for Claude Code
set -e

SKILL_DIR=".claude/skills"
mkdir -p "$SKILL_DIR"

echo "Installing Forgekit skills for Claude Code..."

# Copy skills from package
FORGEKIT_PKG=$(python -c "import importlib.util; spec=importlib.util.find_spec('forgekit'); print(spec.submodule_search_locations[0] if spec else '')" 2>/dev/null || echo "")
if [ -z "$FORGEKIT_PKG" ]; then
    echo "Error: forgekit package not found. Install with: uv tool install forgekit --from git+https://github.com/rapoii/forgekit.git"
    exit 1
fi

cp -r "$FORGEKIT_PKG/skills/forgekit-"* "$SKILL_DIR/" 2>/dev/null || true
echo "Installed $(ls -d $SKILL_DIR/forgekit-* 2>/dev/null | wc -l) skills"

# Create CLAUDE.md if not exists
if [ ! -f ".claude/CLAUDE.md" ]; then
    mkdir -p .claude
    cp "$(dirname "$0")/CLAUDE.md.template" ".claude/CLAUDE.md"
    echo "Created .claude/CLAUDE.md"
fi

echo "Done! Skills installed to $SKILL_DIR/"
