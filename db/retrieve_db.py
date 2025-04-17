import sqlite3
from typing import Optional

DB_PATH = 'session.db'

def get_session(session_id: int) -> Optional[str]:
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT conversation_history FROM session WHERE session_id = ?", (session_id,))
    result = cursor.fetchone()
    conn.close()
    return result[0] if result else None

def get_cache_by_video(session_id: int) -> Optional[dict]:
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        SELECT cache_id, session_id, generated_at, ttl
        FROM context_cache
        WHERE session_id = ?
    """, (session_id,))
    row = cursor.fetchone()
    conn.close()
    if row:
        return {
            "cache_id": row[0],
            "session_id": row[1],
            "generated_at": row[2],
            "ttl": row[3]
        }
    return None

