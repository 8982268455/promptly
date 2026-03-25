import uuid
from db.connection import get_connection
from config.config_loader import get_system_prompt
from server.message_manager import get_history

# Default system prompt for new sessions
SYSTEM_PROMPT = get_system_prompt()

# ------------------ Create or Retrieve Session ------------------
def create_session(session_id):
    """
    Ensure a session exists in the database:
    1. If the session doesn't exist, insert it into sessions table
    2. Add initial system message using SYSTEM_PROMPT
    3. Update token count for the session
    4. Return the full session history
    """
    conn = get_connection()
    cursor = conn.cursor()

    # Check if session already exists
    cursor.execute("SELECT session_id FROM sessions WHERE session_id=?", (session_id,))
    if not cursor.fetchone():
        # Insert new session
        cursor.execute("INSERT INTO sessions (session_id) VALUES (?)", (session_id,))
        
        # Add system message to messages table
        cursor.execute(
            "INSERT INTO messages (session_id, role, content) VALUES (?, ?, ?)",
            (session_id, "system", SYSTEM_PROMPT)
        )
        conn.commit()

        # Update token count for session based on system message
        from tokenizer.tokenizer_utils import count_tokens
        cursor.execute(
            "UPDATE sessions SET token_count=? WHERE session_id=?", 
            (count_tokens([{"role":"system","content":SYSTEM_PROMPT}]), session_id)
        )

    conn.close()
    # Return the current history for the session
    return get_history(session_id)

# ------------------ Delete Session ------------------
def delete_session(session_id):
    """
    Remove a session completely:
    1. Delete all messages associated with the session
    2. Delete the session entry itself
    """
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM messages WHERE session_id=?", (session_id,))
    cursor.execute("DELETE FROM sessions WHERE session_id=?", (session_id,))
    conn.commit()
    conn.close()

# ------------------ Create New Session ------------------
def create_new_session():
    """
    Generate a new unique session ID and create a corresponding session.
    Returns the new session ID.
    """
    new_session_id = str(uuid.uuid4())
    create_session(new_session_id)
    return new_session_id