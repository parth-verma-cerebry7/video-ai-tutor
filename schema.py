import sqlite3
import os

if os.path.exists("/app"):  # running inside Docker
    DB_PATH = "/app/db_data/video_editor.db"
else:  # local environment
    DB_PATH = os.path.join(os.getcwd(), "db_data", "video_editor.db")

# Connect to the database (or create it if it doesn't exist)
conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

# Define the session table schema
create_table_session = """
CREATE TABLE IF NOT EXISTS session (
    session_id TEXT PRIMARY KEY,
    conversation_history TEXT
);
"""

# Define the context cache table schema
create_table_context_cache = """
CREATE TABLE IF NOT EXISTS context_cache (
    video_id TEXT PRIMARY KEY,
    cache_id TEXT NOT NULL,
    generated_at DATETIME NOT NULL,
    ttl TEXT NOT NULL
);
"""

create_table_store_users='''
CREATE TABLE IF NOT EXISTS users (
    user_id TEXT PRIMARY KEY,
    password TEXT NOT NULL
);
'''

# Execute the CREATE TABLE queries
cursor.execute(create_table_session)
cursor.execute(create_table_context_cache)
cursor.execute(create_table_store_users)

# Commit the changes and close the connection
conn.commit()
conn.close()
