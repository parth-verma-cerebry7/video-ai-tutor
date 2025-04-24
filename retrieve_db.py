import sqlite3, json
from typing import Optional
import uuid
from store_db import store_session, store_context_cache
from datetime import datetime, timedelta, timezone
import toml
from create_cache import Caching
with open("config.toml", "r") as f:
    config = toml.load(f)

DB_PATH = 'video_editor.db'

def get_session(session_id: int) -> Optional[str]:
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT conversation_history FROM session WHERE session_id = ?", (session_id,))
    result = cursor.fetchone()
    conn.close()

    if result is None:
        store_session(session_id, None)
        return json.dumps([])  # Return empty conversation history if not found
    
    return result[0]

def store_conversation(session_id: int, conversation_history: str):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("UPDATE session SET conversation_history = ? WHERE session_id = ?", (conversation_history, session_id))
    conn.commit()
    conn.close()
    return session_id

def is_cache_expired(expires_at) -> bool:
    print("Type of expires_at:", type(expires_at))
    return datetime.now(timezone.utc) > expires_at

def create_new_cache_for_video(video_file_name: str,  model: str, ttl: str) -> dict:
    
    cache_handler = Caching(video_file_name=video_file_name, model=model, ttl=ttl)

    cache_handler.upload_video_file()
    cache_id = cache_handler.create_cache()

    store_context_cache(video_file_name, cache_id, ttl)
    return cache_id

def get_cache_by_video(video_id: int):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT cache_id, expires_at
        FROM context_cache
        WHERE video_id = ?
    """, (video_id,))

    row = cursor.fetchone()
    conn.close()
    
    # No cache exists
    if not row:
        cache_id = create_new_cache_for_video(video_id, config['model'], config['ttl'])

    # Check if expired
    if is_cache_expired(row[1]):
        create_new_cache_for_video(video_id, config['model'], config['ttl'])

    return cache_id
