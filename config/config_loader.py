import yaml
import os

# Cache for loaded configuration to avoid reading the YAML file multiple times
_config_cache = None

def _load_config(path: str = "config/config.yaml") -> dict:
    """Load YAML config from file once and cache it for future use."""
    global _config_cache
    if _config_cache is None:
        if not os.path.exists(path):
            raise FileNotFoundError(f"Config file not found: {path}")
        with open(path, "r") as f:
            _config_cache = yaml.safe_load(f)  # Parse YAML into a Python dictionary
    return _config_cache

# ---------------- Model Config ----------------
def get_model_name() -> str:
    """Return the name of the model from config."""
    return _load_config()["model"].get("name", "")

def get_api() -> str:
    """Return the API endpoint for the model from config."""
    return _load_config()["model"].get("api", "")

# ---------------- Auth Config ----------------
def get_auth_type() -> str:
    """Return the authentication type ('basic' or 'apikey')."""
    return _load_config()["model"].get("auth_type", "apikey")

def get_username() -> str:
    """Return username for basic authentication."""
    return _load_config()["model"].get("username", "")

def get_password() -> str:
    """Return password for basic authentication."""
    return _load_config()["model"].get("password", "")

def get_api_key() -> str:
    """Return API key if using 'apikey' auth_type."""
    return _load_config()["model"].get("api_key", "")

# ---------------- Generation Config ----------------
def get_temperature() -> float:
    """Return generation temperature (randomness control)."""
    return _load_config()["generation"].get("temperature", 0)

def get_context_length() -> int:
    """Return maximum context length in tokens."""
    return _load_config()["generation"].get("context_length", 130000)

def get_max_out_tokens() -> int:
    """Return maximum number of tokens the model can output."""
    return _load_config()["generation"].get("max_out_tokens", 64000)

def get_max_message_pairs() -> int:
    """Return maximum number of message pairs to retain in context."""
    return _load_config()["generation"].get("max_message_pairs", 5)

def get_top_p() -> float:
    """Return top-p (nucleus sampling) value."""
    return _load_config()["generation"].get("top_p", 1)

def get_do_sample() -> bool:
    """Return whether to sample outputs randomly or pick highest probability."""
    return _load_config()["generation"].get("do_sample", False)

def get_seed() -> int:
    """Return seed value for reproducibility."""
    return _load_config()["generation"].get("seed", 42)

# ---------------- System Config ----------------
def get_system_prompt() -> str:
    """Return the system prompt used to guide the model."""
    return _load_config()["system"].get("prompt", "You are senior software engineer.")

# ---------------- Database Config ----------------
def get_database_file() -> str:
    """Return path to the database file for session storage."""
    return _load_config()["database"].get("file", "data/sessions.db")

# ---------------- Tokenizer Config ----------------
def get_tokenizer_path() -> str:
    """Return path to the tokenizer JSON file."""
    return _load_config()["tokenizer"].get("path", "tokenizers/tokenizer.json")