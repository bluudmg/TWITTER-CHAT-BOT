#!/bin/bash
# Manual start (launchd already handles auto-start, use this to restart manually)

BOT_DIR="$(cd "$(dirname "$0")" && pwd)"
PLIST_DEST="$HOME/Library/LaunchAgents/com.xchat.bot.plist"

if [ ! -f "$PLIST_DEST" ]; then
    echo "✗ Not set up yet. Run: bash setup.sh"
    exit 1
fi

launchctl unload "$PLIST_DEST" 2>/dev/null || true
launchctl load "$PLIST_DEST"
echo "✓ Bot started. Watch logs: tail -f $BOT_DIR/yajin.log"
