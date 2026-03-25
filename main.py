# Import the `run` function from the server module, which starts the application server
from server.run_server import run

# ------------------ Script Entry Point ------------------
if __name__ == "__main__":
    """
    This block ensures that the server starts only when this script is executed directly.
    If the module is imported elsewhere, the server does not start automatically.
    """
    run()  # Call the main server function to start listening for requests