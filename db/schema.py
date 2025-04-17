import sqlite3

# Connect to the database (or create it if it doesn't exist)
conn = sqlite3.connect('session.db')
cursor = conn.cursor()

# Define the session table schema
create_table_session = """
CREATE TABLE IF NOT EXISTS session (
    session_id INTEGER PRIMARY KEY AUTOINCREMENT,
    conversation_history TEXT
);
"""

# Define the context cache table schema
create_table_context_cache = """
CREATE TABLE IF NOT EXISTS context_cache (
    cache_id TEXT PRIMARY KEY,
    session_id INTEGER NOT NULL,
    generated_at DATETIME NOT NULL,
    ttl TEXT NOT NULL,
    FOREIGN KEY (session_id) REFERENCES session(session_id)
);
"""

# Execute the CREATE TABLE queries
cursor.execute(create_table_session)
cursor.execute(create_table_context_cache)

# Commit the changes and close the connection
conn.commit()
conn.close()
