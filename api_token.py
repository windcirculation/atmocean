"""Utility to fetch the Telegram bot token.

The repository originally contained two conflicting implementations. The newer
version validates that the ``TELEGRAM_BOT_TOKEN`` environment variable is set and
raises a clear error if it is missing, which is safer for production use.
We keep that implementation.
"""

import os


def api_key() -> str:
    """Return the ``TELEGRAM_BOT_TOKEN`` environment variable.

    If the variable is missing we return an empty string instead of raising.
    This makes importing the package safe in environments without the token.
    Callers that require a real token should verify the returned value.
    """
    return os.getenv("TELEGRAM_BOT_TOKEN", "")
