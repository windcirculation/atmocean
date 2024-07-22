import requests
from api_token import api_key


bot_token = api_key()

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