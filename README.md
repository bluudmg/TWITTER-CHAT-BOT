            ...                                                            ...                         
            ...                    .........    ..........                 ...                         
            ...                  ..........................                ...                         
            ...                 .......    .......    .......              ...                         
            ...                 .... .:::   .....:::.   .....              ...                         
            ...                 .... .::     ... ::.    .....              ...                         
         ...........            ....      :. ...     .: .....          ............                    
         ............           ......     ......      .....           .............                   
       ..............            ......:::..........:......           ..............                   
       ..............             ........................           ...............                   
       ..............               ................   ..             ..............                   
         ...........                 ..............  ...               ............                    
           .........                   ...............                    .........                    
           ..........                    ...........                     ..........                    
           .........                        .....                         ........     
           
# XChat Bot

A persistent AI bot that lives inside an X (Twitter) group DM chat.
Reads messages, replies when called by name, summarizes the last 24 hours on demand.

Built with Playwright (browser automation) and any OpenAI-compatible AI API (DeepSeek, OpenAI, etc).

No X API key needed. No third-party X libraries. Just your browser.

---

## What it does

- **Reads the group chat** by connecting to your existing browser — no X API needed
- **Replies when called** — someone says the bot name, she reads recent context and replies in character
- **Batches triggers** — multiple people call her within 12s, she replies once naturally to all of them
- **Summarizes on demand** — type `sumup` and she summarizes the last 24h, naming people by what they said
- **Persistent memory** — SQLite remembers every message and every person. Longer it runs, richer the context.
- **Human-like behavior** — random ignore rate, typing delay, reply cooldown, native X reply threading
- **Prompt injection resistant** — security layer rejects attempts to change her behavior mid-chat

---

## Requirements

- macOS (setup script uses launchd — Linux/Windows users can adapt)
- Python 3.10+
- Brave Browser (or any Chromium-based browser)
- An X account for the bot
- An AI API key — [DeepSeek](https://platform.deepseek.com) (cheap) or [OpenAI](https://platform.openai.com)

---

## Setup

### 1. Fill in `config.py`

```python
X_USERNAME   = "your_bot_username"
X_EMAIL      = "bot@email.com"
X_PASSWORD   = "password"

AI_API_KEY   = "sk-..."
AI_BASE_URL  = "https://api.deepseek.com"   # or https://api.openai.com/v1
AI_MODEL     = "deepseek-chat"              # or gpt-4o

GROUP_ID     = "g1234567890"    # from the URL: x.com/i/chat/g1234567890
BOT_USERNAME = "your_bot_username"
```

### 2. Define your bot's personality

Open `personality.py` and edit `SYSTEM_PROMPT`. This is where you define who your bot is, how they talk, what they care about. The security layer at the bottom is pre-built — don't remove it.

### 3. Install

```bash
cd xchat-bot
bash setup.sh
```

Installs dependencies, logs into X, saves session, registers autostart service.

### 4. Launch Brave with remote debugging

The bot attaches to your existing browser so it can read the encrypted chat:

```bash
pkill -f "Brave Browser"
open -a 'Brave Browser' --args --remote-debugging-port=9222
```

Open the group chat in that Brave window, then:

```bash
venv/bin/python bot.py
```

---

## Chat commands

| What you type | What happens |
|---|---|
| Bot's name anywhere | She reads context and replies in character |
| `sumup` | Summarizes the last 24h, naming people |
| A URL | She refuses in character |
| Prompt injection | She mocks it and stays in character |

---

## Tuning

Timing constants at the top of `bot.py`:

```python
DEBOUNCE_SECONDS = 12    # collect triggers before replying
COOLDOWN_SECONDS = 45    # min time between replies
SUMMARY_COOLDOWN = 3600  # summary once per hour max
```

Ignore rate in `should_ignore_trigger()`:
```python
if random.random() < 0.20:   # 20% chance she ignores
```

---

## Architecture

```
xchat-bot/
├── bot.py          — main loop, browser automation, trigger detection
├── personality.py  — system prompt + summary prompt template
├── memory.py       — SQLite persistent memory
├── config.py       — credentials and settings
├── first_login.py  — one-time X login to generate cookies
├── setup.sh        — one-click macOS install
├── start.sh        — manual start
└── stop.sh         — stop
```

**Reading messages:** Playwright connects to Brave via Chrome DevTools Protocol (CDP). Reads visible DOM text, pairs messages with sender names by font-size heuristics, deduplicates by hash, stores in SQLite.

**Sending messages:** Finds the triggering message in the DOM, hovers to reveal the `...` button, clicks Reply, types the AI response.

**Why CDP instead of X API:** X's group DM API is paywalled/restricted. X also uses end-to-end encryption for newer group chats (XChat) — messages only decrypt inside an authenticated browser session. CDP attaches to that session without re-implementing the encryption.

---

## Notes

- Brave must be open on the group chat tab while the bot runs
- If X changes their DOM, the font-size name detection heuristics may need updating (debug with `debug_names.py`)
- DeepSeek V3 (`deepseek-chat`) recommended — fast, cheap, good instruction following
- Memory DB (`bot_memory.db`) grows indefinitely — trim manually if needed

---

License
This project is licensed under the Viral Public License.
