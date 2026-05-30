#!/bin/bash
PLIST_DEST="$HOME/Library/LaunchAgents/com.xchat.bot.plist"

if [ ! -f "$PLIST_DEST" ]; then
    echo "✗ Service not installed."
    exit 1
fi

launchctl unload "$PLIST_DEST"
echo "✓ Bot stopped."
