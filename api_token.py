import os

def api_key():
    token = os.getenv('TELEGRAM_BOT_TOKEN')
    if not token:
        raise ValueError("TELEGRAM_BOT_TOKEN is not set")
    return token