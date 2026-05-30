#!/bin/bash
# ─────────────────────────────────────────────
#  Yajin Bot — macOS Setup Script
#  Run once: bash setup.sh
# ─────────────────────────────────────────────

set -e

BOT_DIR="$(cd "$(dirname "$0")" && pwd)"
VENV="$BOT_DIR/venv"
PLIST_NAME="com.xchat.bot"
PLIST_DEST="$HOME/Library/LaunchAgents/$PLIST_NAME.plist"

echo ""
echo "  ✮ XChat Bot Setup"
echo "  ─────────────────"
echo ""

# ── 1. Check Python ──────────────────────────
if ! command -v python3 &>/dev/null; then
    echo "✗ Python 3 not found. Install it from https://www.python.org"
    exit 1
fi
echo "✓ Python3 found: $(python3 --version)"

# ── 2. Create virtualenv ─────────────────────
if [ ! -d "$VENV" ]; then
    echo "→ Creating virtual environment..."
    python3 -m venv "$VENV"
fi
echo "✓ Virtual environment ready"

# ── 3. Install dependencies ──────────────────
echo "→ Installing dependencies..."
"$VENV/bin/pip" install --quiet --upgrade pip
"$VENV/bin/pip" install --quiet -r "$BOT_DIR/requirements.txt"
echo "✓ Dependencies installed"

# ── 4. Check config ──────────────────────────
echo ""
echo "⚠  Before continuing, make sure you have filled in config.py:"
echo "   - X_USERNAME, X_EMAIL, X_PASSWORD"
echo "   - DEEPSEEK_API_KEY"
echo "   - GROUP_ID"
echo ""
read -p "   Have you filled in config.py? [y/N] " confirm
if [[ "$confirm" != "y" && "$confirm" != "Y" ]]; then
    echo "→ Open config.py, fill it in, then run setup.sh again."
    exit 0
fi

# ── 5. First login ───────────────────────────
echo ""
echo "→ Logging into X (Twitter)..."
"$VENV/bin/python" "$BOT_DIR/first_login.py"

if [ ! -f "$BOT_DIR/cookies.json" ]; then
    echo "✗ Login failed — cookies.json not created. Check your credentials."
    exit 1
fi
echo "✓ Session saved"

# ── Clear password from config.py ────────────
echo "→ Clearing password from config.py..."
sed -i '' 's/^X_PASSWORD\s*=.*/X_PASSWORD   = ""  # cleared after login/' "$BOT_DIR/config.py"
sed -i '' 's/^X_EMAIL\s*=.*/X_EMAIL      = ""  # cleared after login/' "$BOT_DIR/config.py"
echo "✓ Password and email cleared from config.py (cookies.json handles auth now)"

# ── 6. Install launchd service ───────────────
echo "→ Setting up auto-start service..."

mkdir -p "$HOME/Library/LaunchAgents"

sed \
    -e "s|VENV_PYTHON_PLACEHOLDER|$VENV/bin/python|g" \
    -e "s|BOT_PATH_PLACEHOLDER|$BOT_DIR/bot.py|g" \
    -e "s|BOT_DIR_PLACEHOLDER|$BOT_DIR|g" \
    "$BOT_DIR/com.xchat.bot.plist.template" > "$PLIST_DEST"

# Unload if already running
launchctl unload "$PLIST_DEST" 2>/dev/null || true
launchctl load "$PLIST_DEST"

echo "✓ Service installed and started"

# ── Done ─────────────────────────────────────
echo ""
echo "  ─────────────────────────────────────"
echo "  ✮ Bot is running."
echo ""
echo "  Useful commands:"
echo "  ./start.sh      — start manually"
echo "  ./stop.sh       — stop"
echo "  tail -f bot.log  — watch live logs"
echo "  ─────────────────────────────────────"
echo ""
