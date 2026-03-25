import os
import mimetypes

# ------------------ Serve Static Files ------------------
def serve_static(handler):
    """
    Serve static files to HTTP clients:
    1. '/' or '/index.html' serves the main HTML page from 'templates/index.html'
    2. Paths starting with '/static/' serve files from the filesystem
    3. Returns 404 for unknown paths or missing files
    """
    
    # Map URL path to file path
    if handler.path in ["/", "/index.html"]:
        filepath = os.path.join("templates", "index.html")
    elif handler.path.startswith("/static/"):
        filepath = handler.path.lstrip("/")  # Remove leading '/' to get local path
    else:
        handler.send_error(404, "Not Found")
        return

    # Determine content type based on file extension
    content_type, _ = mimetypes.guess_type(filepath)
    content_type = content_type or "application/octet-stream"

    try:
        # Read file content
        with open(filepath, "rb") as f:
            content = f.read()

        # Send HTTP response with proper headers
        handler.send_response(200)
        handler.send_header("Content-Type", f"{content_type}; charset=utf-8")
        handler.end_headers()
        handler.wfile.write(content)

    except FileNotFoundError:
        # Return 404 if file does not exist
        handler.send_error(404, f"{filepath} not found")