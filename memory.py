#!/usr/bin/env python3
"""
Yajin Memory — persistent SQLite storage
Remembers every message, every person, every topic, forever.
"""

import sqlite3
from datetime import datetime, timezone
from pathlib import Path

DB_PATH = Path(__file__).parent / "yajin_memory.db"


def get_conn() -> sqlite3.Connection:
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db() -> None:
    """Create tables if they don't exist yet."""
    with get_conn() as conn:
        conn.executescript("""
            -- Every message ever seen
            CREATE TABLE IF NOT EXISTS messages (
                id          TEXT PRIMARY KEY,
                username    TEXT NOT NULL,
                text        TEXT NOT NULL,
                timestamp   TEXT NOT NULL
            );

            -- Per-person notes Yajin builds up over time
            CREATE TABLE IF NOT EXISTS people (
                username        TEXT PRIMARY KEY,
                first_seen      TEXT NOT NULL,
                last_seen       TEXT NOT NULL,
                message_count   INTEGER DEFAULT 0,
                topics          TEXT DEFAULT '',   -- comma-separated recurring topics
                notes           TEXT DEFAULT ''    -- free-form observations
            );

            -- Recurring themes tracked across the whole chat
            CREATE TABLE IF NOT EXISTS themes (
                topic       TEXT PRIMARY KEY,
                count       INTEGER DEFAULT 1,
                last_seen   TEXT NOT NULL
            );
        """)


def save_message(msg_id: str, username: str, text: str) -> None:
    now = datetime.now(timezone.utc).isoformat()
    with get_conn() as conn:
        # Save message
        conn.execute(
            "INSERT OR IGNORE INTO messages (id, username, text, timestamp) VALUES (?, ?, ?, ?)",
            (msg_id, username, text, now)
        )
        # Upsert person record
        conn.execute("""
            INSERT INTO people (username, first_seen, last_seen, message_count)
            VALUES (?, ?, ?, 1)
            ON CONFLICT(username) DO UPDATE SET
                last_seen     = excluded.last_seen,
                message_count = message_count + 1
        """, (username, now, now))


def get_person_history(username: str, limit: int = 20) -> list[dict]:
    """Return last N messages from a specific person."""
    with get_conn() as conn:
        rows = conn.execute("""
            SELECT username, text, timestamp
            FROM messages
            WHERE username = ?
            ORDER BY timestamp DESC
            LIMIT ?
        """, (username, limit)).fetchall()
    return [dict(r) for r in reversed(rows)]


def get_person_profile(username: str) -> dict | None:
    """Return everything known about a person."""
    with get_conn() as conn:
        row = conn.execute(
            "SELECT * FROM people WHERE username = ?", (username,)
        ).fetchone()
    return dict(row) if row else None


def get_frequent_people(limit: int = 10) -> list[dict]:
    """Most active people in the chat."""
    with get_conn() as conn:
        rows = conn.execute("""
            SELECT username, message_count, last_seen
            FROM people
            ORDER BY message_count DESC
            LIMIT ?
        """, (limit,)).fetchall()
    return [dict(r) for r in rows]


def get_recent_messages_from_chat(limit: int = 50) -> list[dict]:
    """Last N messages from anyone, for context."""
    with get_conn() as conn:
        rows = conn.execute("""
            SELECT username, text, timestamp
            FROM messages
            ORDER BY timestamp DESC
            LIMIT ?
        """, (limit,)).fetchall()
    return [dict(r) for r in reversed(rows)]


def update_person_notes(username: str, notes: str) -> None:
    """Let Yajin store freeform observations about someone."""
    with get_conn() as conn:
        conn.execute(
            "UPDATE people SET notes = ? WHERE username = ?",
            (notes, username)
        )


def build_person_context(username: str) -> str:
    """
    Build a rich context string about a person to inject before replying.
    Includes their history, how active they are, any stored notes.
    """
    profile = get_person_profile(username)
    history = get_person_history(username, limit=15)

    if not profile:
        return f"{username} is new, you've never interacted before."

    lines = []

    lines.append(f"What you know about {username}:")
    lines.append(f"  - {profile['message_count']} messages sent since you've known them")
    lines.append(f"  - First seen: {profile['first_seen'][:10]}")
    lines.append(f"  - Last seen: {profile['last_seen'][:10]}")

    if profile.get("notes"):
        lines.append(f"  - Your notes on them: {profile['notes']}")

    if history:
        lines.append(f"\nTheir recent messages (last {len(history)}):")
        for m in history[-10:]:  # show max 10 in prompt to save tokens
            lines.append(f"  [{m['timestamp'][:10]}] {m['text']}")

    return "\n".join(lines)
