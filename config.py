# ─────────────────────────────────────────────
#  BOT CONFIG — fill these in, nothing else to touch
# ─────────────────────────────────────────────

# Your X (Twitter) credentials
X_USERNAME   = "your_username"       # without @
X_EMAIL      = "your@email.com"
X_PASSWORD   = "your_password"

# AI API key — supports DeepSeek (cheap) or OpenAI
# DeepSeek: get key at platform.deepseek.com
# OpenAI:   get key at platform.openai.com
AI_API_KEY   = "sk-..."
AI_BASE_URL  = "https://api.deepseek.com"   # or "https://api.openai.com/v1"
AI_MODEL     = "deepseek-chat"              # or "gpt-4o"

# The group DM ID — from the URL when you open the group chat on X web
# e.g. https://x.com/i/chat/g1234567890  →  GROUP_ID = "g1234567890"
GROUP_ID = "your_group_id"

# Your bot's X username (so she doesn't reply to herself)
BOT_USERNAME = "your_username"       # same as X_USERNAME, no @

# How often to check for new messages (seconds)
POLL_INTERVAL = 15

# How many recent messages to include as context when replying
CONTEXT_WINDOW = 8

# Summary covers last N hours
SUMMARY_HOURS = 24
