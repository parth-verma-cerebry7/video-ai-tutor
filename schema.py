import sqlite3

# Connect to the database (or create it if it doesn't exist)
conn = sqlite3.connect('video_editor.db')
cursor = conn.cursor()

# Define the session table schema
create_table_session = """
CREATE TABLE IF NOT EXISTS session (
    session_id INTEGER PRIMARY KEY,
    conversation_history TEXT
);
"""

# Define the context cache table schema
create_table_context_cache = """
CREATE TABLE IF NOT EXISTS context_cache (
    video_id TEXT PRIMARY KEY,
    cache_id TEXT NOT NULL,
    generated_at DATETIME NOT NULL,
    expires_at DATETIME NOT NULL,
    ttl TEXT NOT NULL,
);
"""

# Execute the CREATE TABLE queries
cursor.execute(create_table_session)
cursor.execute(create_table_context_cache)

# Commit the changes and close the connection
conn.commit()
conn.close()
