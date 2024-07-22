import os

def api_key():
    return os.getenv('TELEGRAM_BOT_TOKEN')

# apikey = api_key()
# print(apikey)