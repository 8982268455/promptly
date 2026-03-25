import json
import urllib.request
import base64
from typing import Dict, List, Generator
from config.config_loader import (
    get_model_name, get_api,
    get_temperature, get_max_out_tokens,
    get_top_p, get_seed,
    get_do_sample, get_auth_type,
    get_username, get_password,
    get_api_key
)

# ---------------- Load configuration values ----------------
MODEL_NAME = get_model_name()        # Name of the GPT model
API = get_api()                      # API endpoint
AUTH_TYPE = get_auth_type()          # Authentication method: 'basic' or 'apikey'
USERNAME = get_username()            # Username for basic auth
PASSWORD = get_password()            # Password for basic auth
API_KEY = get_api_key()              # API key if using 'apikey'
TEMPEARTURE = get_temperature()      # Temperature for generation randomness
MAX_TOKENS = get_max_out_tokens()    # Maximum tokens to generate
TOP_P = get_top_p()                  # Top-p for nucleus sampling
SEED = get_seed()                    # Seed for reproducibility
DO_SAMPLE = get_do_sample()          # Whether to sample outputs
STREAM = True                        # Whether to stream responses

# ---------------- Build API payload ----------------
def build_payload(
    messages: List[Dict[str, str]],
) -> bytes:
    """
    Build and encode the request payload to send to the GPT API.
    Includes model name, messages, generation settings, and streaming option.
    """
    payload = {
        "model": MODEL_NAME,
        "messages": messages,
        "temperature": TEMPEARTURE,
        "max_tokens": MAX_TOKENS,
        "top_p": TOP_P,
        "stream": STREAM,
        "do_sample": DO_SAMPLE,
        "seed": SEED
    }
    return json.dumps(payload).encode("utf-8")  # Convert dict to JSON bytes

# ---------------- Create HTTP request ----------------
def create_request(url: str, payload: bytes) -> urllib.request.Request:
    """
    Create a configured POST request with authentication headers.
    Supports both Basic Auth and API Key methods.
    """
    req = urllib.request.Request(url, data=payload, method="POST")
    req.add_header("Content-Type", "application/json")

    # Add authentication header
    if AUTH_TYPE == "basic":
        credentials = f"{USERNAME}:{PASSWORD}"
        encoded_credentials = base64.b64encode(credentials.encode("utf-8")).decode("utf-8")
        req.add_header("Authorization", f"Basic {encoded_credentials}")
    elif AUTH_TYPE == "apikey":
        req.add_header("Authorization", f"Bearer {API_KEY}")
    else:
        raise ValueError("Unsupported auth_type (use 'basic' or 'apikey')")

    return req

# ---------------- Send HTTP request ----------------
def send_request(req: urllib.request.Request) -> urllib.request.urlopen:
    """
    Send the HTTP request to the API and return the response object.
    Raises RuntimeError if the request fails.
    """
    try:
        return urllib.request.urlopen(req)
    except Exception as e:
        raise RuntimeError(f"API request failed: {e}")

# ---------------- Call API with streaming ----------------
def call_ai_api_stream(
    messages: List[Dict[str, str]]
) -> Generator[bytes, None, None]:
    """
    Send messages to the GPT API and yield streamed response lines.
    Each line is a chunk of bytes from the server.
    """
    payload = build_payload(messages)          # Build request payload
    req = create_request(API, payload)         # Prepare HTTP request
    resp = send_request(req)                   # Send request and get response

    try:
        for line in resp:
            if line.strip():  # Skip empty lines
                yield line
    finally:
        resp.close()  # Ensure response is properly closed