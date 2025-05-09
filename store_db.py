import sqlite3, json, os
from datetime import datetime, timezone
from typing import Optional
import logging

# Set up basic configuration
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(message)s'
)

DB_PATH = 'video_editor.db'
if os.path.exists('/app'):  
    DB_PATH = '/app/db_data/video_editor.db' 

def store_session(session_id: str, conversation_history : Optional[str]) -> int:
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    logging.info("Storing session in db")
    if conversation_history is None: conversation_history=json.dumps([])  # Initialize with an empty list
    cursor.execute(
        "INSERT INTO session (session_id, conversation_history) VALUES (?, ?)",
        (session_id, conversation_history,)
    )

    conn.commit()
    conn.close()
    logging.info("Session_id stored successfully")

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

# ...existing code...

def clear_context_cache(video_id: str):
    """
    Clears the cache for a specific video ID from the context_cache table.
    """
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute(
        "DELETE FROM context_cache WHERE video_id = ?",
        (video_id,)
    )
    conn.commit()
    conn.close()
    print(f"Cache cleared for video {video_id}")


def store_user(user_id: str, password: str):
    logging.info("Starts storing user")
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute(
        """
        INSERT INTO users (user_id, password)
        VALUES (?, ?)
        """,
        (user_id, password)
    )
    conn.commit()
    conn.close()
    logging.info("User stored successfully")

def validate_user(user_id: str, password: str) -> bool:
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute(
        """
        SELECT * FROM users WHERE user_id = ?
        """,
        (user_id,)
    )
    result = cursor.fetchone()
    conn.close()

    # check if entry is found and the password amtches then return true elsr return false and if entry if not found then store_user is called
    if result is None:
        logging.info(f"User not found, storing new user")
        store_user(user_id, password)
        return True
    else:
        return result[1] == password

# Example usage:
# clear_context_cache("BigBuckBunny_320x180.mp4")

# store_context_cache("BigBuckBunny_320x180.mp4", "cachedContents/lwyavvattg0b", "180s")