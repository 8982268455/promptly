import webbrowser
from http.server import ThreadingHTTPServer
from server.chat import ChatHandler
from utils.network import get_lan_ip

# ------------------ Run HTTP Server ------------------
def run(port=8000):
    """
    Launch a multi-threaded HTTP server for the chat application:
    1. Binds to all network interfaces on the specified port
    2. Uses ChatHandler to process HTTP requests
    3. Prints the LAN URL and opens it in the default web browser
    4. Handles keyboard interrupt to gracefully shut down
    """

    # Handler factory function required by ThreadingHTTPServer
    def handler(*args, **kwargs):
        ChatHandler(*args, **kwargs)

    # Bind server to all interfaces on the specified port
    server_address = ("0.0.0.0", port)
    httpd = ThreadingHTTPServer(server_address, handler)

    # Get LAN IP to display accessible URL
    host_ip = get_lan_ip()
    print(f"Serving tool on http://{host_ip}:{port}")

    # Automatically open default web browser pointing to the server
    webbrowser.open(f"http://{host_ip}:{port}")

    try:
        # Start server loop, handling requests indefinitely
        httpd.serve_forever()
    except KeyboardInterrupt:
        # Gracefully handle Ctrl+C shutdown
        print("\nShutting down server...")
        httpd.server_close()
        print("Server stopped.")