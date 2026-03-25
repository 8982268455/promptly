from db.connection import get_connection
from tokenizer.tokenizer_utils import count_tokens
from config.config_loader import get_context_length, get_max_out_tokens, get_max_message_pairs

# Safe margin: reserve space in context for model output to prevent overflow
SAFE_MARGIN = get_context_length() - get_max_out_tokens()

# Maximum number of user-assistant message pairs to keep in session
MAX_MESSAGE_PAIRS = get_max_message_pairs()

# ------------------ Retrieve chat history ------------------
def get_history(session_id):
    """
    Fetch all messages for a session in chronological order.
    Returns a list of dictionaries: [{'role': 'user/assistant', 'content': message}, ...]
    """
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT role, content FROM messages WHERE session_id = ? ORDER BY id ASC",
        (session_id,)
    )
    rows = cursor.fetchall()
    conn.close()
    return [{"role": r[0], "content": r[1]} for r in rows]

# ------------------ Add a new message and prune history ------------------
def add_message(session_id, message):
    """
    Add a new user or assistant message to the database and maintain limits:
    1. Enforces MAX_MESSAGE_PAIRS (keeps only the latest N user-assistant pairs)
    2. Token-based pruning to ensure total tokens <= SAFE_MARGIN
    """
    conn = get_connection()
    cursor = conn.cursor()
    
    # Insert new message into messages table
    cursor.execute(
        "INSERT INTO messages (session_id, role, content) VALUES (?, ?, ?)",
        (session_id, message["role"], message["content"])
    )
    conn.commit()

    # ------------------ Enforce max message pairs ------------------
    cursor.execute(
        "SELECT id FROM messages WHERE session_id=? AND role='user' ORDER BY id ASC",
        (session_id,)
    )
    user_ids = [row[0] for row in cursor.fetchall()]

    # Delete oldest user-assistant pairs if exceeding MAX_MESSAGE_PAIRS
    while len(user_ids) > MAX_MESSAGE_PAIRS:
        oldest_user_id = user_ids.pop(0)
        cursor.execute(
            "DELETE FROM messages WHERE session_id=? AND id IN (?, ?)",
            (session_id, oldest_user_id, oldest_user_id + 1)
        )

    # ------------------ Token-based pruning ------------------
    cursor.execute(
        "SELECT role, content, id FROM messages WHERE session_id=? ORDER BY id ASC",
        (session_id,)
    )
    messages = [{"role": r[0], "content": r[1], "id": r[2]} for r in cursor.fetchall()]

    token_count = count_tokens(messages)

    # Remove oldest user-assistant messages until total tokens fit within SAFE_MARGIN
    while token_count > SAFE_MARGIN:
        oldest_user_index = next((i for i, m in enumerate(messages) if m["role"] == "user"), None)
        if oldest_user_index is None:
            break

        oldest_user = messages[oldest_user_index]
        oldest_assistant = messages[oldest_user_index + 1] if oldest_user_index + 1 < len(messages) else None

        delete_ids = [oldest_user["id"]]
        if oldest_assistant:
            delete_ids.append(oldest_assistant["id"])

        # Delete the identified oldest user-assistant pair from DB
        cursor.execute(
            f"DELETE FROM messages WHERE session_id=? AND id IN ({','.join(['?']*len(delete_ids))})",
            [session_id, *delete_ids]
        )

        # Remove deleted messages from local list for next iteration
        messages = [m for m in messages if m["id"] not in delete_ids]
        token_count = count_tokens(messages)

    # Update token count in sessions table
    cursor.execute(
        "UPDATE sessions SET token_count=? WHERE session_id=?",
        (token_count, session_id)
    )
    conn.commit()
    conn.close()

# ------------------ Replace session history ------------------
def update_history(session_id, new_history):
    """
    Replace all messages in a session with new_history:
    1. Deletes existing messages for the session
    2. Inserts new messages from new_history
    3. Updates token count for session
    """
    conn = get_connection()
    cursor = conn.cursor()
    
    # Delete all old messages
    cursor.execute("DELETE FROM messages WHERE session_id=?", (session_id,))
    
    # Insert all new messages
    for m in new_history:
        cursor.execute(
            "INSERT INTO messages (session_id, role, content) VALUES (?, ?, ?)",
            (session_id, m["role"], m["content"])
        )
    
    # Compute new token count
    from tokenizer.tokenizer_utils import count_tokens
    token_count = count_tokens(new_history)
    
    # Update session token count
    cursor.execute("UPDATE sessions SET token_count=? WHERE session_id=?", (token_count, session_id))
    conn.commit()
    conn.close()