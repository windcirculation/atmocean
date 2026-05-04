"""Telegram bot helper functions.

Provides a fallback implementation for the ``requests`` library using the
standard library ``urllib`` when ``requests`` is unavailable.
"""

import json
import urllib.parse
import urllib.request

try:
    import requests  # type: ignore
except ImportError:  # pragma: no cover
    class _SimpleResponse:
        def __init__(self, url: str, data: bytes, status: int):
            self._url = url
            self._data = data
            self.status_code = status

        def raise_for_status(self) -> None:
            if not (200 <= self.status_code < 300):
                raise urllib.error.HTTPError(
                    self._url,
                    self.status_code,
                    f"HTTP error {self.status_code}",
                    hdrs=None,
                    fp=None,
                )

        @property
        def text(self) -> str:
            return self._data.decode("utf-8", errors="replace")

        def json(self):  # type: ignore
            return json.loads(self.text)

    class requests:  # type: ignore
        @staticmethod
        def get(url: str, params: dict | None = None):
            if params:
                url = f"{url}?{urllib.parse.urlencode(params)}"
            try:
                with urllib.request.urlopen(url) as resp:
                    data = resp.read()
                    status = resp.getcode()
            except urllib.error.HTTPError as e:
                data = e.read()
                status = e.code
            return _SimpleResponse(url, data, status)

from .api_token import api_key

# The Telegram bot token is retrieved inside each helper function rather than
# at import time. This prevents ``ValueError`` when the environment variable is
# absent during module import.

def bot_status(bot_token):
    """Check bot status"""
    # URL to check the status of BotFather
    url = f'https://api.telegram.org/bot{bot_token}/getMe'

    try:
        response = requests.get(url)
        response.raise_for_status()  # Will raise an HTTPError if the HTTP request returned an unsuccessful status code
        data = response.json()

        if data.get('ok'):
            bot_info = data.get('result')
            print(f"Bot ID: {bot_info['id']}")
            print(f"Bot Name: {bot_info['first_name']} is live.")
            print(f"Bot Username: {bot_info['username']}")
        else:
            print("Bot status check failed. Response JSON: ", data)
    except requests.exceptions.RequestException as e:
        print(f"Failed to connect to the AtmoceanBot API. Error: {e}")

def postbot(bot_token, message_text):
    """Post Jobs"""
    channel_name = 'atmocean'
    # URL for sending a message to a channel
    url = f'https://api.telegram.org/bot{bot_token}/sendMessage'

    # Set the parameters for the message
    data = {
        'chat_id': f'@{channel_name}',
        'text': message_text,
        'parse_mode': 'Markdown',
    }

    # Send the message using the GET request
    response = requests.get(url, params=data)

    if response.status_code == 200:
        print("Message sent successfully.")
    else:
        print("Failed to send the message.")
