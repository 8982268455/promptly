import sqlite3
import os
from config.config_loader import get_database_file, get_system_prompt

# ---------------- Load configuration ----------------
DB_FILE = get_database_file()       # Path to SQLite database file
SYSTEM_PROMPT = get_system_prompt() # Default system prompt for new sessions

# ---------------- Database Connection ----------------
def get_connection():
    """
    Get a SQLite connection. Automatically creates the DB file and tables if missing.
    Returns a connection object ready for queries.
    """
    # Ensure the parent folder exists before creating the DB file
    os.makedirs(os.path.dirname(DB_FILE), exist_ok=True)

    # Connect to SQLite database with multi-thread support
    conn = sqlite3.connect(DB_FILE, check_same_thread=False, timeout=10)

    # Enable Write-Ahead Logging for better concurrency
    conn.execute("PRAGMA journal_mode=WAL;")

    # Initialize tables if they don't exist
    init_db(conn)

    return conn

# ---------------- Initialize Database Tables ----------------
def init_db(conn):
    """
    Create required tables if they don't exist:
    - sessions: stores session metadata (ID, system prompt, token count)
    - messages: stores individual chat messages per session
    """
    cursor = conn.cursor()

    # Sessions table: stores metadata for each chat session
    cursor.execute(f"""
        CREATE TABLE IF NOT EXISTS sessions (
            session_id TEXT PRIMARY KEY,
            system_prompt TEXT DEFAULT '{SYSTEM_PROMPT}',
            token_count INTEGER DEFAULT 0
        )
    """)

    # Messages table: stores chat messages for each session
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            session_id TEXT,
            role TEXT,
            content TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)

    conn.commit()  # Save changes to the database