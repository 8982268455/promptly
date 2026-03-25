# Import the Tokenizer class from the Hugging Face tokenizers library
from tokenizers import Tokenizer

# Import a helper function that provides the path to the tokenizer file from your config
from config.config_loader import get_tokenizer_path

# Dictionary to cache loaded tokenizers, preventing repeated file reads
tokenizer_cache = {}

# Retrieve the path to the tokenizer file from configuration
TOKENIZER_PATH = get_tokenizer_path()

# ------------------ Tokenizer Loader ------------------
def get_tokenizer():
    """
    Load and cache the tokenizer from file if it hasn't been loaded yet.
    Uses a dictionary cache to ensure that the tokenizer is only loaded once,
    improving performance for repeated calls.
    """
    if "default" not in tokenizer_cache:
        # Load tokenizer from the JSON or binary file path
        tokenizer_cache["default"] = Tokenizer.from_file(TOKENIZER_PATH)
    return tokenizer_cache["default"]  # Return the cached tokenizer

# ------------------ Token Counting ------------------
def count_tokens(messages):
    """
    Count the total number of tokens for a list of messages.
    
    Args:
        messages (list of dict): Each message dict should have a "content" key with text.
    
    Returns:
        int: Total number of tokens across all messages.
    
    This uses the cached tokenizer to encode each message's content into token IDs
    and sums up their lengths.
    """
    tokenizer = get_tokenizer()  # Ensure tokenizer is loaded and cached
    # Sum token counts for each message's content, defaulting to empty string if missing
    return sum(len(tokenizer.encode(m.get("content", "")).ids) for m in messages)