import sqlite3, json
from datetime import datetime, timezone
from typing import Optional

DB_PATH = 'video_editor.db'

def store_session(session_id: int, conversation_history : Optional[str]) -> int:
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    if conversation_history is None: conversation_history=json.dumps([])  # Initialize with an empty list
    cursor.execute(
        "INSERT INTO session (session_id, conversation_history) VALUES (?, ?)",
        (session_id, conversation_history,)
    )

    conn.commit()
    conn.close()

    return session_id

def store_context_cache(video_id: str, cache_id: str, ttl: str):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute(
        """
        INSERT INTO context_cache (video_id, cache_id, generated_at, ttl)
        VALUES (?, ?, ?, ?)
        """,
        (video_id, cache_id, datetime.now(timezone.utc), ttl)
    )
    conn.commit()
    conn.close()
    print(f"Cache stored for video {video_id} with cache ID {cache_id} and TTL {ttl}")

