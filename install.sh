#!/usr/bin/env bash
# SIN-Code-Frontend-Design-Skill Installer
# Installs the design-system skill into ~/.config/opencode/skills/frontend-design/
set -euo pipefail

SKILL_NAME="frontend-design"
OPENCODE_SKILLS_DIR="${OPENCODE_SKILLS_DIR:-$HOME/.config/opencode/skills/$SKILL_NAME}"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

echo "╔══════════════════════════════════════════════════╗"
echo "║  SIN-Code-Frontend-Design-Skill Installer        ║"
echo "╚══════════════════════════════════════════════════╝"
echo ""

# Check Python
if ! command -v python3 &> /dev/null; then
    echo "❌ python3 not found. Please install Python 3.10+ first."
    exit 1
fi
PY_VERSION=$(python3 -c "import sys; print(f'{sys.version_info.major}.{sys.version_info.minor}')")
echo "✅ Python $PY_VERSION detected"

# Check pip
if ! command -v pip3 &> /dev/null && ! python3 -m pip --version &> /dev/null; then
    echo "❌ pip3 not found. Please install pip."
    exit 1
fi
echo "✅ pip available"

# Install Python package (editable, lightweight — no v0 SDK needed)
if [ -f "$SCRIPT_DIR/requirements.txt" ]; then
    python3 -m pip install --quiet --user -r "$SCRIPT_DIR/requirements.txt" 2>/dev/null || \
        python3 -m pip install --quiet -r "$SCRIPT_DIR/requirements.txt" 2>/dev/null || \
        echo "  (continuing — some optional packages may not be installed)"
    echo "✅ Python requirements installed"
fi

# Create skill dir
mkdir -p "$OPENCODE_SKILLS_DIR/scripts"
echo "✅ Skill directory: $OPENCODE_SKILLS_DIR"

# Copy SKILL.md
if [ -f "$SCRIPT_DIR/SKILL.md" ]; then
    cp "$SCRIPT_DIR/SKILL.md" "$OPENCODE_SKILLS_DIR/"
    echo "✅ SKILL.md installed"
fi

# Copy scripts
if [ -d "$SCRIPT_DIR/scripts" ]; then
    cp "$SCRIPT_DIR/scripts/"*.sh "$OPENCODE_SKILLS_DIR/scripts/"
    chmod +x "$OPENCODE_SKILLS_DIR/scripts/"*.sh
    echo "✅ Scripts installed: $OPENCODE_SKILLS_DIR/scripts/"
fi

# Copy src/ for PYTHONPATH usage
if [ -d "$SCRIPT_DIR/src" ]; then
    cp -r "$SCRIPT_DIR/src" "$OPENCODE_SKILLS_DIR/"
    echo "✅ Source code installed"
fi

echo ""
echo "╔══════════════════════════════════════════════════╗"
echo "║  ✅  Installation abgeschlossen!                  ║"
echo "╚══════════════════════════════════════════════════╝"
echo ""
echo "Test it:"
echo "  PYTHONPATH=$OPENCODE_SKILLS_DIR/src python3 -c \"from sin_frontend_design import DesignSystem; print(DesignSystem().philosophy()[:2])\""
echo ""
echo "Use the bash scripts:"
echo "  $OPENCODE_SKILLS_DIR/scripts/design-load.sh"
echo "  $OPENCODE_SKILLS_DIR/scripts/design-component.sh button --framework=react"
echo "  $OPENCODE_SKILLS_DIR/scripts/design-page.sh landing"
echo "  $OPENCODE_SKILLS_DIR/scripts/design-a11y.sh page.html"
