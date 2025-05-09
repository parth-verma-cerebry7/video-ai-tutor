import sqlite3, json, base64, os
from typing import Optional
import uuid
from store_db import store_session, store_context_cache
from datetime import datetime, timedelta, timezone
import toml
from create_cache import Caching

with open("config.toml", "r") as f:
    config = toml.load(f)

import logging

# Set up basic configuration
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(message)s'
)

DB_PATH = 'video_editor.db'
if os.path.exists('/app'):  
    DB_PATH = '/app/db_data/video_editor.db' 


def get_session(session_id: str) -> Optional[str]:
    logging.info("Fetching information from db")
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT conversation_history FROM session WHERE session_id = ?", (session_id,))
    result = cursor.fetchone()
    conn.close()

    if result is None:
        logging.info("Session_id not found in db")
        store_session(session_id, None)
        return json.dumps([])  # Return empty conversation history if not found
    
    return result[0]

def store_conversation(session_id: int, model_response: str, text_query: str, image_query: Optional[bytes] = None):
    logging.info("Getting the previous conversation")
    conversation = get_session(session_id) 

    logging.info("Converts it into json")
    try:
        conversation = json.loads(conversation)
    except json.JSONDecodeError:
        logging.error("Failed to decode JSON, initializing conversation as empty list")
        conversation = []

    modal = {
        "text_query": text_query,
        "model_response": model_response,
        "image_query": base64.b64encode(image_query).decode('utf-8') if image_query else None
    }

    conversation.append(modal)
    updated_conversation = json.dumps(conversation)

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("UPDATE session SET conversation_history = ? WHERE session_id = ?", (updated_conversation, session_id))
    conn.commit()
    conn.close()
    return session_id

def is_cache_expired(expires_at) -> bool:
    print("Type of expires_at:", type(expires_at))
    return datetime.now(timezone.utc) > expires_at

def create_new_cache_for_video(video_file_name: str,  model: str, ttl: str) -> dict:
    logging.info("Creating new cache for video_id: %s")
    cache_handler = Caching(video_file_name=video_file_name, model=model, ttl=ttl)

    # cache_handler.upload_video_file()
    cache_id = cache_handler.create_cache()

    store_context_cache(video_file_name, cache_id, ttl)
    return cache_id

def get_cache_by_video(video_id: int):
    logging.info("Starts extracting cache for video from db")
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT cache_id
        FROM context_cache
        WHERE video_id = ?
    """, (video_id,))

    row = cursor.fetchone()
    logging.info("Row fetched from db: %s", row)
    conn.close()
    
    # No cache exists
    cache_id = None
    if not row:
        logging.info("No cache exists for video_id")
        cache_id = create_new_cache_for_video(video_id, config['model'], config['ttl'])

    # Check if expired
    # if is_cache_expired(row[1]):
    #     logging.info("Cache expired for video_id")
    #     create_new_cache_for_video(video_id, config['model'], config['ttl'])

    return cache_id
