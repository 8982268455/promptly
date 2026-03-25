# Import the socket module to work with network connections
import socket

# ------------------ LAN IP Retrieval ------------------
def get_lan_ip():
    """
    Obtain the local machine's LAN IP address.
    
    This function creates a temporary UDP socket and connects to a public IP (8.8.8.8),
    which allows the OS to assign the most appropriate local IP address for the outgoing
    connection. The IP is then retrieved from the socket.
    
    Returns:
        str: The local LAN IP address. Defaults to "127.0.0.1" if detection fails.
    """
    # Create a UDP socket (does not actually send data)
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    
    try:
        # Attempt to "connect" to a public DNS server (Google) to determine the local IP
        s.connect(("8.8.8.8", 80))
        # Get the IP address assigned to the socket on this machine
        ip = s.getsockname()[0]
    except Exception:
        # If any error occurs (e.g., no network), fall back to localhost
        ip = "127.0.0.1"
    finally:
        # Ensure the socket is closed to free system resources
        s.close()
    
    # Return the detected IP address
    return ip