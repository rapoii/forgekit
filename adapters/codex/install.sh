#!/bin/bash
# Install Forgekit skills for Codex CLI
set -e

SKILL_DIR=".codex/skills"
mkdir -p "$SKILL_DIR"

echo "Installing Forgekit skills for Codex CLI..."

FORGEKIT_PKG=$(python -c "import importlib.util; spec=importlib.util.find_spec('forgekit'); print(spec.submodule_search_locations[0] if spec else '')" 2>/dev/null || echo "")
if [ -z "$FORGEKIT_PKG" ]; then
    echo "Error: forgekit package not found."
    exit 1
fi

cp -r "$FORGEKIT_PKG/skills/forgekit-"* "$SKILL_DIR/" 2>/dev/null || true
echo "Installed $(ls -d $SKILL_DIR/forgekit-* 2>/dev/null | wc -l) skills"

if [ ! -f ".codex/instructions.md" ]; then
    mkdir -p .codex
    echo "# Forgekit Instructions\n\nLoad forgekit-bootstrap when user says 'mau bikin X'" > ".codex/instructions.md"
    echo "Created .codex/instructions.md"
fi

echo "Done! Skills installed to $SKILL_DIR/"
