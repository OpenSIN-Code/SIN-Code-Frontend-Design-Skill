# SIN-Code-Frontend-Design-Skill — Installation

*One install, eight MCP tools, six bash scripts. Works on any Mac or Linux with Python 3.10+.*

---

## 1. Prerequisites

### 1.1 Python 3.10+

```bash
python3 --version
# ✅ "Python 3.10.x" or higher
```

### 1.2 (Optional) v0-pool running

The skill falls back to built-in templates if the v0-pool is offline, but
component generation with `use_v0=true` requires it:

```bash
curl -s http://localhost:27401/v1/models | head -5
# ✅ Lists v0-1.5-lg, v0-1.5-md
# ❌ → see SINator-v0 README
```

---

## 2. Clone the repository

```bash
cd ~/dev
git clone https://github.com/OpenSIN-Code/SIN-Code-Frontend-Design-Skill.git
cd SIN-Code-Frontend-Design-Skill
```

---

## 3. Install the skill

```bash
bash install.sh
```

**What happens:**
1. Installs the Python package via `pip install -e .` (or just `PYTHONPATH=src`).
2. Copies the bash scripts to `~/.config/opencode/skills/frontend-design/scripts/`.
3. Copies `SKILL.md` to `~/.config/opencode/skills/frontend-design/`.

---

## 4. Verify the install

```bash
# 4.1 — Design system loads
PYTHONPATH=src python3 -c "
from sin_frontend_design import DesignSystem
ds = DesignSystem()
print('OK', len(ds.philosophy()), 'philosophy items')
"

# 4.2 — Tests pass
PYTHONPATH=src python3 -m pytest tests/ -q
# ✅ 202 passed

# 4.3 — Scripts work
./scripts/design-load.sh --json | head -5
./scripts/design-component.sh button --framework=react | head -10
./scripts/design-page.sh landing --framework=html | head -10
```

---

## 5. Usage from opencode

The skill auto-registers in opencode via the SKILL.md frontmatter. The 8 MCP
tools become available after the FastMCP server is started:

```bash
# Start the MCP server (foreground)
python3 -m sin_frontend_design.mcp_server

# Or via the script
~/.config/opencode/skills/frontend-design/scripts/design-load.sh
```

---

## 6. Usage from the shell

```bash
# 6.1 — Load the design system
./scripts/design-load.sh

# 6.2 — Generate a button
./scripts/design-component.sh button --framework=react --variant=primary

# 6.3 — Scaffold a pricing page
./scripts/design-page.sh pricing --framework=html

# 6.4 — Review your UI
./scripts/design-review.sh path/to/page.html

# 6.5 — Extract tokens
./scripts/design-tokens.sh tokens.css

# 6.6 — WCAG 2.2 AA check
./scripts/design-a11y.sh page.html
```

---

## 7. Uninstall

```bash
rm -rf ~/.config/opencode/skills/frontend-design
pip uninstall sin-frontend-design
```

---

*Built by OpenSIN AI — Anthropic-compatible design system for agents.*
