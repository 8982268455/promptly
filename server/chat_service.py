import uuid
import json
from ai.streaming import call_ai_api_stream
from server.session_manager import (
    create_session,
    delete_session,       
    create_new_session    
)
from server.message_manager import (
    add_message,
    get_history
)

# ------------------ Chat Processing ------------------
def process_chat(session_id, prompt):
    """
    Handle a user's message:
    - Generate a new session ID if none provided
    - Create a session if it doesn't exist
    - Add the user's message to the session
    - Maintains last 5 user-assistant pairs and token limits via add_message
    Returns the session_id used.
    """
    if not session_id:
        session_id = str(uuid.uuid4())  # Create a unique session ID
    create_session(session_id)          # Ensure session exists

    # Add the user's message to the session
    add_message(session_id, {"role": "user", "content": prompt})

    return session_id

# ------------------ Streaming AI Responses ------------------
def stream_ai_response(session_id):
    """
    Stream the AI's response to the client line by line:
    - Retrieves session history
    - Calls AI API in streaming mode
    - Yields partial content as it's received
    - Adds final assistant message to the session
    """
    response_text = ""
    history = get_history(session_id)  # Get all previous messages in session

    for raw in call_ai_api_stream(history):  # Stream API response
        line = raw.decode().strip()
        if not line.startswith("data:"):     # Ignore non-data lines
            continue
        try:
            parsed = json.loads(line[5:].strip())  # Parse JSON from API
            text = parsed["choices"][0]["delta"].get("content")
        except Exception:
            text = None

        if text:
            response_text += text
            yield text  # Yield partial content for real-time streaming

    # Add the completed AI response to the session
    if response_text.strip():
        add_message(session_id, {"role": "assistant", "content": response_text})

# ------------------ New Chat Session ------------------
def new_chat(old_session_id=None):
    """
    Delete an existing session (if provided) and create a new one.
    Returns the new session ID.
    """
    if old_session_id:
        delete_session(old_session_id)  # Remove old session
    new_session_id = create_new_session()  # Create a fresh session
    return new_session_id