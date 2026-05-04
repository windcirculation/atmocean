# atmocean

## Environment

Create a file named `example.env` (or `.env`) with your Telegram bot token and add it to `.gitignore` so it is not committed. Example:
```
TELEGRAM_BOT_TOKEN=REMOVED_TELEGRAM_BOT_TOKEN
```

When running locally, source the file:
```bash
source .env
```
In GitHub Actions the secret `TELEGRAM_BOT_TOKEN` is automatically exported.
