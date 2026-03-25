import json
from http.server import BaseHTTPRequestHandler
from server.static_handler import serve_static
from server.chat_service import process_chat, stream_ai_response, new_chat

# ------------------ HTTP Request Handler ------------------
class ChatHandler(BaseHTTPRequestHandler):
    """
    Handles HTTP GET and POST requests for the chat application.
    - Serves static files
    - Provides /new_chat endpoint to create new sessions
    - Provides /chat endpoint to handle user prompts and stream AI responses
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    # ------------------ Serve Static Files ------------------
    def do_GET(self):
        """
        Serve static files for GET requests using serve_static.
        """
        serve_static(self)

    # ------------------ Handle Chat-Related POST Requests ------------------
    def do_POST(self):
        # ---------------- New Chat Endpoint ----------------
        if self.path == "/new_chat":
            try:
                length = int(self.headers.get("Content-Length", 0))
                data = json.loads(self.rfile.read(length).decode()) if length > 0 else {}
            except Exception as e:
                self.send_error(400, f"Invalid request: {e}")
                return

            old_session_id = data.get("session_id")

            # Delete old session (if any) and create a new session
            new_session_id = new_chat(old_session_id)

            # Send JSON response with new session ID
            self.send_response(200)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.send_header("Cache-Control", "no-cache")
            self.end_headers()
            self.wfile.write(json.dumps({"session_id": new_session_id, "status": "ok"}).encode("utf-8"))
            return

        # ---------------- Chat Endpoint ----------------
        if self.path != "/chat":
            self.send_error(404)
            return

        # Parse incoming POST data
        try:
            length = int(self.headers.get("Content-Length", 0))
            data = json.loads(self.rfile.read(length).decode())
        except Exception as e:
            self.send_error(400, f"Invalid request: {e}")
            return

        session_id = data.get("session_id")
        prompt = data.get("prompt", "")

        # Process the user prompt, creating session/messages as needed
        session_id = process_chat(session_id, prompt)

        # Start HTTP response headers
        self.send_response(200)
        self.send_header("Content-Type", "text/plain; charset=utf-8")
        self.send_header("Cache-Control", "no-cache")
        self.end_headers()

        try:
            # Stream AI response chunks to client in real time
            for chunk in stream_ai_response(session_id):
                self.wfile.write(chunk.encode("utf-8"))
                self.wfile.flush()
        except Exception as e:
            # On streaming error, send error message without crashing the server
            error_msg = f"\n[Error streaming AI response: {e}]"
            self.wfile.write(error_msg.encode("utf-8"))
            self.wfile.flush()