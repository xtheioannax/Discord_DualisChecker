# DiscordBots_DualisChecker

A small Python bot that checks DHBW Dualis for grade changes and sends a
notification to a Discord channel through a Discord webhook.

The bot logs in to Dualis, reads the course results, compares them with the
previous check, and repeats this every hour.

## Requirements

- Python 3.10 or newer
- A valid Dualis account
- A Discord webhook URL

Install the Python dependencies:

```powershell
pip install -r .requirements
```

## Setup

### 1. Configure the environment file

The project uses environment variables from a `.env` file. A template is
included as `.env.example`.

Rename `.env.example` to `.env`:

```powershell
Rename-Item .env.example .env
```

If you want to keep the example file for reference, copy it instead:

```powershell
Copy-Item .env.example .env
```

Then open `.env` and fill in your values:

```env
DUALIS_USERNAME="your_dualis_username"
DUALIS_PASSWORD="your_dualis_password"
DISCORD_WEBHOOK_URL="your_discord_webhook_url"
```

### 2. Environment variables

`DUALIS_USERNAME`

Your Dualis login username.

`DUALIS_PASSWORD`

Your Dualis login password.

`DISCORD_WEBHOOK_URL`

The Discord webhook URL for the channel where grade notifications should be
sent.

To create a Discord webhook:

1. Open your Discord server settings.
2. Go to `Integrations`.
3. Create or select a webhook.
4. Copy the webhook URL.
5. Paste it into `DISCORD_WEBHOOK_URL` in your `.env` file.

## Running the bot

Start the checker with:

```powershell
python main.py
```

The script keeps running and checks Dualis once per hour. When it detects a new
or changed grade, it sends a message to the configured Discord webhook.

To stop the bot, press `Ctrl+C` in the terminal.

## Project files

- `main.py` starts the hourly check loop.
- `dualis.py` handles login, grade retrieval, grade parsing, and logout.
- `change_detection.py` compares the newest Dualis result with the previous
  result.
- `discord_webhook.py` sends Discord notifications.
- `.requirements` lists the Python dependencies.
- `.env.example` is the template for the required environment variables.

## Security notes

Do not commit your `.env` file. It contains your Dualis credentials and Discord
webhook URL. The repository already ignores `.env` through `.gitignore`, so keep
your real secrets in `.env` only.
