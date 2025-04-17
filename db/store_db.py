import sqlite3
from datetime import datetime

DB_PATH = 'session.db'

def store_session(conversation_history: str) -> int:
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO session (conversation_history) VALUES (?)",
        (conversation_history,)
    )
    session_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return session_id

def store_context_cache(cache_id: str, session_id: int, ttl: str):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute(
        """
        INSERT INTO context_cache (cache_id, session_id, generated_at, ttl)
        VALUES (?, ?, ?, ?)
        """,
        (cache_id, session_id, datetime.utcnow(), ttl)
    )
    conn.commit()
    conn.close()
